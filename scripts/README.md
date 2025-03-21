# JSONCardLists Scripts

This folder contains several Python scripts that perform various operations on JSON card lists to help automate their creation and help with some of the more tedious tasks. Below is a brief description of each script:

## Scripts

### add-category-uid.py
This script adds a unique identifier (UID) to each Release in a given Category definition JSON file (`baseball.json`, `football.json`, etc.). This is handy when creating a new Category, allowing you to generate a full valid JSON document and then use this tool
to come in behind you and automatically generate all the `uniqueId` properties on each release.

**Syntax**:
`python add-category-uid.py <JSON file to process>`

**Example**:
`python add-uid.py ../categories/baseball.json`

### add-uid.py
This script adds a unique identifier (UID) to each Card and Set in the a Release JSON (`2004-Topps.json` for example). As with the above script, this script helps in filling in all the `uniqueId` fields within a Release JSON document for both the `sets` and `cards`, saving you the time from having to generate these values when creating a Release JSON.

Syntax:
`python add-uid.py <path to process>`

Example:
`python add-uid.py ../categories/baseball/2024`

### build-parquet.py
This script takes all the JSON files in this repository and builds a parquet file containing all Categories/Releases/Sets/Cards defined in every JSON file. No parameters are passed into it, as it assumes the same directory structure of the repository and it will look in `../categories`.

Example:
`python build-parquet.py`

### propagate-release-uniqueId.py
This script propagates a unique release identifier to all relevant Relases. This is handy if you've added many new Releases to a category JSON file, and would like to automatically apply the Release `uniqueId` to each Release JSON file automatically.

Syntax:
`python propagate-release-uniqueId.py <Category JSON File>`

Example:
`python propagate-release-uniqueId.py ../categories/baseball.json`

### validate-json-data.py
This script validates the JSON card list to ensure it meets the required schema and data integrity constraints. The input parameter is a given Category path, and will treat all JSON files recursively in that path as the total dataset for analysis.

It will perform the following checks:  

- Verify all Attributes Defined on Cards within a Release JSON is in the `attributes` array for that Release
- Verify all defined Attributes in the `attributes` array in a JSON file appear in the `cards` for that Release
- Verify `attribute` definitions are the same across all files (For example, `"RC"` is `"Rookie Card"` across all JSON files)
- Provide you the JSON for the `attributes` array for a given file (helps when creating new files)
- Flags new `attributes` that require definitions

Syntax:
`python validate-json-data.py <Category Path>`

Example:
`python validate-json-data.py "categories/basketball/**/*.json"`

## Usage
To run any of these scripts, use the following command:
```
python script_name.py
```
Replace `script_name.py` with the name of the script you wish to execute.

## License
This project is licensed under the MIT License.

For more information, refer to the individual script files or contact the project maintainer.