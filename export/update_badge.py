#!/usr/bin/env python3
import os
import json

# Load the card counts from the JSON file
with open("card_counts.json", "r", encoding="utf-8") as f:
    counts = json.load(f)

# List of sports for which badges will be generated
target_sports = ["baseball", "football", "basketball", "hockey"]

# Ensure the badge output directory exists
os.makedirs("badge", exist_ok=True)

# Template for the SVG badge
def generate_badge_svg(sport, count):
    # Adjust width based on content if needed; here we use fixed values
    svg_template = f'''<svg xmlns="http://www.w3.org/2000/svg" width="150" height="20">
  <linearGradient id="b" x2="0" y2="100%">
    <stop offset="0" stop-color="#bbb" stop-opacity=".1"/>
    <stop offset="1" stop-opacity=".1"/>
  </linearGradient>
  <mask id="a">
    <rect width="150" height="20" rx="3" fill="#fff"/>
  </mask>
  <g mask="url(#a)">
    <rect width="80" height="20" fill="#555"/>
    <rect x="80" width="70" height="20" fill="#4c1"/>
    <rect width="150" height="20" fill="url(#b)"/>
  </g>
  <g fill="#fff" text-anchor="middle" font-family="Verdana" font-size="11">
    <text x="40" y="14">{sport.capitalize()}</text>
    <text x="115" y="14">{count}</text>
  </g>
</svg>'''
    return svg_template

# Generate an SVG badge for each sport and write it to a file
for sport in target_sports:
    count = counts.get(sport, 0)
    svg_content = generate_badge_svg(sport, count)
    badge_path = os.path.join("badge", f"{sport}.svg")
    with open(badge_path, "w", encoding="utf-8") as svg_file:
        svg_file.write(svg_content)
    print(f"Badge for {sport} updated with count: {count}")
