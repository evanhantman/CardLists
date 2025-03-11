#!/usr/bin/env python3
import os
import sys
import json
import uuid

def process_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return

    # Expecting the file to follow the schema:
    # {
    #   "$schema": "http://json-schema.org/draft-07/schema#",
    #   "category": {
    #       "name": "Category Name",
    #       "years": [
    #           {
    #               "year": "2021",
    #               "releases": [
    #                   {
    #                       "name": "Release Name",
    #                       "indexed": true,
    #                       "version": "1.0",
    #                       "uniqueId": "optional-guid"
    #                   },
    #                   ...
    #               ]
    #           },
    #           ...
    #       ]
    #   }
    # }
    category = data.get("category")
    if category is None:
        print(f"File {filepath} does not contain a 'category' property.")
        return

    years = category.get("years", [])
    for year_obj in years:
        releases = year_obj.get("releases", [])
        for release in releases:
            if release.get("indexed") and "uniqueId" not in release:
                release["uniqueId"] = str(uuid.uuid4())

    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
        print(f"Updated: {filepath}")
    except Exception as e:
        print(f"Error writing {filepath}: {e}")

def main(filepath):
    if not os.path.isfile(filepath):
        print(f"Error: {filepath} is not a valid file.")
        return
    process_file(filepath)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python update_json.py <json_file>")
        sys.exit(1)
    main(sys.argv[1])
