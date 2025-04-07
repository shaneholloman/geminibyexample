# Jekyll to MkDocs Converter

This directory contains tools to convert a Jekyll-based documentation site to MkDocs.

## Files

- `convert_to_mkdocs.py`: Main conversion script that transforms Jekyll content to MkDocs format
- `migrate_to_mkdocs.py`: Script to handle the full migration process including dependency installation
- `test_conversion.py`: Test script to verify data loading and processing
- `pyproject.toml`: Python project configuration with dependencies and tool settings
- `pyrightconfig.json`: Pylance/Pyright configuration for type checking
- `README_MKDOCS.md`: Detailed documentation about the MkDocs setup

## Usage

1. Copy these files to the root of your Jekyll project
2. Install dependencies:

    ```sh
    uv venv
    uv sync
    ```

3. Run the migration script:

    ```sh
    python3 migrate_to_mkdocs.py
    ```

This will:

- Convert your Jekyll content to MkDocs format
- Generate a proper mkdocs.yml configuration
- Build the MkDocs site
- Provide options to preview and deploy the site

## Requirements

- Python 3.12 or higher
- UV package manager (recommended) or pip

## Customization

You may need to modify the scripts to match your specific Jekyll structure. The main areas to check are:

- Input file paths in `convert_to_mkdocs.py`
- Output directory structure
- Navigation structure in the generated mkdocs.yml
