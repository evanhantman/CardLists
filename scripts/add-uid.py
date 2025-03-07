#!/usr/bin/env python3
import os
import sys
import json
import uuid

#Adds the Unique ID field fo each card and set in the JSON files

def process_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return

    # Process each set in the release
    sets = data.get("sets", [])
    for s in sets:
        if "uniqueId" not in s:
            s["uniqueId"] = str(uuid.uuid4())
        # Process each card in the set
        cards = s.get("cards", [])
        for card in cards:
            if "uniqueId" not in card:
                card["uniqueId"] = str(uuid.uuid4())

    # Write back the modified JSON data
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
        print(f"Updated: {filepath}")
    except Exception as e:
        print(f"Error writing {filepath}: {e}")

def main(root_path):
    for dirpath, _, filenames in os.walk(root_path):
        for filename in filenames:
            if filename.lower().endswith('.json'):
                file_path = os.path.join(dirpath, filename)
                process_file(file_path)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python add-uid.py <path>")
        sys.exit(1)
    main(sys.argv[1])
