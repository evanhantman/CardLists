use serde::{Deserialize, Serialize};
use std::env;
use std::fs;
use std::process;

#[derive(Debug, Serialize, Deserialize)]
pub struct CardList {
    pub name: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub notes: Option<Vec<String>>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub attributes: Option<Vec<AttributeItem>>,
    pub sets: Vec<Set>,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct AttributeItem {
    pub attribute: String,
    pub note: String,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct Set {
    pub name: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub notes: Option<Vec<String>>,
    #[serde(rename = "numberedTo", skip_serializing_if = "Option::is_none")]
    pub numbered_to: Option<u32>,
    #[serde(rename = "insertOdds", skip_serializing_if = "Option::is_none")]
    pub insert_odds: Option<Vec<InsertOdd>>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub variations: Option<Vec<Variation>>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub parallels: Option<Vec<Parallel>>,
    pub cards: Vec<Card>,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct InsertOdd {
    pub product: String,
    pub odds: String,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct Variation {
    pub variation: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub note: Option<String>,
    #[serde(rename = "insertOdds", skip_serializing_if = "Option::is_none")]
    pub insert_odds: Option<Vec<InsertOdd>>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub parallels: Option<Vec<Parallel>>,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct Parallel {
    pub name: String,
    #[serde(rename = "numberedTo", skip_serializing_if = "Option::is_none")]
    pub numbered_to: Option<u32>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub notes: Option<Vec<String>>,
    #[serde(rename = "insertOdds", skip_serializing_if = "Option::is_none")]
    pub insert_odds: Option<Vec<InsertOdd>>,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct Card {
    #[serde(skip_serializing_if = "Option::is_none")]
    pub number: Option<String>,
    pub name: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub attributes: Option<Vec<String>>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub note: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub variations: Option<Vec<Variation>>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub parallels: Option<Vec<Parallel>>,
}

fn main() {
    // Expect exactly one command-line argument: the path to the JSON file.
    let args: Vec<String> = env::args().collect();
    if args.len() != 2 {
        eprintln!("Usage: {} <path-to-json-file>", args[0]);
        process::exit(1);
    }
    let file_path = &args[1];

    // Read the file into a string.
    let file_content = fs::read_to_string(file_path).unwrap_or_else(|err| {
        eprintln!("Error reading file '{}': {}", file_path, err);
        process::exit(1);
    });

    // Parse the JSON file into the CardList struct.
    let card_list: CardList = serde_json::from_str(&file_content).unwrap_or_else(|err| {
        eprintln!("Error parsing JSON: {}", err);
        process::exit(1);
    });

    println!("JSON file loaded and validated successfully!");

    // Pretty-print the parsed data.
    let output = serde_json::to_string_pretty(&card_list).unwrap();
    println!("{}", output);
}
