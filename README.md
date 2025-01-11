# Baseball Card JSON Repository

This repository contains comprehensive card lists for various baseball card sets in structured JSON format. Our goal is to provide a readily accessible and open-source database for use in applications, games, or personal projects involving baseball cards, without relying on SaaS or API providers.

## Why This Repository?

There is currently a lack of readily available, open datasets for baseball cards that developers can use without being tied to a specific API or SaaS provider. By offering these JSON files under an open-source license, we aim to fill this gap and enable developers to:

- Build apps or tools around baseball cards.
- Create offline applications without network dependencies.
- Have complete control over the dataset and how it is used.

## Repository Structure

The repository is organized by sets. Each set is represented by a JSON file with the following structure:

```json
{
  "Number": "97",
  "Name": "Jose Canseco",
  "Variations": [
    {
      "Variation": "Factory Set",
      "Note": "Reverse back facing right"
    }
  ]
}
```

- **Number**: The unique number assigned to the card within the set.
- **Name**: The name of the player featured on the card.
- **Variations**: An array of variations of the card.
  - **Variation**: The specific variation name/description
  - **Note**: Additional information about the variation.
- **Attributes:** An array of acronyms describing card attributes ("RC" for Rookie Card, etc.)

## License

All JSON files in this repository are licensed under the MIT License. You are free to use, modify, and distribute this data as long as the original license is retained.

## How to Contribute

We welcome contributions to improve and expand the dataset. Here’s how you can contribute:

1. Fork this repository.
2. Add or update a card set in the appropriate JSON format.
3. Submit a pull request with a detailed description of your changes.

Please ensure your contributions adhere to the following guidelines:

- Use consistent formatting as shown in the example.
- Verify the accuracy of the card data.

## Contact

If you have any questions or suggestions, feel free to open an issue or reach out via GitHub.

Thank you for supporting this open-source project!