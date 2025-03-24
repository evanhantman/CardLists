import pandas as pd
import json
import sys
import uuid

def generate_uuid():
    return str(uuid.uuid4())

def normalize_text(s):
    """Trim leading/trailing whitespace from a string."""
    return s.strip() if isinstance(s, str) else ""

def normalize_card_number(num_str):
    """Trim and, if numeric, convert to a canonical integer string."""
    num_str = normalize_text(num_str)
    if num_str.isdigit():
        return str(int(num_str))
    return num_str

def get_attributes_for_set(set_name):
    """
    Return a list of attribute codes to apply to cards based on the set name.
    
    Rules:
      - If the set name contains "autograph" (case-insensitive), add "AU"
      - If the set name contains "relic" (case-insensitive), add "RELIC"
    """
    attrs = []
    lower_set = set_name.lower()
    if "autograph" in lower_set:
        attrs.append("AU")
    if "relic" in lower_set:
        attrs.append("RELIC")
    return attrs

def is_parallel_candidate(group1, group2):
    """
    Returns True if group2 should be considered a parallel of group1.
    (Used only when the "PARALLEL OF" column is not present.)
    Currently, if the normalized set of (card number, athlete) pairs in the base rows
    of both groups are equal, then group2 is a parallel candidate.
    """
    def get_base_keys(group):
        return {
            (normalize_card_number(row["CARD NUMBER"]), normalize_text(row["ATHLETE"]))
            for row in group["base_rows"]
        }
    return get_base_keys(group1) == get_base_keys(group2)

