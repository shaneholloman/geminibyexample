#!/usr/bin/env python3
"""
Conversion script to transform Gemini by Example to MkDocs.

This script reads the existing examples.json and sections.json files,
and converts them to Markdown files for use with MkDocs.
"""

import json
import os
import re
import shutil

try:
    import yaml
except ImportError:
    print("PyYAML is not installed. Please run 'uv sync' to install dependencies.")
    import sys

    sys.exit(1)

# Constants
INPUT_EXAMPLES_JSON = "data/examples.json"
INPUT_SECTIONS_JSON = "data/sections.json"
OUTPUT_DOCS_DIR = "docs"
EXAMPLES_DIR = "examples"


def load_json_data(file_path):
    """Load JSON data from a file."""
    with open(file_path, "r") as f:
        return json.load(f)


def create_directory(path):
    """Create a directory if it doesn't exist."""
    os.makedirs(path, exist_ok=True)


def slugify(text):
    """Convert text to a URL-friendly slug."""
    # Remove special characters and replace spaces with hyphens
    slug = re.sub(r"[^\w\s-]", "", text.lower())
    slug = re.sub(r"[\s_-]+", "-", slug)
    return slug


def copy_images(example, source_dir, target_dir):
    """Copy images from the example directory to the target directory."""
    image_data = example.get("image_data", [])
    if not image_data:
        return []

    # Create images directory in the target directory
    images_dir = os.path.join(target_dir, "images")
    create_directory(images_dir)

    copied_images = []
    for image in image_data:
        src_path = os.path.join(source_dir, image["path"])
        filename = image["filename"]
        dst_path = os.path.join(images_dir, filename)

        if os.path.exists(src_path):
            shutil.copy2(src_path, dst_path)
            copied_images.append(
                {"filename": filename, "caption": image.get("caption", "")}
            )

    return copied_images


def convert_code_segments_to_markdown(code_segments):
    """Convert code segments to Markdown format."""
    markdown = []
    current_annotation = ""

    for segment in code_segments:
        annotation = segment.get("annotation", "")
        code = segment.get("display_code", "").strip()

        # Skip empty segments
        if not annotation and not code:
            continue

        # If there's an annotation, add it as text
        if annotation:
            if current_annotation:
                current_annotation += "\n\n"
            current_annotation += annotation

        # If there's code, add it as a code block
        if code:
            if current_annotation:
                markdown.append(current_annotation)
                current_annotation = ""

            markdown.append(f"```python\n{code}\n```")

    # Add any remaining annotation
    if current_annotation:
        markdown.append(current_annotation)

    return markdown


def convert_shell_segments_to_markdown(shell_segments):
    """Convert shell segments to Markdown format."""
    if not shell_segments:
        return []

    markdown = ["## Running the Example"]

    for segment in shell_segments:
        explanation = segment.get("explanation", "")
        command = segment.get("command", "")
        output = segment.get("output", "")

        if explanation:
            markdown.append(explanation)

        if command:
            markdown.append(f"```sh\n$ {command}\n{output}\n```")

    return markdown


def create_example_markdown(example, project_root, section_dir):
    """Convert an example to a Markdown file."""
    title = example["title"]
    description = example.get("description", "")

    # Create the markdown content
    markdown = [f"# {title}"]

    if description:
        markdown.append(description)

    # Convert code segments
    code_markdown = convert_code_segments_to_markdown(example["code_segments"])
    markdown.extend(code_markdown)

    # Convert shell segments
    shell_markdown = convert_shell_segments_to_markdown(
        example.get("shell_segments", [])
    )
    if shell_markdown:
        markdown.append("")  # Add a blank line
        markdown.extend(shell_markdown)

    # Copy images and add to markdown
    copied_images = copy_images(example, project_root, section_dir)

    if copied_images:
        markdown.append("")  # Add a blank line
        markdown.append("## Images")

        for image in copied_images:
            caption = image.get("caption", "")
            caption_text = f" - {caption}" if caption else ""
            markdown.append(f"![{caption}](images/{image['filename']}){caption_text}")

    # Add documentation links if available
    doc_links = example.get("documentation_links", [])
    if doc_links:
        markdown.append("")  # Add a blank line
        markdown.append("## Further Information")

        for i, link in enumerate(doc_links, 1):
            markdown.append(f"- [Gemini docs link {i}]({link})")

    # Join all markdown parts with double newlines
    return "\n\n".join(markdown)


def create_section_index(section, examples):
    """Create an index.md file for a section."""
    title = section["title"]
    description = section.get("description", "")

    markdown = [f"# {title}"]

    if description:
        markdown.append(description)

    markdown.append("## Examples in this section")

    # Add links to each example in the section
    section_examples = [e for e in examples if e.get("section_id") == section["id"]]
    for example in sorted(section_examples, key=lambda e: e["order"]):
        example_slug = slugify(example["title"])
        markdown.append(f"- [{example['title']}]({example_slug}.md)")

    return "\n\n".join(markdown)


