import json
from pathlib import Path
import pandas as pd
import sys
import uuid  # Add this import to generate new unique IDs

def flatten_card_data(category, year, release, json_data):
    """
    Iterate over each set and each card to create flat records.
    For every card, a base record is always created using the updated base_record.
    Then, additional records for parallels and variations are created.
    
    Variation records have a modified card_name (appending the variation name in parenthesis)
    and a combined attributes list (base attributes plus any variation attributes, then "VAR").
    
    For parallel records, if the parallel object defines a "numberedTo" value or an "insertOdds" array,
    they are applied to the record.
    
    Parallel cards get their own unique ID and maintain a reference to their parent card.
    
    A temporary field '_is_variation' is used internally for duplicate checking,
    but will be removed before writing the final output.
    """
    records = []
    source = json_data.get("name", "")

    for card_set in json_data.get("sets", []):
        set_name = card_set.get("name", "")
        # Get set-level parallels that apply to all cards/variations.
        set_parallels = card_set.get("parallels", [])
        for card in card_set.get("cards", []):
            base_card_name = card.get("name", "")
            # Get or generate base card unique ID
            base_card_unique_id = card.get("uniqueId", "")
            if not base_card_unique_id:
                base_card_unique_id = str(uuid.uuid4())
                
            # Updated base record with GUID fields.
            base_record = {
                "category": category,
                "release_unique_id": json_data.get("uniqueId", ""),
                "year": year,
                "release": release,
                "release_name": source,
                "set_unique_id": card_set.get("uniqueId", ""),
                "set": set_name,
                "card_unique_id": base_card_unique_id,
                "card_parent_unique_id": "",  # Base cards don't have a parent
                "card_number": card.get("number", ""),
                "card_name": base_card_name,
                "attributes": card_set.get("attributes", []) + card.get("attributes", []),
                "note": card.get("note", ""),
                "parallel": "",
                "_is_variation": False
            }
            records.append(base_record)

            # Add parallels for the base card: combine card-level and set-level parallels.
            base_parallels = card.get("parallels", [])
            all_base_parallels = base_parallels + set_parallels
            for parallel in all_base_parallels:
                parallel_record = base_record.copy()
                # Generate a new unique ID for the parallel
                parallel_record["card_unique_id"] = str(uuid.uuid4())
                # Link back to the parent card
                parallel_record["card_parent_unique_id"] = base_card_unique_id
                parallel_record["parallel"] = parallel.get("name", "")
                # Apply parallel's numberedTo if provided.
                if "numberedTo" in parallel:
                    parallel_record["numberedTo"] = parallel["numberedTo"]
                # Apply parallel's insertOdds if provided.
                if "insertOdds" in parallel:
                    parallel_record["insertOdds"] = parallel["insertOdds"]
                parallel_record["_is_variation"] = False
                records.append(parallel_record)
            
            # Process variations for the card.
            for variation in card.get("variations", []):
                variation_name = variation.get("variation", "")
                # Generate a unique ID for the variation
                variation_unique_id = str(uuid.uuid4())
                
                variation_record = base_record.copy()
                variation_record["card_unique_id"] = variation_unique_id
                variation_record["card_parent_unique_id"] = base_card_unique_id
                
                # Update card_name: append the variation name in parenthesis.
                if variation_name:
                    variation_record["card_name"] = f"{base_card_name} ({variation_name})"
                else:
                    variation_record["card_name"] = base_card_name

                # Combine attributes: base attributes plus any variation attributes, then append "VAR".
                combined_attributes = base_record["attributes"].copy() if base_record["attributes"] else []
                if variation.get("attributes"):
                    combined_attributes.extend(variation.get("attributes"))
                combined_attributes.append("VAR")
                variation_record["attributes"] = combined_attributes

                # Override note if the variation has its own.
                if variation.get("note"):
                    variation_record["note"] = variation.get("note")
                # Carry over additional properties if present.
                if "insertOdds" in variation:
                    variation_record["insertOdds"] = variation.get("insertOdds")
                if "numberedTo" in variation:
                    variation_record["numberedTo"] = variation.get("numberedTo")
                # Mark as a variation.
                variation_record["_is_variation"] = True
                variation_record["parallel"] = ""
                records.append(variation_record)
                
                # Add parallels for the variation: combine variation-level and set-level parallels.
                variation_parallels = variation.get("parallels", [])
                all_variation_parallels = variation_parallels + set_parallels
                for v_parallel in all_variation_parallels:
                    v_par_record = variation_record.copy()
                    # Generate a new unique ID for the variation's parallel
                    v_par_record["card_unique_id"] = str(uuid.uuid4())
                    # Link back to the variation as the parent
                    v_par_record["card_parent_unique_id"] = variation_unique_id
                    
                    v_par_record["parallel"] = v_parallel.get("name", "")
                    # Apply parallel's numberedTo if provided.
                    if "numberedTo" in v_parallel:
                        v_par_record["numberedTo"] = v_parallel["numberedTo"]
                    # Apply parallel's insertOdds if provided.
                    if "insertOdds" in v_parallel:
                        v_par_record["insertOdds"] = v_parallel["insertOdds"]
                    v_par_record["_is_variation"] = True
                    records.append(v_par_record)
    return records