def process_csv_with_pandas(file_path):
    # Load CSV into a pandas DataFrame. Fill missing values with an empty string.
    df = pd.read_csv(file_path, dtype=str).fillna("")
    
    # Top-level metadata (assumed consistent across the CSV)
    top_year    = normalize_text(df.loc[0, "YEAR"])
    top_brand   = normalize_text(df.loc[0, "BRAND"])
    top_program = normalize_text(df.loc[0, "PROGRAM"])
    top_sport   = normalize_text(df.loc[0, "SPORT"])
    
    groups = []
    # --- Grouping Step ---
    # If the CSV has a "PARALLEL OF" column, use it to determine the effective base set.
    if "PARALLEL OF" in df.columns:
        groups_by_manual = {}
        for _, row in df.iterrows():
            card_set = normalize_text(row["CARD SET"])
            parallel_of = normalize_text(row["PARALLEL OF"])
            # Use the PARALLEL OF value if present; otherwise, fall back to CARD SET.
            effective_base = parallel_of if parallel_of != "" else card_set
            if effective_base not in groups_by_manual:
                groups_by_manual[effective_base] = {
                    "base_set": effective_base,
                    "base_rows": [],
                    "parallel_rows": []
                }
            # If PARALLEL OF is non-empty and CARD SET differs from effective_base,
            # treat the row as a parallel.
            if parallel_of != "" and card_set != effective_base:
                # Apply parallel name logic: if card_set starts with effective_base + " ",
                # trim it.
                if card_set.startswith(effective_base + " "):
                    parallel_name = normalize_text(card_set[len(effective_base) + 1:]).strip(" -")
                else:
                    parallel_name = card_set
                groups_by_manual[effective_base]["parallel_rows"].append((row, parallel_name))
            else:
                groups_by_manual[effective_base]["base_rows"].append(row)
        groups = list(groups_by_manual.values())
    else:
        # Use original grouping logic based on "starts-with" rule.
        current_group = None
        current_base = None
        for _, row in df.iterrows():
            card_set = normalize_text(row["CARD SET"])
            if current_group is None:
                current_group = {
                    "base_set": card_set,
                    "base_rows": [row],
                    "parallel_rows": []  # holds tuples: (row, parallel_name)
                }
                current_base = card_set
            else:
                if card_set == current_base or card_set.startswith(current_base + " "):
                    if card_set == current_base:
                        current_group["base_rows"].append(row)
                    else:
                        parallel_name = normalize_text(card_set[len(current_base) + 1:]).strip(" -")
                        current_group["parallel_rows"].append((row, parallel_name))
                else:
                    groups.append(current_group)
                    current_group = {
                        "base_set": card_set,
                        "base_rows": [row],
                        "parallel_rows": []
                    }
                    current_base = card_set
        if current_group is not None:
            groups.append(current_group)
        
        # Merge adjacent groups using matching logic.
        merged_groups = []
        for group in groups:
            merged = False
            for m_group in merged_groups:
                if is_parallel_candidate(m_group, group):
                    for row in group["base_rows"]:
                        m_group["parallel_rows"].append((row, normalize_text(group["base_set"])))
                    for tup in group["parallel_rows"]:
                        m_group["parallel_rows"].append(tup)
                    merged = True
                    break
            if not merged:
                merged_groups.append(group)
        groups = merged_groups
    
    # Process each group into a set object.
    sets = []
    for group in groups:
        base_set = group["base_set"]
        base_rows = group["base_rows"]
        parallel_rows = group["parallel_rows"]
        
        # Get attributes from the set name.
        set_attributes = get_attributes_for_set(base_set)
        
        # Process base rows into card objects.
        base_cards = []
        base_card_numbers = set()
        base_sequences = set()
        for row in base_rows:
            card_number = normalize_card_number(row["CARD NUMBER"])
            athlete = normalize_text(row["ATHLETE"])
            seq_str = normalize_text(row["SEQUENCE"])
            seq_value = int(seq_str) if seq_str.isdigit() else None
            
            base_card_numbers.add(card_number)
            if seq_value is not None:
                base_sequences.add(seq_value)
                
            card_obj = {
                "uniqueId": generate_uuid(),
                "number": card_number,
                "name": athlete,
            }
            card_obj["_sequence"] = seq_value  # temporary field
            card_obj["parallels"] = []
            if set_attributes:
                card_obj["attributes"] = set_attributes.copy()
            base_cards.append(card_obj)
        
        # Determine if the base cards share a uniform (non-None) sequence.
        uniform_base_seq = False
        if base_sequences and len(base_sequences) == 1 and (None not in base_sequences):
            set_numberedTo = base_sequences.pop()
            uniform_base_seq = True
        
        # Clean up base card objects.
        for card_obj in base_cards:
            if uniform_base_seq:
                card_obj.pop("_sequence", None)
            else:
                if card_obj.get("_sequence") is not None:
                    card_obj["numberedTo"] = card_obj["_sequence"]
                card_obj.pop("_sequence", None)
            if "parallels" in card_obj and not card_obj["parallels"]:
                del card_obj["parallels"]
        
        # Process parallel rows.
        # Group parallel rows by parallel name.
        parallels_by_name = {}
        for row, parallel_name in parallel_rows:
            parallels_by_name.setdefault(parallel_name, []).append(row)
        
        set_level_parallels = []
        for parallel_name, rows_list in parallels_by_name.items():
            parallel_card_numbers = set()
            parallel_sequences = set()
            for row in rows_list:
                card_number = normalize_card_number(row["CARD NUMBER"])
                parallel_card_numbers.add(card_number)
                seq_str = normalize_text(row["SEQUENCE"])
                seq_value = int(seq_str) if seq_str.isdigit() else None
                if seq_value is not None:
                    parallel_sequences.add(seq_value)
            if parallel_card_numbers == base_card_numbers:
                parallel_obj = {"name": parallel_name}
                if parallel_sequences and len(parallel_sequences) == 1 and (None not in parallel_sequences):
                    parallel_obj["numberedTo"] = parallel_sequences.pop()
                set_level_parallels.append(parallel_obj)
            else:
                for row in rows_list:
                    card_number = normalize_card_number(row["CARD NUMBER"])
                    seq_str = normalize_text(row["SEQUENCE"])
                    seq_value = int(seq_str) if seq_str.isdigit() else None
                    parallel_obj = {"name": parallel_name}
                    if seq_value is not None:
                        parallel_obj["numberedTo"] = seq_value
                    found = False
                    for card_obj in base_cards:
                        if card_obj["number"] == card_number:
                            if "parallels" not in card_obj:
                                card_obj["parallels"] = []
                            card_obj["parallels"].append(parallel_obj)
                            found = True
                            break
                    if not found:
                        athlete = normalize_text(row["ATHLETE"])
                        new_card = {
                            "uniqueId": generate_uuid(),
                            "number": card_number,
                            "name": athlete,
                            "note": "No Base Set Version"
                        }
                        if seq_value is not None:
                            new_card["numberedTo"] = seq_value
                        new_card["parallels"] = [parallel_obj]
                        if set_attributes:
                            new_card["attributes"] = set_attributes.copy()
                        base_cards.append(new_card)
                        base_card_numbers.add(card_number)
        
        # --- Duplicate Removal Step ---
        unique_cards = []
        seen_keys = set()
        duplicates_found = False
        for card in base_cards:
            key = (card["number"], card["name"])
            if key in seen_keys:
                duplicates_found = True
                continue
            seen_keys.add(key)
            unique_cards.append(card)
        if duplicates_found:
            print(f"Warning: Duplicate records found in set '{base_set}'. Please manually verify the accuracy.")
        base_cards = unique_cards
        
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
    
    top_obj = {
        "$schema": "https://raw.githubusercontent.com/JunkWaxData/CardLists/refs/heads/main/schemas/release.json",
        "name": f"{top_year} {top_brand} {top_program} {top_sport}",
        "version": "1.0",
        "uniqueId": generate_uuid(),
        "attributes": [],
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
