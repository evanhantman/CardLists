package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"os"
)

// AttributeItem represents an attribute for a card.
type AttributeItem struct {
	Attribute string `json:"attribute"`
	Note      string `json:"note"`
}

// InsertOdd represents the odds information.
type InsertOdd struct {
	Product string `json:"product"`
	Odds    string `json:"odds"`
}

// Variation represents a variation applicable to a set or card.
type Variation struct {
	Variation  string      `json:"variation"`
	Note       *string     `json:"note,omitempty"`
	InsertOdds []InsertOdd `json:"insertOdds,omitempty"`
	Parallels  []Parallel  `json:"parallels,omitempty"`
}

// Parallel represents a parallel version of a set or card.
type Parallel struct {
	Name       string      `json:"name"`
	NumberedTo *int        `json:"numberedTo,omitempty"`
	Notes      []string    `json:"notes,omitempty"`
	InsertOdds []InsertOdd `json:"insertOdds,omitempty"`
}

// Card represents an individual card.
type Card struct {
	Number     *string     `json:"number,omitempty"`
	Name       string      `json:"name"`
	Attributes []string    `json:"attributes,omitempty"`
	Note       *string     `json:"note,omitempty"`
	Variations []Variation `json:"variations,omitempty"`
	Parallels  []Parallel  `json:"parallels,omitempty"`
}

// Set represents a set of cards.
type Set struct {
	Name       string      `json:"name"`
	Notes      []string    `json:"notes,omitempty"`
	NumberedTo *int        `json:"numberedTo,omitempty"`
	InsertOdds []InsertOdd `json:"insertOdds,omitempty"`
	Variations []Variation `json:"variations,omitempty"`
	Parallels  []Parallel  `json:"parallels,omitempty"`
	Cards      []Card      `json:"cards"`
}

// CardList represents the root JSON object.
type CardList struct {
	Name       string          `json:"name"`
	Notes      []string        `json:"notes,omitempty"`
	Attributes []AttributeItem `json:"attributes,omitempty"`
	Sets       []Set           `json:"sets"`
}

func main() {
	if len(os.Args) != 2 {
		fmt.Println("Usage: go run main.go <path-to-json-file>")
		return
	}

	filePath := os.Args[1]

	// Read the JSON file.
	data, err := ioutil.ReadFile(filePath)
	if err != nil {
		fmt.Printf("Error reading file: %v\n", err)
		return
	}

	// Parse the JSON data.
	var root CardList
	err = json.Unmarshal(data, &root)
	if err != nil {
		fmt.Printf("Error parsing JSON: %v\n", err)
		return
	}

	// Print the parsed data in a pretty format.
	output, err := json.MarshalIndent(root, "", "  ")
	if err != nil {
		fmt.Printf("Error formatting JSON: %v\n", err)
		return
	}

	fmt.Println("JSON file loaded and validated successfully!")
	fmt.Println(string(output))
}