def main():
    # Since this script is in the 'scripts' folder, the repository root is one level up.
    base_dir = Path(__file__).parent.parent
    categories_dir = base_dir / "categories"
    all_records = []

    # Process JSON files and flatten records.
    for category_dir in categories_dir.iterdir():
        if category_dir.is_dir():
            for year_dir in category_dir.iterdir():
                if year_dir.is_dir():
                    for json_file in year_dir.glob("*.json"):
                        parts = json_file.stem.split("-", 1)
                        release = parts[1] if len(parts) == 2 else parts[0]
                        try:
                            with json_file.open("r", encoding="utf-8") as f:
                                data = json.load(f)
                            records = flatten_card_data(category_dir.name, year_dir.name, release, data)
                            all_records.extend(records)
                        except Exception as e:
                            print(f"Error processing {json_file}: {e}")
                            sys.exit(1)

    if not all_records:
        print("No records found to process.")
        sys.exit(1)

    # Create a DataFrame.
    df = pd.DataFrame(all_records)

    # Filter to base records: those with no parallel and not marked as a variation.
    df_base = df[(df["parallel"] == "") & (~df["_is_variation"])]

    # For set_unique_id, drop duplicate rows (since the same set appears on multiple cards)
    # then group by set_unique_id and check if a single set name is associated with each.
    df_sets = df_base[['set_unique_id', 'set']].drop_duplicates()
    dup_sets = df_sets.groupby('set_unique_id')['set'].nunique()
    if (dup_sets > 1).any():
        dup_ids = dup_sets[dup_sets > 1].index.tolist()
        raise ValueError(f"Duplicate set_unique_id found for multiple sets: {dup_ids}")

    # For card_unique_id, drop duplicate rows (if any) and then check for duplicates.
    df_cards = df_base[['card_unique_id', 'card_name']].drop_duplicates()
    if df_cards['card_unique_id'].duplicated().any():
        dup_ids = df_cards[df_cards['card_unique_id'].duplicated(keep=False)]['card_unique_id'].unique()
        raise ValueError(f"Duplicate card_unique_id found in base records: {dup_ids}")

    # Remove the temporary field '_is_variation' from all records.
    df = df.drop(columns=["_is_variation"])

    # Sort the DataFrame by year and release (ascending).
    df = df.sort_values(by=["year", "release"], ascending=True)

    # Write to a Parquet file.
    output_dir = base_dir / "output"
    output_dir.mkdir(exist_ok=True)
    parquet_path = output_dir / "dataset.parquet"
    df.to_parquet(parquet_path, index=False)
    print(f"Dataset written to {parquet_path}")

if __name__ == "__main__":
    main()
