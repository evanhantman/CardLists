import json
from pathlib import Path
from typing import List, Optional
from pydantic import BaseModel, ValidationError

# Model definitions based on the new JSON schema

class AttributeItem(BaseModel):
    attribute: str
    note: str

class InsertOdd(BaseModel):
    product: str
    odds: str

class Variation(BaseModel):
    variation: str
    note: Optional[str] = None
    insertOdds: Optional[List[InsertOdd]] = None
    parallels: Optional[List["Parallel"]] = None  # Forward reference

class Parallel(BaseModel):
    name: str
    numberedTo: Optional[int] = None  # Renamed from "of" to "numberedTo"
    notes: Optional[List[str]] = None
    insertOdds: Optional[List[InsertOdd]] = None

class Card(BaseModel):
    number: Optional[str] = None
    name: str
    attributes: Optional[List[str]] = None
    note: Optional[str] = None
    variations: Optional[List[Variation]] = None
    parallels: Optional[List[Parallel]] = None

class Set(BaseModel):
    name: str
    notes: Optional[List[str]] = None
    numberedTo: Optional[int] = None
    insertOdds: Optional[List[InsertOdd]] = None
    variations: Optional[List[Variation]] = None
    parallels: Optional[List[Parallel]] = None
    cards: List[Card]

class CardList(BaseModel):
    name: str
    notes: Optional[List[str]] = None
    attributes: Optional[List[AttributeItem]] = None
    sets: List[Set]

# Resolve forward references in Variation (for the Parallel type)
Variation.update_forward_refs()

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
