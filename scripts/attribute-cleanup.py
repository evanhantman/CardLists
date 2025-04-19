import json
import os
import glob
import jsonschema
import copy
from urllib.parse import urlparse
from urllib.request import urlopen
import sys

def load_schema(schema_url):
    """Load schema from URL or local file."""
    try:
        parsed_url = urlparse(schema_url)
        if parsed_url.scheme in ('http', 'https'):
            with urlopen(schema_url) as response:
                return json.loads(response.read().decode('utf-8'))
        else:
            # Assume it's a local file
            with open(schema_url, 'r') as f:
                return json.load(f)
    except Exception as e:
        print(f"Error loading schema {schema_url}: {e}")
        return None

def detect_indentation(file_path):
    """Detect indentation in JSON file."""
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Find the first indented line
    lines = content.split('\n')
    for line in lines:
        if line.startswith(' ') or line.startswith('\t'):
            # Count leading spaces or tabs
            indent = ''
            for char in line:
                if char in (' ', '\t'):
                    indent += char
                else:
                    break
            return indent
    
    # Default to 2 spaces if no indentation detected
    return '  '

def process_file(file_path):
    """Process a single JSON file."""
    print(f"Processing {file_path}")
    
    # Detect indentation
    indent_str = detect_indentation(file_path)
    
    try:
        # Load JSON file
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        # Skip if no schema defined
        if '$schema' not in data:
            print(f"  No schema defined in {file_path}, skipping")
            return False
        
        # Load and validate schema
        schema = load_schema(data['$schema'])
        if not schema:
            print(f"  Failed to load schema for {file_path}, skipping")
            return False
        
        try:
            jsonschema.validate(instance=data, schema=schema)
        except jsonschema.exceptions.ValidationError as e:
            print(f"  JSON validation failed for {file_path}: {e}")
            return False
        
        # Create a copy of the data for modification
        modified_data = copy.deepcopy(data)
        modified = False
        
        # Process each set
        for set_idx, card_set in enumerate(data.get('sets', [])):
            # Skip sets with no cards
            if 'cards' not in card_set or not card_set['cards']:
                continue
            
            # Find common attributes across all cards in the set
            common_attributes = None
            for card in card_set['cards']:
                if 'attributes' not in card:
                    # If any card doesn't have attributes, there can't be common ones
                    common_attributes = None
                    break
                
                if common_attributes is None:
                    # Initialize with the first card's attributes
                    common_attributes = set(card['attributes'])
                else:
                    # Intersect with this card's attributes
                    common_attributes &= set(card['attributes'])
            
            # If common attributes found, move them to set level
            if common_attributes and common_attributes:
                common_attributes = sorted(list(common_attributes))
                
                # Add attributes to set if not already present
                if 'attributes' not in modified_data['sets'][set_idx]:
                    modified_data['sets'][set_idx]['attributes'] = common_attributes
                else:
                    # Merge with existing set attributes
                    existing = set(modified_data['sets'][set_idx]['attributes'])
                    for attr in common_attributes:
                        if attr not in existing:
                            modified_data['sets'][set_idx]['attributes'].append(attr)
                
                # Remove common attributes from each card
                for card_idx, card in enumerate(modified_data['sets'][set_idx]['cards']):
                    if 'attributes' in card:
                        card['attributes'] = [attr for attr in card['attributes'] if attr not in common_attributes]
                        if not card['attributes']:
                            del card['attributes']
                
                modified = True
                print(f"  Moved {len(common_attributes)} common attributes to set level in set '{card_set['name']}'")
        
        # Save the modified file if changes were made
        if modified:
            # Validate the modified data against the schema before saving
            try:
                jsonschema.validate(instance=modified_data, schema=schema)
            except jsonschema.exceptions.ValidationError as e:
                print(f"  Modified JSON failed validation for {file_path}: {e}")
                print(f"  Skipping modifications to avoid breaking the file")
                return False
            
            # Preserve the original formatting
            with open(file_path, 'w') as f:
                json.dump(modified_data, f, indent=indent_str)
            print(f"  Successfully updated {file_path}")
            return True
        else:
            print(f"  No changes needed for {file_path}")
            return False
            
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

def process_directory(directory_path):
    """Process all JSON files in directory and subdirectories."""
    print(f"Scanning directory: {directory_path}")
    
    # Get all JSON files in directory and subdirectories
    json_files = glob.glob(os.path.join(directory_path, '**', '*.json'), recursive=True)
    
    success_count = 0
    total_count = len(json_files)
    
    for file_path in json_files:
        if process_file(file_path):
            success_count += 1
    
    print(f"\nProcessed {total_count} JSON files, modified {success_count} files")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py <directory_path>")
        sys.exit(1)
    
    directory_path = sys.argv[1]
    if not os.path.isdir(directory_path):
        print(f"Error: {directory_path} is not a valid directory")
        sys.exit(1)
    
    process_directory(directory_path)