def create_main_index(sections, examples):
    """Create the main index.md file."""
    markdown = [
        "# Gemini by Example",
        "A hands-on introduction to using the Google Gemini API through "
        "annotated example programs."
    ]

    markdown.append("## Overview")
    markdown.append(
        "Gemini by Example provides step-by-step tutorials for learning how to use "
        "the Gemini API in Python. The project features:"
    )
    markdown.append(
        "- Simple, commented examples that build from basic to advanced usage"
    )
    markdown.append("- Side-by-side code and explanations")
    markdown.append("- Runnable shell commands with expected outputs")
    markdown.append("- Examples organized by category")
    markdown.append("- Support for images to illustrate concepts")

    markdown.append("## Sections")

    # Add links to each section
    for section in sorted(sections, key=lambda s: s["order"]):
        section_slug = slugify(section["title"])
        section_examples = [e for e in examples if e.get("section_id") == section["id"]]
        example_count = len(section_examples)

        link_text = f"- [{section['title']}]({section_slug}/index.md)"
        markdown.append(f"{link_text} - {example_count} examples")

    return "\n\n".join(markdown)


def generate_mkdocs_yml(sections, examples):
    """Generate the mkdocs.yml configuration file."""
    # Create the basic configuration
    config = {
        "site_name": "Gemini by Example",
        "site_description": "Learn the Gemini API through annotated examples",
        "theme": {
            "name": "material",
            "palette": {"primary": "indigo", "accent": "indigo"},
            "features": [
                "content.code.copy",
                "navigation.instant",
                "navigation.tracking",
                "navigation.indexes",
                "navigation.top",
            ],
        },
        "markdown_extensions": [
            "pymdownx.highlight",
            "pymdownx.superfences",
            "pymdownx.inlinehilite",
            "pymdownx.snippets",
            "admonition",
            "pymdownx.details",
            "attr_list",
            "md_in_html",
        ],
        "plugins": ["search"],
        "nav": [{"Home": "index.md"}],
    }

    # Add sections and examples to the navigation
    for section in sorted(sections, key=lambda s: s["order"]):
        section_title = section["title"]
        section_slug = slugify(section_title)

        section_nav = {section_title: []}

        # Add section index
        section_nav[section_title].append({"Overview": f"{section_slug}/index.md"})

        # Add examples in this section
        section_examples = [e for e in examples if e.get("section_id") == section["id"]]
        for example in sorted(section_examples, key=lambda e: e["order"]):
            example_title = example["title"]
            example_slug = slugify(example_title)
            section_nav[section_title].append(
                {example_title: f"{section_slug}/{example_slug}.md"}
            )

        config["nav"].append(section_nav)

    class IndentDumper(yaml.Dumper):
        def increase_indent(self, flow=False, indentless=False):
            return super(IndentDumper, self).increase_indent(flow, False)

    with open("mkdocs.yml", "w") as f:
        yaml.dump(config, f, IndentDumper, default_flow_style=False)


def main():
    """Main function to convert the site to MkDocs."""
    print("Converting Gemini by Example to MkDocs...")

    # Load the data
    examples_data = load_json_data(INPUT_EXAMPLES_JSON)
    sections_data = load_json_data(INPUT_SECTIONS_JSON)

    examples = examples_data["examples"]
    sections = sections_data["sections"]

    # Create the output directory
    create_directory(OUTPUT_DOCS_DIR)

    # Create the main index.md
    main_index = create_main_index(sections, examples)
    with open(os.path.join(OUTPUT_DOCS_DIR, "index.md"), "w") as f:
        f.write(main_index)

    # Process each section
    for section in sections:
        section_title = section["title"]
        section_slug = slugify(section_title)
        section_dir = os.path.join(OUTPUT_DOCS_DIR, section_slug)
        create_directory(section_dir)

        # Create section index
        section_index = create_section_index(section, examples)
        with open(os.path.join(section_dir, "index.md"), "w") as f:
            f.write(section_index)

        # Process examples in this section
        section_examples = [e for e in examples if e.get("section_id") == section["id"]]
        for example in section_examples:
            example_title = example["title"]
            example_slug = slugify(example_title)

            # Create example markdown
            example_markdown = create_example_markdown(
                example, os.getcwd(), section_dir
            )
            with open(os.path.join(section_dir, f"{example_slug}.md"), "w") as f:
                f.write(example_markdown)

    # Generate mkdocs.yml
    generate_mkdocs_yml(sections, examples)

    print(
        f"Conversion complete! MkDocs files are in the '{OUTPUT_DOCS_DIR}' directory."
    )
    print("\nNext steps:")
    print("1. Build the site: mkdocs build")
    print("2. Preview the site: mkdocs serve")


if __name__ == "__main__":
    main()
