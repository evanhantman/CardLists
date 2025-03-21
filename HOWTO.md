# How to create a new Card List JSON File

## Step 1 - Creating the Release File

The easiest way to start a new Release JSON file is to start with a simple, blank template such as this:

```json
{
    "$schema": "https://raw.githubusercontent.com/JunkWaxData/CardLists/refs/heads/main/schemas/release.json",
    "name": "1900 Generic Baseball",
    "version": "1.0",
    "uniqueId": "00000000-0000-0000-0000-000000000000",
    "attributes": [],
    "sets": []
}
```

The fields you'll need to fill in manually:

* `name`: The format of your Release JSON should be `<year> <release name> <category>` with examples being:
  * `1990 Topps Baseball`
  * `2001-2002 O-Pee-Chee Hockey`
* `version`: The initial version should be `1.0`
*`uniqueId`: You can fill this in now with a valid GUID (you can generate one here), or it can be filled in later using one of the utility scripts.

## Step 2 - Generating the Card List

For the release you're creating, it must have at least one `set` defined in the `sets` array. For Releases with only one Base Set of cards, the value we've been using for the default is `Base Set`.

```json
{
    "$schema": "https://raw.githubusercontent.com/JunkWaxData/CardLists/refs/heads/main/schemas/release.json",
    "name": "1900 Generic Baseball",
    "version": "1.0",
    "uniqueId": "00000000-0000-0000-0000-000000000000",
    "attributes": [],
    "sets": [
        {
            "name": "Base Set",
            "cards" []
        }
    ]
}
```

To generate the list of `cards` that go into a set, you can manually create the JSON for the `card` objects, or use a tool such as the Custom GPT we've created to help convert unstructured list of Sports Cards into `card` objects. You can access the custom GPT here: [JunkWaxData Card List Parser (ChatGPT)](https://chatgpt.com/g/g-67827e2827908191a6c84def26bfd9c4-junkwaxdata-card-list-parser)

The Custom GPT we've put together will accept a plaintext checklist of cards with a format of "<number> <name> <attributes>" which is the most common format we could find on the internet. An example list of cards used by the Custom GPT would be:

```
165 Jeff Reardon
166 Bob Boone
167 Jim Deshaies
168 Lou Piniella
169 Ron Washington
170 Bo Jackson RC
171 Chuck Cary
172 Ron Oester
173 Alex Trevino
174 Henry Cotto
175 Bob Stanley 
```

The JunkWaxData Custom GPT will convert this list to:

```json
[
    {"name":"Jeff Reardon","number":"165"},
    {"name":"Bob Boone","number":"166"},
    {"name":"Jim Deshaies","number":"167"},
    {"name":"Lou Piniella","number":"168"},
    {"name":"Ron Washington","number":"169"},
    {"name":"Bo Jackson","number":"170","attributes":["RC"]},
    {"name":"Chuck Cary","number":"171"},
    {"name":"Ron Oester","number":"172"},
    {"name":"Alex Trevino","number":"173"},
    {"name":"Henry Cotto","number":"174"},
    {"name":"Bob Stanley","number":"175"}
]

```

Why use AI? Because a lot of card lists have the attributes or extra card data in a single line, and it's more accurate to have the LLM determine the players name, and differentiate between that and any additional information in the card record.

For sets where there are variations for the entire set (commonly Chrome, Gold, Foil, etc.), where every card in the enumerated set has a variation, you can define these at the `set` level as a `parallel`:

```json
{
    "$schema": "https://raw.githubusercontent.com/JunkWaxData/CardLists/refs/heads/main/schemas/release.json",
    "name": "1900 Generic Baseball",
    "version": "1.0",
    "uniqueId": "00000000-0000-0000-0000-000000000000",
    "attributes": [],
    "sets": [
        {
            "name": "Base Set",
            "parallels":[
                {
                    "name": "Gold",
                    "numberedTo": 100
                }
            ]
            "cards" [
                    {"name":"Jeff Reardon","number":"165"},
                    {"name":"Bob Boone","number":"166"},
                    {"name":"Jim Deshaies","number":"167"},
                    {"name":"Lou Piniella","number":"168"},
                    {"name":"Ron Washington","number":"169"},
                    {"name":"Bo Jackson","number":"170","attributes":["RC"]},
                    {"name":"Chuck Cary","number":"171"},
                    {"name":"Ron Oester","number":"172"},
                    {"name":"Alex Trevino","number":"173"},
                    {"name":"Henry Cotto","number":"174"},
                    {"name":"Bob Stanley","number":"175"}
            ]
        }
    ]
}
```

