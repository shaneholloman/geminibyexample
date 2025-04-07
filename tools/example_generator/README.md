# Gemini Example Generator for MkDocs

This tool helps generate new examples for the Gemini by Example MkDocs site. It automates the process of creating example files, documentation, and updating the MkDocs navigation.

## Features

- Automatically determines the next example number
- Generates Python code, shell commands, and optional requests code using Gemini API
- Creates Markdown documentation for MkDocs
- Updates the mkdocs.yml navigation structure
- Organizes examples into appropriate sections based on focus area
- Handles image requirements for examples that need them

## Prerequisites

- Python 3.12+
- Dependencies installed via `uv sync` (see pyproject.toml in the project root)
- Gemini API key (provided in the script)

## Usage

Run the script from the project root directory:

```bash
python tools/example_generator/generate_mkdocs_example.py
```

The script will prompt you for:

1. The name for the example (e.g., "hello-world")
2. The specific aspect to focus on (e.g., "streaming text", "image generation")
3. An optional topical theme (e.g., "cats", "astronomy")
4. Documentation URLs related to the example (a default URL will be used if none provided)

## How It Works

1. The script determines the next available example number
2. It prompts for example details
3. It fetches content from provided documentation URLs
4. It uses the Gemini API to generate code examples
5. It creates the necessary files in the examples directory
6. It creates a Markdown file in the appropriate docs section
7. It updates the mkdocs.yml navigation structure

## Output

The script generates:

- Python file in the examples directory
- Shell script in the examples directory
- Optional requests code file if curl examples are found
- Documentation links file
- Markdown file in the appropriate docs section

## Example

```
$ python tools/example_generator/generate_mkdocs_example.py
Welcome to the Gemini Example Generator!
Enter the name for this example (e.g., hello-world): image-classification
What specific aspect should this example focus on? (e.g., streaming text, multi-turn chat, etc.): image classification
Do you want a specific topical theme for this example? (e.g., cats, astronomy, cooking, etc. Leave blank for no theme): animals
Enter documentation URLs related to this example (press Enter when done): https://ai.google.dev/tutorials/image_classification_tutorial
URL:

Fetching content from URLs...
Generating example using Gemini...
Saved documentation links to examples/034-image-classification/image-classification_links.txt
Created Markdown file: docs/images/image-classification.md
Updated mkdocs.yml with new example

Successfully created example in examples/034-image-classification
```

## Maintenance

If you need to modify the script:

1. Make your changes
2. Run `ruff check tools/example_generator/generate_mkdocs_example.py` to check for issues
   - Note: Line length errors (E501) are ignored in the project's ruff configuration
3. Fix any other issues found by ruff
4. Test the script by generating a new example
