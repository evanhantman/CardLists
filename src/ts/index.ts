import * as fs from 'fs';
import * as path from 'path';

// Interfaces based on the updated JSON schema

interface AttributeItem {
    attribute: string;
    note: string;
}

interface InsertOdd {
    product: string;
    odds: string; // Should match the pattern /^[0-9]+:[0-9,]+$/
}

interface Variation {
    variation: string;
    note?: string;
    insertOdds?: InsertOdd[];
    parallels?: Parallel[];
}

interface Parallel {
    name: string;
    numberedTo?: number;  // Renamed from "of" to "numberedTo"
    notes?: string[];
    insertOdds?: InsertOdd[];
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
    notes?: string[];
    numberedTo?: number;
    insertOdds?: InsertOdd[];
    variations?: Variation[];
    parallels?: Parallel[];
    cards: Card[];
}

interface CardList {
    name: string;
    notes?: string[];
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
    } catch (error: any) {
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
