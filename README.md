# Gemini by Example

A hands-on introduction to using the Google Gemini API through annotated example programs.

## Overview

Gemini by Example provides step-by-step tutorials for learning how to use the Gemini API in Python. The project features:

- Simple, commented examples that build from basic to advanced usage
- Side-by-side code and explanations
- Runnable shell commands with expected outputs
- Examples organized by category
- Support for images to illustrate concepts

## Project Structure

```txt
geminibyexample/
├── data/               # Processed data files
│   ├── examples.json   # Structured example data
│   └── sections.json   # Section definitions for organizing examples
├── examples/           # Source examples
│   ├── 001-basic-generation/
│   │   ├── basic-generation.py  # Python code with comments
│   │   ├── basic-generation.sh  # Shell commands and output
│   │   └── basic-generation.png # Optional example image
│   ├── 002-streaming-text/
│   └── ...
├── docs/               # MkDocs documentation site
│   ├── index.md        # Main index page
│   ├── text/           # Text examples
│   ├── images/         # Image examples
│   └── ...
├── tools/              # Utility tools
│   ├── example_generator/       # Tool for generating new examples
│   └── jekyll_to_mkdocs_converter/ # Conversion tools
├── mkdocs.yml          # MkDocs configuration
└── static/             # Static assets
```

## Quickstart

To build and preview the site locally:

```sh
# Install dependencies
uv venv
uv sync

# Build the MkDocs site
mkdocs build

# Serve the site locally
mkdocs serve

# Open the site in your browser
open http://127.0.0.1:8000
```

## Features

- **Organized Sections**: Examples are grouped into logical sections
- **Copy Code**: Material for MkDocs provides code copying functionality
- **Annotated Code**: Line-by-line explanations paired with code
- **Visual Examples**: Support for images to illustrate concepts
- **Shell Commands**: Example commands with expected output
- **Mobile-Friendly**: Responsive design works on all devices
- **Search**: Full-text search functionality
- **Dark Mode**: Support for dark mode

## Working with Examples

Examples are Python files with special comment formatting:

```python
# Title of the Example
# This is a description of what this example demonstrates.

# This is a comment that explains the next line of code
code_here()

# Another explanation
more_code()
```

- The first comment block becomes the title and description
- Each comment block explains the code that follows it
- Comments without following code create section headers

For detailed instructions on creating new examples, see [CONTRIBUTING.md](CONTRIBUTING.md).

## Generating New Examples

This project includes an automated example generator that simplifies the process of creating new examples:

```sh
python tools/example_generator/generate_mkdocs_example.py
```

The generator will:

- Automatically determine the next example number
- Generate Python code and shell commands using the Gemini API
- Create Markdown documentation in the appropriate section
- Update the mkdocs.yml navigation structure

The tool will prompt you for:

1. The name for the example
2. The specific aspect to focus on
3. An optional topical theme
4. Documentation URLs related to the example

For detailed instructions and examples, see the [Example Generator README](tools/example_generator/README.md).

## Building the Site

Build the MkDocs site with:

```sh
mkdocs build
```

This will:

1. Generate the static site in the `site/` directory
2. Copy all assets and images
3. Create a searchable index

To preview the site locally:

```sh
mkdocs serve
```

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for detailed instructions on how to:

- Add new examples (manually or using the [example generator](#generating-new-examples))
- Create example categories
- Include images
- Format your code and comments

## License

Apache License 2.0 - see the [LICENSE](LICENSE) file for details.
