#!/usr/bin/env python3
import json
import sys
import uuid

def add_missing_unique_ids(data):
    """
    Traverse the JSON structure and add a uniqueId to any release that is indexed (indexed: true)
    and missing a uniqueId.
    The JSON structure is expected to be an array of objects. Each object contains a "years" array,
    and each year contains a "releases" array.
    """
    for category in data:
        years = category.get('years', [])
        for year_item in years:
            releases = year_item.get('releases', [])
            for release in releases:
                # Only add uniqueId if 'indexed' is True and uniqueId is missing
                if release.get('indexed') is True and 'uniqueId' not in release:
                    release['uniqueId'] = str(uuid.uuid4())
    return data

def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <json_file>")
        sys.exit(1)

    json_file = sys.argv[1]
    try:
        with open(json_file, 'r') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error reading JSON file: {e}")
        sys.exit(1)

    updated_data = add_missing_unique_ids(data)

    try:
        with open(json_file, 'w') as f:
            json.dump(updated_data, f, indent=2)
        print(f"File '{json_file}' updated successfully.")
    except Exception as e:
        print(f"Error writing JSON file: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
