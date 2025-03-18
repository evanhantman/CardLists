#!/usr/bin/env python3
import json
import sys
import argparse
import pathlib
import glob

def traverse_card_obj(obj, collected, warnings):
    """
    Recursively traverse a card (or variation) object.
    Collect attribute strings from the "attributes" key and
    continue into nested "variations".
    """
    if isinstance(obj, dict):
        if "attributes" in obj:
            attrs = obj["attributes"]
            if isinstance(attrs, list):
                for attr in attrs:
                    collected.add(attr)
            else:
                warnings.append(f"Warning: 'attributes' is not a list in object: {obj}")
        if "variations" in obj:
            variations = obj["variations"]
            if isinstance(variations, list):
                for variation in variations:
                    traverse_card_obj(variation, collected, warnings)
            else:
                warnings.append(f"Warning: 'variations' is not a list in object: {obj}")

def validate_file(file_path):
    """
    Validate a single JSON file with two checks:
      (a) Internal consistency:
          - Each attribute used on cards (or nested variations) is defined
            in the root-level "attributes" array.
          - Every attribute defined in the root appears on at least one card.
      (b) Also, extract the root attribute definitions (mapping attribute -> note)
          for later cross-file consistency validation.
    Returns a tuple: (list_of_errors, root_attribute_map)
    """
    errors = []
    warnings = []
    root_attr_map = {}  # Mapping: attribute -> note
    try:
        with open(file_path, "r") as f:
            data = json.load(f)
    except Exception as e:
        errors.append(f"Failed to read JSON file: {e}")
        return errors, root_attr_map

    # Extract root-level attributes.
    if "attributes" in data:
        for attr_pair in data["attributes"]:
            if (
                isinstance(attr_pair, dict)
                and "attribute" in attr_pair
                and "note" in attr_pair
            ):
                attr_name = attr_pair["attribute"]
                note = attr_pair["note"]
                # Check for conflicting definitions within the same file.
                if attr_name in root_attr_map and root_attr_map[attr_name] != note:
                    errors.append(
                        f"In file, attribute '{attr_name}' defined with conflicting notes: '{root_attr_map[attr_name]}' and '{note}'."
                    )
                else:
                    root_attr_map[attr_name] = note
            else:
                errors.append(f"Invalid attribute pair in root 'attributes' array: {attr_pair}")

    # Collect all attributes used in cards and nested variations.
    card_attrs = set()
    if "sets" not in data:
        errors.append("Missing 'sets' property in JSON data.")
        return errors, root_attr_map

    for s in data["sets"]:
        if "cards" not in s:
            errors.append(f"A set is missing the 'cards' property: {s}")
            continue
        for card in s["cards"]:
            traverse_card_obj(card, card_attrs, warnings)

    # Two-way per-file validation:
    # 1. Every attribute on a card must be defined in the root-level attributes.
    for attr in card_attrs:
        if attr not in root_attr_map:
            errors.append(
                f"Attribute '{attr}' found on a card but not defined in root attributes."
            )
    # 2. Every attribute defined in the root must appear on at least one card.
    for attr in root_attr_map:
        if attr not in card_attrs:
            errors.append(
                f"Attribute '{attr}' defined in root attributes but not found on any card."
            )

    # Report any warnings to stderr.
    for warn in warnings:
        print(warn, file=sys.stderr)

    return errors, root_attr_map

def find_json_files(path_pattern):
    """
    Given a path (directory, file, or glob pattern),
    return a list of Path objects for JSON files.
    """
    p = pathlib.Path(path_pattern)
    files = []
    # If the argument is an existing directory, search recursively.
    if p.is_dir():
        files = list(p.rglob("*.json"))
    # If it is an existing file, return that file.
    elif p.is_file():
        files = [p]
    # Otherwise, assume it is a glob pattern.
    else:
        files = [pathlib.Path(fp) for fp in glob.glob(path_pattern, recursive=True)]
    return files

def main():
    parser = argparse.ArgumentParser(
        description="Validate JSON files by checking that each attribute used on a card "
                    "is defined in the root-level attributes array and vice versa, "
                    "and then ensuring that attributes have consistent notes across files."
    )
    parser.add_argument("path", help="Path, directory, or glob pattern for JSON files to validate")
    args = parser.parse_args()

    files = find_json_files(args.path)
    if not files:
        print(f"No JSON files found for pattern: {args.path}", file=sys.stderr)
        sys.exit(1)

    overall_errors = {}
    global_attr_notes = {}  # Mapping: attribute -> dict of note -> count

    # Validate each file individually.
    for file in files:
        file_errors, file_attr_map = validate_file(file)
        if file_errors:
            overall_errors[str(file)] = file_errors

        # Accumulate cross-file attribute definitions with counts.
        for attr, note in file_attr_map.items():
            if attr in global_attr_notes:
                global_attr_notes[attr][note] = global_attr_notes[attr].get(note, 0) + 1
            else:
                global_attr_notes[attr] = {note: 1}

    # Cross-file validation: check that each attribute's note is consistent.
    cross_file_errors = []
    for attr, notes_counts in global_attr_notes.items():
        if len(notes_counts) > 1:
            counts_str = ", ".join(f"'{note}': {count}" for note, count in notes_counts.items())
            cross_file_errors.append(
                f"Inconsistent note for attribute '{attr}': found differing notes with counts: {counts_str}."
            )

    # Report errors from per-file validation.
    if overall_errors:
        for file, errors in overall_errors.items():
            print(f"\nErrors in file: {file}", file=sys.stderr)
            for error in errors:
                print("  Error:", error, file=sys.stderr)
    # Report cross-file consistency errors.
    if cross_file_errors:
        print("\nCross-file consistency errors:", file=sys.stderr)
        for error in cross_file_errors:
            print("  Error:", error, file=sys.stderr)

    # Exit with error code if any errors found.
    if overall_errors or cross_file_errors:
        sys.exit(1)
    else:
        print("All JSON files passed attribute validation and cross-file consistency checks.")
        sys.exit(0)

if __name__ == "__main__":
    main()
