import pandas as pd
import json
import sys
import uuid

def generate_uuid():
    return str(uuid.uuid4())

def process_csv_with_pandas(file_path):
    # Load CSV into a pandas DataFrame. Fill missing values with an empty string.
    df = pd.read_csv(file_path, dtype=str).fillna("")
    
    # Top-level metadata (assumed consistent across the CSV)
    top_year    = df.loc[0, "YEAR"].strip()
    top_brand   = df.loc[0, "BRAND"].strip()
    top_program = df.loc[0, "PROGRAM"].strip()
    top_sport   = df.loc[0, "SPORT"].strip()
    
    # Build groups sequentially.
    # Each group is a dict with:
    #  - "base_set": the base set name (first occurrence)
    #  - "base_rows": list of rows (as Series) whose CARD SET exactly equals the base set
    #  - "parallel_rows": list of tuples (row, parallel_name) for rows where CARD SET starts with base_set + " "
    groups = []
    current_group = None
    current_base = None
    
    for _, row in df.iterrows():
        card_set = row["CARD SET"].strip()
        if current_group is None:
            # Start first group.
            current_group = {
                "base_set": card_set,
                "base_rows": [row],
                "parallel_rows": []  # will hold tuples: (row, parallel_name)
            }
            current_base = card_set
        else:
            # Updated logic: Only treat as parallel if card_set equals current_base
            # or starts with current_base followed by a space.
            if card_set == current_base or card_set.startswith(current_base + " "):
                if card_set == current_base:
                    current_group["base_rows"].append(row)
                else:
                    # Derive parallel name: remove current_base and the following space, then strip hyphens/spaces.
                    parallel_name = card_set[len(current_base)+1:].strip(" -")
                    current_group["parallel_rows"].append((row, parallel_name))
            else:
                # This row does not belong to the current group.
                groups.append(current_group)
                current_group = {
                    "base_set": card_set,
                    "base_rows": [row],
                    "parallel_rows": []
                }
                current_base = card_set
    if current_group is not None:
        groups.append(current_group)
    
    # Now process each group into a set object.
    sets = []
    for group in groups:
        base_set = group["base_set"]
        base_rows = group["base_rows"]
        parallel_rows = group["parallel_rows"]
        
        # Process base rows into card objects.
        base_cards = []
        base_card_numbers = set()
        base_sequences = set()
        for row in base_rows:
            card_number = row["CARD NUMBER"].strip()
            athlete = row["ATHLETE"].strip()
            seq_str = row["SEQUENCE"].strip()
            seq_value = int(seq_str) if seq_str.isdigit() else None
            
            base_card_numbers.add(card_number)
            if seq_value is not None:
                base_sequences.add(seq_value)
                
            card_obj = {
                "uniqueId": generate_uuid(),
                "number": card_number,
                "name": athlete,
            }
            # Temporarily store sequence to decide later if we can set it at the set level.
            card_obj["_sequence"] = seq_value
            # Prepare a placeholder for card-level parallels.
            card_obj["parallels"] = []
            base_cards.append(card_obj)
        
        # Determine if the base cards share a uniform (non-None) sequence.
        uniform_base_seq = False
        if base_sequences and len(base_sequences) == 1 and (None not in base_sequences):
            set_numberedTo = base_sequences.pop()
            uniform_base_seq = True
        
        # Remove the temporary _sequence from base cards;
        # if not uniform, assign numberedTo on each card that has it.
        for card_obj in base_cards:
            if uniform_base_seq:
                card_obj.pop("_sequence", None)
            else:
                if card_obj.get("_sequence") is not None:
                    card_obj["numberedTo"] = card_obj["_sequence"]
                card_obj.pop("_sequence", None)
            # Remove empty parallels placeholder.
            if not card_obj["parallels"]:
                del card_obj["parallels"]
        
        # Process parallel rows.
        # Group parallel rows by parallel_name.
        parallels_by_name = {}
        for row, parallel_name in parallel_rows:
            parallels_by_name.setdefault(parallel_name, []).append(row)
        
        # For set-level parallels.
        set_level_parallels = []
        # For card-level parallels, we’ll attach them to the matching base card.
        for parallel_name, rows_list in parallels_by_name.items():
            # Determine the card numbers in this parallel group and gather sequence values.
            parallel_card_numbers = set()
            parallel_sequences = set()
            for row in rows_list:
                card_number = row["CARD NUMBER"].strip()
                parallel_card_numbers.add(card_number)
                seq_str = row["SEQUENCE"].strip()
                seq_value = int(seq_str) if seq_str.isdigit() else None
                if seq_value is not None:
                    parallel_sequences.add(seq_value)
            
            # Check if this parallel covers the entire base set.
            if parallel_card_numbers == base_card_numbers:
                # Complete parallel: attach at the set level.
                parallel_obj = {"name": parallel_name}
                if parallel_sequences and len(parallel_sequences) == 1 and (None not in parallel_sequences):
                    parallel_obj["numberedTo"] = parallel_sequences.pop()
                set_level_parallels.append(parallel_obj)
            else:
                # Incomplete parallel: attach each parallel row to the matching base card.
                for row in rows_list:
                    card_number = row["CARD NUMBER"].strip()
                    seq_str = row["SEQUENCE"].strip()
                    seq_value = int(seq_str) if seq_str.isdigit() else None
                    parallel_obj = {"name": parallel_name}
                    if seq_value is not None:
                        parallel_obj["numberedTo"] = seq_value
                    # Find the matching base card and add this parallel.
                    for card_obj in base_cards:
                        if card_obj["number"] == card_number:
                            if "parallels" not in card_obj:
                                card_obj["parallels"] = []
                            card_obj["parallels"].append(parallel_obj)
                            break
        
        # Build the set object.
        set_obj = {
            "uniqueId": generate_uuid(),
            "name": base_set,
            "cards": base_cards,
            "parallels": set_level_parallels,
            "variations": []
        }
        if uniform_base_seq:
            set_obj["numberedTo"] = set_numberedTo
        sets.append(set_obj)
    
    # Build the top-level JSON object.
    top_obj = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "name": f"{top_year} {top_brand} {top_program} {top_sport}",
        "version": "1.0",
        "uniqueId": generate_uuid(),
        "attributes": [],
        "notes": [],
        "sets": sets
    }
    
    return top_obj

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py input.csv output.json")
        sys.exit(1)
        
    input_csv = sys.argv[1]
    output_json = sys.argv[2]
    
    result = process_csv_with_pandas(input_csv)
    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)
    print(f"JSON output written to {output_json}")