For Insert Sets, where the card numbers differ from the Base Set, you can define this as an additional `set` in the `sets` array:

```json
{
    "$schema": "https://raw.githubusercontent.com/JunkWaxData/CardLists/refs/heads/main/schemas/release.json",
    "name": "1900 Generic Baseball",
    "version": "1.0",
    "uniqueId": "00000000-0000-0000-0000-000000000000",
    "attributes": [],
    "sets": [
        {
            "name": "Base Set",
            "parallels":[
                {
                    "name": "Gold",
                    "numberedTo": 100
                }
            ]
            "cards" [
                    {"name":"Jeff Reardon","number":"165"},
                    {"name":"Bob Boone","number":"166"},
                    {"name":"Jim Deshaies","number":"167"},
                    {"name":"Lou Piniella","number":"168"},
                    {"name":"Ron Washington","number":"169"},
                    {"name":"Bo Jackson","number":"170","attributes":["RC"]},
                    {"name":"Chuck Cary","number":"171"},
                    {"name":"Ron Oester","number":"172"},
                    {"name":"Alex Trevino","number":"173"},
                    {"name":"Henry Cotto","number":"174"},
                    {"name":"Bob Stanley","number":"175"}
            ]
        },
        {
            "name": "Rookies",
            "cards": []
        }
    ]
}
```

## Step 3 - Apply Unique ID's

Just like we have a `uniqueId` property on the release, we also apply `uniqueId` properties to the `set` and `card` objects. This provides several advantages, such as:

* Identifying a card across versions if the number, name, set, or even release changes between updates
* Tracking changes to a specific card, even if the number or name change
* Easily looking up a card (and all parallels/variations) in a flattened dataset

Because it would be cumbersome to do manually, we've provided some helper scripts to assist with these tasks. You can access them in our `/scripts` folder in this repository.

The Python Script `add-uid.py` can be used to automatically add `uniqueId` values to all `set` and `card` objects within the specified JSON file. You can execute the script using the following command line:

`python3 add-uid.py path/to/my/file/release.json`

## Step 4 - Create Attributes

Now that we have a JSON file that should pass JSON Schema validation (after adding the `uniqueId` fields), the next step is to create the `attributes` array for the Release, ensuring all attributes used by the `cards` in the JSON file are represented in the `attributes` array. Additionally, we want to ensure our `attributes` definitions are consistent across the entire category.

As with Unique ID's, we have a helper script that assists with ensuring the `attributes` used by your release JSON are accurate. You can use the script `validate-json-data.py` to assist with this. You can execute the script with the following command line:

`python3 validate-json-data.py path/to/my/category`

THe script will not just look at the new Release you've added, but also load every release in the category to ensure:

* All `attribute` values used on a `card` are represented in the `attributes` array
* All `attribute` values in the `attribute` array within a Release are used by at least one `card` in the Release
* All `attribute` values in the `attribute` array are defined consistently across the category

This means if you define `RC` to mean "Rookie Card" in the `baseball` category, it'll ensure it has the same definition in every file.

The reason we persist attributes in each JSON file is to ensure every JSON release file can be used consistently by itself, without having to rely on additional JSON files through relationship entities.

## Step 5 - Update the Category JSON File

For each Category in this repository, we define a JSON file for each one that tracks Releases and if they're indexed (included) in this repostiory. This has two main benefits:

1. Gives an exhaustive list of all _potentially_ available Releases in a given category
2. Informs the consumer if a Release is available without having first to check to see if a file exists

For your release, if there's an existing Release defined in the Category JSON file, please update that record:

Before:

```json
{
    "year": "1998",
    "releases": [
        {
            "name": "Bowman",
            "indexed": false
        }
    ]
}
```

After:

```json
{
    "year": "1998",
    "releases": [
        {
            "name": "Bowman",
            "version": "1.0",
            "uniqueId": "ffbd7ba9-d34d-4eae-98e4-0634586ec922",
            "indexed": true
        }
    ]
}
```

As you can see, we've added a `uniqueId` to the release. We can now manually add that `uniqueId` to our release, _or_ if we've created many new releases and we'd like this to be done automatically, we can use the script `add-category-uid.py` which will generate the `uniqueId` on any Release in a Category JSON file marked `true`, and propagate that `uniqueId` down to the JSON file for that Release as well.

## Step 5 - Open a Pull Request

After you've created your JSON file and you're ready to add it to the collection, Fork this Repository, add your code and open a full request! Automated checks will run on your PR to ensure the JSON is valid, passes Schema Validation, and also passes the same checks you can run via `validate-json-data.py`

We sincerely appreciate contributions from the community, as this is a free and open community project!