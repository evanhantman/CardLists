import json
from pathlib import Path
import pandas as pd

def flatten_card_data(sport, year, release, json_data):
    """
    Given the metadata and loaded JSON data,
    iterate over each set and each card to create flat records.
    """
    records = []
    source = json_data.get("name", "")  # top-level name field

    # Loop over each set in the JSON file
    for card_set in json_data.get("sets", []):
        set_name = card_set.get("name", "")
        # Loop over each card in the current set
        for card in card_set.get("cards", []):
            record = {
                "sport": sport,
                "year": year,
                "release": release,
                "source": source,
                "set": set_name,
                "card_number": card.get("number", ""),
                "card_name": card.get("name", ""),
                # Optionally, you can add more fields (or even serialize nested fields as JSON)
                "attributes": card.get("attributes", []),
                "note": card.get("note", "")
            }
            records.append(record)
    return records

def main():
    root = Path(".")
    all_records = []

    # The directory structure is assumed to be: ./<Sport>/<Year>/*.json
    for sport_dir in root.iterdir():
        if sport_dir.is_dir():
            for year_dir in sport_dir.iterdir():
                if year_dir.is_dir():
                    # Process each JSON file in the year directory
                    for json_file in year_dir.glob("*.json"):
                        # Extract release name from filename (e.g., "1990-Topps.json" -> "Topps")
                        parts = json_file.stem.split("-", 1)
                        release = parts[1] if len(parts) == 2 else parts[0]
                        try:
                            with json_file.open("r", encoding="utf-8") as f:
                                data = json.load(f)
                            records = flatten_card_data(sport_dir.name, year_dir.name, release, data)
                            all_records.extend(records)
                        except Exception as e:
                            print(f"Error processing {json_file}: {e}")

    if all_records:
        df = pd.DataFrame(all_records)
        output_dir = Path("output")
        output_dir.mkdir(exist_ok=True)
        parquet_path = output_dir / "dataset.parquet"
        df.to_parquet(parquet_path, index=False)
        print(f"Dataset written to {parquet_path}")
    else:
        print("No records found to process.")

if __name__ == "__main__":
    main()
