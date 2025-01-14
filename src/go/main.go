package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"os"
)

// Struct definitions based on the schema

type AttributeItem struct {
	Attribute string `json:"attribute"`
	Note      string `json:"note"`
}

type Variation struct {
	Variation string  `json:"variation"`
	Note      *string `json:"note,omitempty"`
}

type Parallel struct {
	Name string  `json:"name"`
	Of   *int    `json:"of,omitempty"`
	Notes []string `json:"notes"`
}

type Card struct {
	Number     *string     `json:"number,omitempty"`
	Name       string      `json:"name"`
	Attributes []string    `json:"attributes,omitempty"`
	Note       *string     `json:"note,omitempty"`
	Variations []Variation `json:"variations,omitempty"`
	Parallels  []Parallel  `json:"parallels,omitempty"`
}

type Set struct {
	Name       string      `json:"name"`
	Notes      []string    `json:"notes"`
	Variations []Variation `json:"variations,omitempty"`
	Parallels  []Parallel  `json:"parallels,omitempty"`
	Cards      []Card      `json:"cards"`
}

type CardList struct {
	Name       string      `json:"name"`
	Attributes []AttributeItem `json:"attributes,omitempty"`
	Sets       []Set           `json:"sets"`
}

func main() {
	if len(os.Args) != 2 {
		fmt.Println("Usage: go run main.go <path-to-json-file>")
		return
	}

	filePath := os.Args[1]

	// Read the JSON file
	data, err := ioutil.ReadFile(filePath)
	if err != nil {
		fmt.Printf("Error reading file: %v\n", err)
		return
	}

	// Parse the JSON data
	var root CardList
	err = json.Unmarshal(data, &root)
	if err != nil {
		fmt.Printf("Error parsing JSON: %v\n", err)
		return
	}

	// Print the parsed data in a pretty format
	output, err := json.MarshalIndent(root, "", "  ")
	if err != nil {
		fmt.Printf("Error formatting JSON: %v\n", err)
		return
	}

	fmt.Println("JSON file loaded and validated successfully!")
	fmt.Println(string(output))
}
