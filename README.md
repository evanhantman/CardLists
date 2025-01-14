# Sports Cards JSON Dataset Repository ⚾🏈

This repository contains comprehensive card lists for various sports card sets in structured JSON format. While our initial focus is on baseball cards, we aim to expand the dataset to include football, hockey, and other sports in the future. Our goal is to provide a readily accessible and open-source database for use in applications, games, or personal projects involving sports cards, without relying on SaaS or API providers.

## Why This Repository?

There is currently a lack of readily available, open datasets for sports cards that developers can use without being tied to a specific API or SaaS provider. By offering these JSON files under an open-source license, we aim to fill this gap and enable developers to:

- Build apps or tools around sports cards.
- Create offline applications without network dependencies.
- Have complete control over the dataset and how it is used.

## Repository Structure

The repository is organized by sports and sets. Each set is represented by a JSON file with the following structure:

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
      "variations": [
        {
          "variation": "Reverse Back",
          "note": "Reverse back facing right"
        }
      ],
      "parallels": [
        {
          "name": "Gold Edition",
          "of": 1000,
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
              "of": 1000,
              "notes": ["Serial numbered"]
            }
          ]
        }
      ]
    }
  ]
}
```

- **name**: The name of the card set.
- **attributes**: General attributes of the set, such as "Rookie Card".
- **sets**: An array of sets included in the dataset.
  - **name**: The specific set name.
  - **notes**: Additional notes about the set.
  - **variations**: List of variations available in the set.
    - **variation**: The variation type.
    - **note**: Further description of the variation.
  - **parallels**: Array of parallel versions of the cards.
    - **name**: Name of the parallel version.
    - **of**: Total number of copies for the parallel.
    - **notes**: Additional notes about the parallel.
  - **cards**: An array of individual cards in the set.
    - **number**: The unique card number.
    - **name**: Player's name.
    - **attributes**: Specific attributes related to the card.
    - **note**: Additional information about the card.
    - **variations**: List of variations specific to the card.
    - **parallels**: Parallel versions of the card.

## Language Examples

In the `src` folder, we provide example code in various languages to demonstrate how to load and work with the JSON files:

| Language       | Example File            |
| -------------- | ----------------------- |
| **C#**         | `src/csharp/Program.cs` |
| **Python**     | `src/python/main.py`    |
| **Go**         | `src/go/main.go`        |
| **TypeScript** | `src/ts/index.ts`       |

These examples show how to parse the JSON files and access card data in each respective language.

## License

All JSON files in this repository are licensed under the MIT License. You are free to use, modify, and distribute this data as long as the original license is retained.

## How to Contribute

We welcome contributions to improve and expand the dataset. Here’s how you can contribute:

1. Fork this repository.
2. Add or update a card set in the appropriate JSON format.
3. Ensure your JSON file is compliant with our `schema.json` file.
4. Submit a pull request with a detailed description of your changes.

Please note that all pull requests must pass the validation build action, which uses **ajv-cli** to validate the JSON files against our `schema.json`. If your JSON file does not pass validation, the pull request will not be accepted.

Please ensure your contributions adhere to the following guidelines:

- Use consistent formatting as shown in the example.
- Verify the accuracy of the card data.

## Contact

If you have any questions or suggestions, feel free to open an issue or reach out via GitHub.

Thank you for supporting this open-source project!