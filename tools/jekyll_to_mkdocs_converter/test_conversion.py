#!/usr/bin/env python3
# This script tests the conversion process for Gemini by Example to MkDocs
"""
Test script to verify that the conversion script can correctly load and
process the data.
"""

import json
from pathlib import Path


def load_json_data(file_path):
    """Load JSON data from a file."""
    with open(file_path, "r") as f:
        return json.load(f)


def main():
    """Main function to test the conversion process."""
    print("Testing conversion process...")

    # Check if the data files exist
    examples_path = "data/examples.json"
    sections_path = "data/sections.json"

    if not Path(examples_path).exists():
        print(f"Error: {examples_path} not found.")
        return 1

    if not Path(sections_path).exists():
        print(f"Error: {sections_path} not found.")
        return 1

    # Load the data
    try:
        examples_data = load_json_data(examples_path)
        sections_data = load_json_data(sections_path)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return 1
    except Exception as e:
        print(f"Error loading data: {e}")
        return 1

    # Print some basic information
    examples = examples_data.get("examples", [])
    sections = sections_data.get("sections", [])

    print(f"Found {len(examples)} examples and {len(sections)} sections.")

    # Print section information
    print("\nSections:")
    for section in sorted(sections, key=lambda s: s.get("order", 0)):
        section_id = section.get("id", "unknown")
        section_title = section.get("title", "unknown")
        section_examples = [e for e in examples if e.get("section_id") == section_id]
        print(f"  - {section_title} ({section_id}): {len(section_examples)} examples")

    # Print example information for the first section
    if sections:
        first_section = sorted(sections, key=lambda s: s.get("order", 0))[0]
        section_id = first_section.get("id", "unknown")
        section_title = first_section.get("title", "unknown")
        section_examples = [e for e in examples if e.get("section_id") == section_id]

        print(f"\nExamples in {section_title}:")
        for example in sorted(section_examples, key=lambda e: e.get("order", 0)):
            example_id = example.get("id", "unknown")
            example_title = example.get("title", "unknown")
            code_segments = example.get("code_segments", [])
            shell_segments = example.get("shell_segments", [])
            image_data = example.get("image_data", [])

            print(f"  - {example_title} ({example_id}):")
            print(f"    - {len(code_segments)} code segments")
            print(f"    - {len(shell_segments)} shell segments")
            print(f"    - {len(image_data)} images")

    print("\nTest completed successfully!")
    return 0


if __name__ == "__main__":
    # Use the Python interpreter that's running this script
    # This ensures compatibility with UV's Python management
    exit(main())
