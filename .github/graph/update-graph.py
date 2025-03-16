#!/usr/bin/env python3
import os
import json
import matplotlib.pyplot as plt

# List of sports for which graphs will be generated
target_sports = ["baseball", "football", "basketball", "hockey"]

# Ensure the output directory for badges exists
badge_dir = os.path.join(".github", "badge")
os.makedirs(badge_dir, exist_ok=True)

# Process each sport's category JSON file to generate a bar graph
for sport in target_sports:
    category_file = os.path.join("categories", f"{sport}.json")
    try:
        with open(category_file, "r", encoding="utf-8") as f:
            category_data = json.load(f)
    except Exception as e:
        print(f"Error loading category file for {sport}: {e}")
        continue

    # Extract the years array from the JSON structure
    years_data = category_data.get("category", {}).get("years", [])
    
    # Calculate the percentage of indexed releases per year
    indexed_percentages = {}
    for entry in years_data:
        try:
            # Extract the first 4 characters to get the year (e.g., "2001" from "2001-02")
            year_str = entry.get("year", "")[:4]
            year = int(year_str)
        except ValueError:
            continue
        
        releases = entry.get("releases", [])
        total = len(releases)
        if total == 0:
            percent = 0.0
        else:
            indexed_count = sum(1 for r in releases if r.get("indexed", False))
            percent = (indexed_count / total) * 100
        indexed_percentages[year] = percent

    if not indexed_percentages:
        print(f"No valid year data found for {sport}. Skipping graph generation.")
        continue

    # Determine the full range of years to be represented on the graph
    min_year = min(indexed_percentages.keys())
    max_year = max(indexed_percentages.keys())
    all_years = list(range(min_year, max_year + 1))
    percentages = [indexed_percentages.get(year, 0.0) for year in all_years]

    # Create the bar graph with dimensions 600x120 pixels (6 inches wide x 1.2 inches tall at 100 DPI)
    fig, ax = plt.subplots(figsize=(6, 1.2), dpi=100)
    ax.bar(all_years, percentages, width=0.8, align='center', color='green')
    ax.set_ylim(0, 100)
    ax.set_xlabel("Year")
    ax.set_ylabel("% Indexed")
    ax.set_title(f"{sport.capitalize()} Sets Indexed")
    ax.set_xticks(all_years)
    
    # Rotate the x-tick labels 90 degrees for readability in the narrow layout
    plt.xticks(rotation=90)

    # Save the bar graph image
    plt.tight_layout()
    bar_graph_path = os.path.join(badge_dir, f"{sport}_bar.png")
    plt.savefig(bar_graph_path)
    plt.close(fig)
    print(f"Bar graph for {sport} generated at {bar_graph_path}")
