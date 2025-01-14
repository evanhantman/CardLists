import json
from pathlib import Path
from typing import List, Optional
from pydantic import BaseModel, ValidationError

# Class definitions based on the schema

class AttributeItem(BaseModel):
    attribute: str
    note: str

class Variation(BaseModel):
    variation: str
    note: Optional[str]

class Parallel(BaseModel):
    name: str
    of: Optional[int]
    notes: List[str]

class Card(BaseModel):
    number: Optional[str]
    name: str
    attributes: Optional[List[str]]
    note: Optional[str]
    variations: Optional[List[Variation]]
    parallels: Optional[List[Parallel]]

class Set(BaseModel):
    name: str
    notes: List[str]
    variations: Optional[List[Variation]]
    parallels: Optional[List[Parallel]]
    cards: List[Card]

class CardList(BaseModel):
    name: str
    attributes: Optional[List[AttributeItem]]
    sets: List[Set]


def main(file_path: str):
    try:
        # Load and parse the JSON file
        with open(file_path, 'r') as file:
            data = json.load(file)

        # Validate and parse the JSON data into the CardList model
        root_object = CardList(**data)

        # Print the validated data in a pretty format
        print("JSON file loaded and validated successfully!")
        print(json.dumps(root_object.dict(), indent=4))

    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
    except json.JSONDecodeError as e:
        print(f"Error: Failed to decode JSON - {e}")
    except ValidationError as e:
        print("Error: JSON validation failed.")
        print(e.json())


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python main.py <path-to-json-file>")
    else:
        main(sys.argv[1])
