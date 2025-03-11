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
      - If present, "$schema" is preserved at the top.
      - Then "name" and "version" are kept in order.
      - "uniqueId" is then inserted.
      - Followed by "attributes", "notes", "sets" (if present).
      - Any additional keys are appended in their original order.
    """
    new_data = OrderedDict()

    # Preserve $schema at the top if it exists.
    if "$schema" in release_data:
        new_data["$schema"] = release_data["$schema"]

    # Add "name" and "version" in order.
    for key in ["name", "version"]:
        if key in release_data:
            new_data[key] = release_data[key]
    
    # Insert "uniqueId" with the new value.
    new_data["uniqueId"] = unique_id

    # Then add "attributes", "notes", and "sets" in that order if present.
    for key in ["attributes", "notes", "sets"]:
        if key in release_data:
            new_data[key] = release_data[key]

    # Append any remaining keys that were not already added.
    for key, value in release_data.items():
        if key not in new_data:
            new_data[key] = value

    return new_data

def update_release_file(base_dir, category, year, release_name, unique_id):
    """
    Builds the relative file path using the pattern:
      <base_dir>/<category>/<year>/<year>-<formatted_release_name>.json
    Opens the JSON file at that location, updates its top-level "uniqueId" (in the proper order),
    and writes the updated JSON back to disk with 4-space indentation.
    """
    formatted_name = format_filename(release_name)
    file_name = f"{year}-{formatted_name}.json"
    file_path = os.path.join(base_dir, category, year, file_name)
    
    try:
        with open(file_path, 'r') as f:
            # Load JSON preserving key order.
            release_data = json.load(f, object_pairs_hook=OrderedDict)
    except Exception as e:
        print(f"Error reading file '{file_path}': {e}")
        return
    
    # Reorder the data with uniqueId inserted after version.
    new_release_data = reorder_release_data(release_data, unique_id)
    
    try:
        with open(file_path, 'w') as f:
            json.dump(new_release_data, f, indent=4)
        print(f"Updated '{file_path}' with uniqueId: {unique_id}")
    except Exception as e:
        print(f"Error writing file '{file_path}': {e}")

def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <category_json_file>")
        sys.exit(1)

    category_json_file = sys.argv[1]
    # Use the directory of the category JSON file as the base directory for relative paths.
    base_dir = os.path.dirname(os.path.abspath(category_json_file))
    
    try:
        with open(category_json_file, 'r') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error reading category JSON file '{category_json_file}': {e}")
        sys.exit(1)
    
    # According to the new schema, the top-level object must contain "category".
    category_obj = data.get("category")
    if not category_obj:
        print("Error: 'category' property not found in the JSON file.")
        sys.exit(1)
    
    category_name = category_obj.get("name")
    if not category_name:
        print("Error: 'name' property not found in the category.")
        sys.exit(1)
    
    years = category_obj.get("years", [])
    for year_obj in years:
        year_value = year_obj.get("year")
        if not year_value:
            print("Warning: 'year' value missing, skipping entry.")
            continue
        
        releases = year_obj.get("releases", [])
        for release in releases:
            # Process only releases that are indexed.
            if release.get("indexed") is not True:
                continue
            unique_id = release.get("uniqueId")
            if not unique_id:
                continue  # Skip if uniqueId is not present.
            release_name = release.get("name")
            if not release_name:
                continue
            update_release_file(base_dir, category_name, year_value, release_name, unique_id)

if __name__ == "__main__":
    main()
