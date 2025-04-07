# Converting Gemini by Example to MkDocs

This guide explains how to convert the Gemini by Example site from its custom static site generator to MkDocs.

## Prerequisites

Before you begin, make sure you have Python 3.9+ installed and UV package manager. Then set up a virtual environment and install the required dependencies:

```sh
# Create a virtual environment using UV's native way
uv venv

# Install dependencies from pyproject.toml
uv sync
```

UV will automatically create and manage the virtual environment for you. It will also activate the environment when running commands like `uv sync`.

If you don't have UV installed, you can install it following the instructions at [https://github.com/astral-sh/uv](https://github.com/astral-sh/uv).

Alternatively, you can use the migration script which will handle the virtual environment creation and dependency installation for you:

```sh
python3 migrate_to_mkdocs.py
```

## Conversion Process

The conversion process involves two main steps:

1. Converting the existing examples to Markdown files
2. Building the MkDocs site

### Step 1: Set Up Environment and Dependencies

First, set up the environment and install dependencies:

```sh
# Create a virtual environment and install dependencies
uv venv
uv sync
```

### Step 2: Convert Examples to Markdown

Run the conversion script to transform the examples from the JSON format to Markdown files:

```sh
# Run the conversion script
python3 convert_to_mkdocs.py
```

This script will:

- Read the existing `data/examples.json` and `data/sections.json` files
- Create a `docs_mkdocs/` directory with the Markdown files
- Generate a `mkdocs.yml` configuration file
- Copy images to the appropriate locations

### Step 3: Build and Preview the MkDocs Site

Once the conversion is complete, you can build and preview the MkDocs site:

```sh
# Build the site
mkdocs build

# Preview the site locally
mkdocs serve
```

The `mkdocs serve` command will start a local server. Open your browser to [http://127.0.0.1:8000/](http://127.0.0.1:8000/) to view the site.

## Deploying to GitHub Pages

To deploy the site to GitHub Pages, you have two options:

### Option 1: Using the gh-pages branch (recommended)

If you want to use the `gh-pages` branch:

```sh
mkdocs gh-deploy
```

### Option 2: Using the docs directory

If you want to use the `docs/` directory in the main branch:

```sh
# Build the site
mkdocs build
# Copy the site to docs/
cp -r site/* docs/
```

## Customizing the Site

You can customize the MkDocs site by editing the `mkdocs.yml` file. Some common customizations include:

- Changing the theme colors
- Adding additional plugins
- Configuring the navigation structure
- Adding custom CSS

For more information, see the [MkDocs documentation](https://www.mkdocs.org/) and the [Material for MkDocs documentation](https://squidfunk.github.io/mkdocs-material/).

## Directory Structure

After conversion, your project will have the following structure:

```text
geminibyexample/
├── mkdocs.yml                # MkDocs configuration
├── docs_mkdocs/              # MkDocs documentation directory
│   ├── index.md              # Home page
│   ├── text/                 # Section directories
│   │   ├── index.md          # Section index
│   │   ├── basic-generation.md
│   │   └── ...
│   └── ...
├── site/                     # Generated static site (after running mkdocs build)
├── examples/                 # Original examples (unchanged)
└── ...
```

## Migrating from the Old Site

To fully migrate from the old site to MkDocs:

1. Complete the conversion process above
2. Update any references to the old site structure
3. If using GitHub Pages from the `docs/` directory, replace the contents of the `docs/` directory with the contents of the `site/` directory
4. Add a `.nojekyll` file to the `site/` or `docs/` directory to disable Jekyll processing on GitHub Pages

## Troubleshooting

If you encounter any issues during the conversion process:

- Make sure the `data/examples.json` and `data/sections.json` files exist and are valid JSON
- Check that the images referenced in the examples exist in the expected locations
- Verify that you have installed all the required dependencies
