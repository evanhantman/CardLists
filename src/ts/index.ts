import * as fs from 'fs';
import * as path from 'path';

// Interfaces based on the schema

interface AttributeItem {
    attribute: string;
    note: string;
}

interface Variation {
    variation: string;
    note?: string;
}

interface Parallel {
    name: string;
    of?: number;
    notes: string[];
}

interface Card {
    number?: string;
    name: string;
    attributes?: string[];
    note?: string;
    variations?: Variation[];
    parallels?: Parallel[];
}

interface Set {
    name: string;
    notes: string[];
    variations?: Variation[];
    parallels?: Parallel[];
    cards: Card[];
}

interface CardList {
    attributes?: AttributeItem[];
    sets: Set[];
}

// Function to load and parse the JSON file
function loadJsonFile(filePath: string): CardList | null {
    try {
        const absolutePath = path.resolve(filePath);
        const fileContent = fs.readFileSync(absolutePath, 'utf-8');
        const data: CardList = JSON.parse(fileContent);

        console.log("JSON file loaded successfully!");
        console.log(JSON.stringify(data, null, 4));

        return data;
    } catch (error) {
        console.error("Error loading or parsing JSON:", error.message);
        return null;
    }
}

// Main function
function main() {
    const args = process.argv.slice(2);
    if (args.length !== 1) {
        console.log("Usage: ts-node index.ts <path-to-json-file>");
        return;
    }

    const filePath = args[0];
    loadJsonFile(filePath);
}

// Run the main function
main();
