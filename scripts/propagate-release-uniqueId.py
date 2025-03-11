#!/usr/bin/env python3
import json
import sys
import os
from collections import OrderedDict

def format_filename(name):
    """
    Cleans up the release name by replacing spaces with '-' and removing apostrophes.
    """
    return name.replace(" ", "-").replace("'", "")

def reorder_release_data(release_data, unique_id):
    """
    Reorders the top-level keys of release_data so that:
      - If present, "$schema" comes first.
      - Then "name", "version", "uniqueId", "attributes", "notes", "sets".
      - "uniqueId" is set to the provided unique_id.
      - Any other keys (if any) are appended in their original order.
    """
    new_data = OrderedDict()

    # If $schema exists, preserve it at the top.
    if "$schema" in release_data:
        new_data["$schema"] = release_data["$schema"]

    # Order as specified by the schema.
    for key in ["name", "version"]:
        if key in release_data:
            new_data[key] = release_data[key]
    
    # Insert uniqueId with the new value.
    new_data["uniqueId"] = unique_id

    # Then add attributes, notes, sets in that order if they exist.
    for key in ["attributes", "notes", "sets"]:
        if key in release_data:
            new_data[key] = release_data[key]

    # Add any remaining keys that weren't already added.
    for key, value in release_data.items():
        if key not in new_data:
            new_data[key] = value

    return new_data

def update_release_file(base_dir, category, year, release_name, unique_id):
    """
    Builds the relative file path using the pattern:
      <base_dir>/<category>/<year>/<year>-<formatted_release_name>.json
    Opens the JSON file at that location, sets its top-level "uniqueId" property in the proper order,
    and writes the updated JSON back to disk with a 4-space indent.
    """
    formatted_name = format_filename(release_name)
    file_name = f"{year}-{formatted_name}.json"
    file_path = os.path.join(base_dir, category, year, file_name)
    
    try:
        with open(file_path, 'r') as f:
            # Load preserving key order.
            release_data = json.load(f, object_pairs_hook=OrderedDict)
    except Exception as e:
        print(f"Error reading file '{file_path}': {e}")
        return

    # Reorder the data with uniqueId inserted in the proper position.
    new_release_data = reorder_release_data(release_data, unique_id)

    try:
        with open(file_path, 'w') as f:
            json.dump(new_release_data, f, indent=4)
        print(f"Updated '{file_path}' with uniqueId: {unique_id}")
    except Exception as e:
        print(f"Error writing file '{file_path}': {e}")

def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <main_json_file>")
        sys.exit(1)

    main_json_file = sys.argv[1]
    # Use the directory of the main JSON file as the base directory for relative paths.
    base_dir = os.path.dirname(os.path.abspath(main_json_file))
    
    try:
        with open(main_json_file, 'r') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error reading main JSON file '{main_json_file}': {e}")
        sys.exit(1)
    
    # Iterate over each category, year, and release record.
    for category_obj in data:
        category_name = category_obj.get("category")
        if not category_name:
            continue  # Skip if category name is missing.
        
        years = category_obj.get("years", [])
        for year_obj in years:
            year_value = year_obj.get("year")
            if not year_value:
                continue  # Skip if year value is missing.
            
            releases = year_obj.get("releases", [])
            for release in releases:
                # Only process releases that are indexed.
                if release.get("indexed") is not True:
                    continue
                unique_id = release.get("uniqueId")
                if not unique_id:
                    continue  # Skip if uniqueId is missing.
                release_name = release.get("name")
                if not release_name:
                    continue  # Skip if release name is missing.
                update_release_file(base_dir, category_name, year_value, release_name, unique_id)

if __name__ == "__main__":
    main()
