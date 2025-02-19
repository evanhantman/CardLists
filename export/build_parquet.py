import json
from pathlib import Path
import pandas as pd

def flatten_card_data(sport, year, release, json_data):
    """
    Given the metadata and loaded JSON data,
    iterate over each set and each card to create flat records.
    """
    records = []
    source = json_data.get("name", "")  # Top-level name field

    for card_set in json_data.get("sets", []):
        set_name = card_set.get("name", "")
        for card in card_set.get("cards", []):
            record = {
                "sport": sport,
                "year": year,
                "release": release,
                "source": source,
                "set": set_name,
                "card_number": card.get("number", ""),
                "card_name": card.get("name", ""),
                "attributes": card.get("attributes", []),
                "note": card.get("note", "")
            }
            records.append(record)
    return records

def main():
    # Since this script is in the 'export' folder, the repository root is one level up.
    base_dir = Path(__file__).parent.parent
    all_records = []

    # Assume the directory structure is: <repo_root>/<Sport>/<Year>/*.json
    for sport_dir in base_dir.iterdir():
        if sport_dir.is_dir():
            for year_dir in sport_dir.iterdir():
                if year_dir.is_dir():
                    for json_file in year_dir.glob("*.json"):
                        # Extract release info from filename (e.g., "1990-Topps.json" -> "Topps")
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
        # Create a DataFrame and write to a Parquet file in <repo_root>/output
        df = pd.DataFrame(all_records)
        output_dir = base_dir / "output"
        output_dir.mkdir(exist_ok=True)
        parquet_path = output_dir / "dataset.parquet"
        df.to_parquet(parquet_path, index=False)
        print(f"Dataset written to {parquet_path}")

        # Calculate card counts for the four specified sports
        target_sports = ["baseball", "football", "basketball", "hockey"]
        counts = {sport: 0 for sport in target_sports}
        for record in all_records:
            sport_lower = record.get("sport", "").lower()
            if sport_lower in counts:
                counts[sport_lower] += 1

        # Write the counts to a JSON file at the repository root
        card_counts_file = base_dir / "card_counts.json"
        with open(card_counts_file, "w", encoding="utf-8") as f:
            json.dump(counts, f)
        print(f"Card counts written to {card_counts_file}: {counts}")
    else:
        print("No records found to process.")

if __name__ == "__main__":
    main()
