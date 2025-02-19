# Sports Cards JSON Repository
[![Baseball Cards](badge/baseball.svg)](badge/baseball.svg)  [![Football Cards](badge/football.svg)](badge/football.svg)  [![Basketball Cards](badge/basketball.svg)](badge/basketball.svg)  [![Hockey Cards](badge/hockey.svg)](badge/hockey.svg)

Welcome to the Sports Cards JSON Repository, your ultimate destination for exploring sports card data in a structured and open-source format. This repository features comprehensive datasets for baseball cards and aims to expand to include football, hockey, and more. Developers, collectors, and enthusiasts alike can use this resource to power their projects such as: 
* Integrating a Baseball Card database into your Mobile or Web Application
* Providing datasets for a Machine Learning model
* Using them as checklists for your own personal collection

## Why This Repository?

The Sports Cards JSON Repository addresses the gap in freely accessible, high-quality sports card datasets. By providing open data, we empower developers to:

- Create innovative tools for sports card collectors.
- Develop offline applications for managing and analyzing card collections.
- Use structured data for building machine learning models or generating insights.

Whether you're working on a trading card tracker, a sports card price guide, or exploring trends in sports memorabilia, this repository offers a solid foundation.

## Repository Structure

The repository is organized by sports and card sets. Each set is represented by a JSON file that adheres to our schema. Below is an example of the structure:

```json
{
  "name": "Baseball Cards 1990",
  "attributes": [
    {
      "attribute": "Rookie Card",
      "note": "First appearance of player"
    }
  ],
  "sets": [
    {
      "name": "Factory Set",
      "notes": ["Complete set included"],
      "numberedTo": 1000,
      "variations": [
        {
          "variation": "Reverse Back",
          "note": "Reverse back facing right"
        }
      ],
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

Key fields include:

- **name**: The name of the card list or set.
- **attributes**: General properties (e.g., "Rookie Card") with additional notes.
- **notes**: Optional notes that provide extra context at the card list or set level.
- **sets**: Detailed information about specific card sets.
  - **numberedTo**: (Optional) The maximum number for cards in the set.
  - **insertOdds**: (Optional) An array of objects specifying insert odds.
  - **variations**: Differences within a set, such as misprints or unique designs.
  - **parallels**: Limited edition versions with unique numbering or designs.
- **cards**: Individual cards with their attributes, variations, and parallels.

## Language Examples

The `src` folder contains example code for loading and processing the JSON files:

| Language       | Example File            |
| -------------- | ----------------------- |
| **C#**         | `src/csharp/Program.cs` |
| **Python**     | `src/python/main.py`    |
| **Go**         | `src/go/main.go`        |
| **TypeScript** | `src/ts/index.ts`       |
| **Rust**       | `src/rust/main.rs`      |

These examples demonstrate how to parse JSON data and work with it effectively, making it easier to build applications or tools for collectors and developers.

## License

All JSON files in this repository are licensed under the MIT License. This ensures you can freely use, modify, and distribute the data while retaining proper attribution.

## How to Contribute

We welcome contributions to expand and enhance this repository. To contribute:

1. Fork this repository.
2. Add or update a card set in JSON format.
3. Ensure your JSON complies with the provided JSON schema.
4. Submit a pull request with a description of your changes.

All pull requests are validated using ajv-cli to ensure JSON files meet schema requirements. Validation must pass for the request to be merged.

Guidelines for contributors:

- Use consistent formatting as shown in the examples.
- Double-check the accuracy of card data.

## Contact

For questions or suggestions, feel free to open an issue or reach out through GitHub.

By supporting this project, you’re contributing to a comprehensive resource for sports card data enthusiasts, developers, and collectors alike.
