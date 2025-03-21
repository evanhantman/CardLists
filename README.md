# JunkWaxData - Sports Cards JSON Repository

## Comprehensive Database for Collectors and Developers

[![Baseball Cards Indexed](.github/badge/baseball.svg)](.github/badge/baseball.svg) [![Football Cards Indexed](.github/badge/football.svg)](.github/badge/football.svg) [![Basketball Cards Indexed](.github/badge/basketball.svg)](.github/badge/basketball.svg) [![Hockey Cards Indexed](.github/badge/hockey.svg)](badge/hockey.svg)
[![Baseball Cards Indexed Graph](.github/graph/baseball_bar.png)](.github/graph/baseball_bar.png)

Welcome to the Sports Cards JSON Repository, your ultimate destination for exploring sports card data in a structured and open-source format. This repository features comprehensive datasets for baseball cards, football cards, basketball cards, and hockey cards in a developer-friendly JSON format. Collectors, developers, and enthusiasts can use this resource to power their projects such as:

* Integrating a complete sports card database into web applications
* Building mobile apps with powerful search across MLB, NFL, NBA, and NHL card collections
* Training machine learning models on structured sports memorabilia data
* Managing personal card collections with accurate checklists

## Why This Repository?

The Sports Cards JSON Repository addresses the gap in freely accessible, high-quality sports card datasets. By providing open data, we empower developers to:

* Create innovative tools for sports card collectors
* Develop offline applications for managing and analyzing card collections
* Use structured data for building machine learning models or generating insights
* Access comprehensive metadata about card sets across multiple sports

Whether you're working on a trading card tracker, a sports card price guide, or exploring trends in sports memorabilia, this repository offers a solid foundation.

## Repository Structure

The repository is organized by sports categories with releases organized by year:

```text
Sports Cards JSON Repository
├── categories/                    # Sport Categories
│   ├── baseball.json              # Baseball Category metadata
│   ├── football.json              # Football Category metadata 
│   ├── basketball.json            # Basketball Category metadata
│   ├── hockey.json                # Hockey Category metadata
|   ├── football/                  # Football Card Releases
│   ├── basketball/                # Basketball Card Releases
│   ├── hockey/                    # Hockey Card Releases
│   └── baseball/                  # Baseball Card Release
│       ├── 1990/                  # 1990 Baseball Releases
│       │   ├── 1990-Topps.json    # 1990 Topps Baseball Release
│       │   └── ...
│       └── ...
├── schemas/                       # JSON schemas for validation
│   ├── category.json              # Schema for Category files
│   └── release.json               # Schema for Card Releases
├── scripts/                       # Python Utility Scripts
└── examples/                      # Example code implementations
    ├── csharp/                    # C# examples
    ├── python/                    # Python examples
    ├── go/                        # Go examples
    ├── ts/                        # TypeScript examples
    └── rust/                      # Rust examples
```

## Data Schema Structure

### Category Files

Each sport has a category file (e.g., `baseball.json`) defining available years and releases:

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "category": {
    "name": "Baseball Cards",
    "years": [
      {
        "year": "1990",
        "releases": [
          {
            "name": "Topps Baseball",
            "indexed": true,
            "version": "1.0",
            "uniqueId": "550e8400-e29b-41d4-a716-446655440000"
          },
          {
            "name": "Upper Deck Baseball",
            "indexed": false
          }
        ]
      },
      {
        "year": "1991",
        "releases": [
          {
            "name": "Donruss Baseball",
            "indexed": false
          }
        ]
      }
    ]
  }
}
```

### Card Release Files

Individual card set releases follow this structure:

```json
{
  "name": "Topps Baseball",
  "version": "1.0",
  "uniqueId": "550e8400-e29b-41d4-a716-446655440000",
  "attributes": [
    {
      "attribute": "RC",
      "note": "Rookie Card"
    }
  ],
  "sets": [
    {
      "name": "Factory Set",
      "uniqueId": "ff789858-390c-4cb4-bbae-29bb501d91b3",
      "notes": ["Complete set included"],
      "numberedTo": 1000,
      "parallels": [
        {
          "name": "Gold Edition",
          "numberedTo": 1000,
          "notes": ["Limited edition release"]
        }
      ],
      "cards": [
        {
          "number": "97",
          "uniqueId": "958bd99d-a01f-49d6-979f-154d7675142b",
          "name": "Jose Canseco",
          "attributes": ["RC"],
          "note": "Star player",
          "variations": [
            {
              "variation": "Error Card",
              "note": "Misprint on back"
            }
          ],
          "parallels": [
            {
              "name": "Gold Edition",
              "numberedTo": 1000,
              "notes": ["Serial numbered"]
            }
          ]
        }
      ]
    }
  ]
}
```

## Key Fields

### Category Files

* **name**: The sport category name (e.g., "baseball")
* **years**: Array of year objects containing releases
  * **year**: Year in YYYY or YYYY-YY format (e.g., "1990" or "1990-91")
  * **releases**: Array of card releases for that year
    * **name**: Release name
    * **indexed**: Boolean indicating if this release is fully indexed
    * **version**: (Optional) Version of the data
    * **uniqueId**: (Optional) UUID for the release

### Release Files

* **name**: The name of the card list or set
* **attributes**: General properties (e.g., "Rookie Card") with additional notes
* **notes**: Optional notes providing extra context at the card list or set level
* **sets**: Detailed information about specific card sets
  * **numberedTo**: (Optional) The maximum number for cards in the set
  * **insertOdds**: (Optional) An array of objects specifying insert odds
  * **variations**: Differences within a set, such as misprints or unique designs
  * **parallels**: Limited edition versions with unique numbering or designs
* **cards**: Individual cards with their attributes, variations, and parallels

## Code Examples

The `examples` folder contains example code for loading and processing the JSON files:

| Language       | Example File            | Use Case |
| -------------- | ----------------------- | -------- |
| **C#**         | `examples/csharp/Program.cs` | .NET applications, desktop collectors' tools |
| **Python**     | `examples/python/main.py`    | Data analysis, web scrapers for card data |
| **Go**         | `examples/go/main.go`        | High-performance card search APIs |
| **TypeScript** | `examples/ts/index.ts`       | Web-based card collection managers |
| **Rust**       | `examples/rust/main.rs`      | Performance-critical card data processing |

These examples demonstrate how to parse JSON data and work with it effectively, making it easier to build applications or tools for collectors and developers.

## License

All JSON files in this repository are licensed under the MIT License. This ensures you can freely use, modify, and distribute the data while retaining proper attribution.

## How to Contribute

We welcome contributions to expand and enhance this repository. 

To contribute:

1. Read our handy [HOWTO](HOWTO.md) on creating your own JSON Releases
2. Fork this repository
3. Add or update a card set in JSON format
4. Ensure your JSON complies with the provided JSON schemas
5. Submit a pull request with a description of your changes

All pull requests are validated against our JSON schemas to ensure data consistency. Validation must pass for the request to be merged.

Guidelines for contributors:

* Use consistent formatting as shown in the examples
* Double-check the accuracy of card data
* Include complete set information where possible
* Add appropriate metadata to help with searchability

## Contact

For questions or suggestions about our sports card database, feel free to open an issue or reach out through GitHub.

By supporting this project, you're contributing to a comprehensive resource for sports card data enthusiasts, developers, and collectors alike.
