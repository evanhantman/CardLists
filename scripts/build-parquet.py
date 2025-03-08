import json
from pathlib import Path
import pandas as pd

def flatten_card_data(category, year, release, json_data):
    """
    Iterate over each set and each card to create flat records.
    For every card, a base record is always created.
    Then, additional records for parallels and variations are created.
    Variation records have a modified card_name and combined attributes.
    For variations, the attribute list is combined from the base attributes,
    any additional variation attributes, and the literal "VAR" is appended to denote it's a variation.
    
    A temporary field '_is_variation' is used internally for counting purposes,
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
            # Base record for the card
            base_record = {
                "category": category,
                "year": year,
                "release": release,
                "source": source,
                "set_unique_id": card_set.get("uniqueId", ""),
                "set": set_name,
                "card_unique_id": card.get("uniqueId", ""),
                "card_number": card.get("number", ""),
                "card_name": base_card_name,
                "attributes": card.get("attributes", []),
                "note": card.get("note", ""),
                "parallel": "",
                "_is_variation": False
            }
            records.append(base_record)

            # Add parallels for the base card: combine card-level and set-level parallels
            base_parallels = card.get("parallels", [])
            all_base_parallels = base_parallels + set_parallels
            for parallel in all_base_parallels:
                parallel_record = base_record.copy()
                parallel_record["parallel"] = parallel.get("name", "")
                parallel_record["_is_variation"] = False
                records.append(parallel_record)
            
            # Process variations for the card.
            for variation in card.get("variations", []):
                variation_name = variation.get("variation", "")
                variation_record = base_record.copy()
                # Update card_name to append the variation name in parenthesis.
                if variation_name:
                    variation_record["card_name"] = f"{base_card_name} ({variation_name})"
                else:
                    variation_record["card_name"] = base_card_name

                # Combine attributes: start with base attributes,
                # then add any attributes provided by the variation,
                # and finally append the literal "VAR" to denote it's a variation.
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
                    v_par_record["parallel"] = v_parallel.get("name", "")
                    v_par_record["_is_variation"] = True
                    records.append(v_par_record)
    return records

def main():
    # Since this script is in the 'export' folder, the repository root is one level up.
    base_dir = Path(__file__).parent.parent
    categories_dir = base_dir / "categories"
    all_records = []

    # Directory structure: <repo_root>/categories/<category>/<year>/*.json
    for category_dir in categories_dir.iterdir():
        if category_dir.is_dir():
            for year_dir in category_dir.iterdir():
                if year_dir.is_dir():
                    for json_file in year_dir.glob("*.json"):
                        # Extract release info from filename (e.g., "1990-Topps.json" -> "Topps")
                        parts = json_file.stem.split("-", 1)
                        release = parts[1] if len(parts) == 2 else parts[0]
                        try:
                            with json_file.open("r", encoding="utf-8") as f:
                                data = json.load(f)
                            records = flatten_card_data(category_dir.name, year_dir.name, release, data)
                            all_records.extend(records)
                        except Exception as e:
                            print(f"Error processing {json_file}: {e}")

    if all_records:
        # Calculate card counts for the four specified categories.
        # Only count base card records (records where parallel is empty and _is_variation is False).
        target_categories = ["baseball", "football", "basketball", "hockey"]
        counts = {cat: 0 for cat in target_categories}
        for record in all_records:
            if record.get("parallel", "") == "" and not record.get("_is_variation", False):
                cat_lower = record.get("category", "").lower()
                if cat_lower in counts:
                    counts[cat_lower] += 1

        # Remove the temporary field '_is_variation' from all records.
        for record in all_records:
            if "_is_variation" in record:
                del record["_is_variation"]

        # Create a DataFrame, sort by year and release (ascending), then write to a Parquet file.
        df = pd.DataFrame(all_records)
        df = df.sort_values(by=["year", "release"], ascending=True)
        output_dir = base_dir / "output"
        output_dir.mkdir(exist_ok=True)
        parquet_path = output_dir / "dataset.parquet"
        df.to_parquet(parquet_path, index=False)
        print(f"Dataset written to {parquet_path}")

        # Write the card counts to a JSON file at the repository root.
        card_counts_file = base_dir / "card_counts.json"
        with open(card_counts_file, "w", encoding="utf-8") as f:
            json.dump(counts, f)
        print(f"Card counts written to {card_counts_file}: {counts}")
    else:
        print("No records found to process.")

if __name__ == "__main__":
    main()
