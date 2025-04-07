#!/usr/bin/env python3
"""
Generate new examples for the Gemini by Example MkDocs site.

This script creates new example files and corresponding MkDocs documentation.
It uses the Gemini API to generate code examples based on documentation URLs.
"""

import os
import re
from pathlib import Path

import requests
import yaml
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from google import genai
from pydantic import BaseModel, Field
from rich import print as rprint
from rich.prompt import Prompt

# Ensure we're running from the project root
PROJECT_ROOT = Path(__file__).parent.parent.parent.absolute()
os.chdir(PROJECT_ROOT)

# Load environment variables from .env file
load_dotenv()

# Get API key from environment variables
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    rprint("[bold red]Error: GEMINI_API_KEY not found in environment variables.[/bold red]")
    rprint("[bold yellow]Please create a .env file with your API key or copy from example.env.[/bold yellow]")
    exit(1)

GEMINI_MODEL = "gemini-2.5-pro-preview-03-25"


class GeminiExample(BaseModel):
    """Represents a code example for the Gemini by Example site."""

    python_code: str = Field(description="The Python code to be displayed and executed")
    shell_code: str = Field(
        description="Shell commands to run the Python code and sample outputs"
    )
    requests_code: str | None = Field(
        description="Python code using requests to replicate curl examples",
        default=None,
    )
    requires_image: bool = Field(
        description="Whether this example needs an image to be displayed",
    )


def fetch_url_content(url: str) -> str:
    """Fetch and parse content from a URL."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.extract()

        return soup.get_text()
    except Exception as e:
        rprint(f"[bold red]Error fetching {url}: {e}[/bold red]")
        return ""


def get_example_files_content():
    """Get content from example files."""
    python_example = Path("examples/002-streaming-text/streaming-text.py").read_text()
    shell_example = Path("examples/002-streaming-text/streaming-text.sh").read_text()
    requests_example = Path(
        "examples/002-streaming-text/streaming-text_requests.py"
    ).read_text()
    return python_example, shell_example, requests_example


def get_contributing_guidelines():
    """Extract formatting guidelines from CONTRIBUTING.md."""
    contributing_text = Path("CONTRIBUTING.md").read_text()

    # Extract formatting sections with safer pattern matching
    python_format_match = re.search(
        r"### 2\. Add Python File.*?```python(.*?)```", contributing_text, re.DOTALL
    )
    python_format = python_format_match.group(1) if python_format_match else ""

    shell_format_match = re.search(
        r"### 3\. Add Shell Script.*?```sh(.*?)```", contributing_text, re.DOTALL
    )
    shell_format = shell_format_match.group(1) if shell_format_match else ""

    formatting_rules_match = re.search(
        r"#### Formatting Rules:(.*?)###", contributing_text, re.DOTALL
    )
    formatting_rules = formatting_rules_match.group(1) if formatting_rules_match else ""

    shell_format_rules_match = re.search(
        r"#### Shell Script Format:(.*?)###", contributing_text, re.DOTALL
    )
    shell_format_rules = ""
    if shell_format_rules_match:
        shell_format_rules = shell_format_rules_match.group(1)

    return python_format, shell_format, formatting_rules, shell_format_rules


def generate_example(prompt: str) -> GeminiExample:
    client = genai.Client(api_key=GEMINI_API_KEY)

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_schema": GeminiExample,
        },
    )

    # Cast to GeminiExample to satisfy type checker
    result = response.parsed
    if not isinstance(result, GeminiExample):
        raise ValueError("Failed to generate example with the expected schema")

    return result


def get_next_example_number() -> int:
    """Determine the next available example number based on existing examples."""
    examples_dir = Path("examples")

    if not examples_dir.exists():
        return 1  # Start with 001 if examples directory doesn't exist

    # Get all example directories that match the pattern NNN-*
    example_dirs = [
        d for d in examples_dir.iterdir() if d.is_dir() and re.match(r"^\d{3}-", d.name)
    ]

    if not example_dirs:
        return 1  # Start with 001 if no examples exist

    # Extract the numeric portion and find the max
    max_number = 0
    for dir_path in example_dirs:
        match = re.match(r"^(\d{3})-", dir_path.name)
        if match:
            number = int(match.group(1))
            max_number = max(max_number, number)

    return max_number + 1


def determine_section(focus: str) -> str:
    """Determine which section the example belongs to based on its focus."""
    # Map of keywords to sections (matching the case in mkdocs.yml)
    section_mapping = {
        "text": "Text",
        "streaming": "Text",
        "chat": "Text",
        "system prompt": "Text",
        "reasoning": "Text",
        "structured output": "Text",

        "image": "Images",
        "vision": "Images",
        "bounding box": "Images",
        "segmentation": "Images",

        "audio": "Audio",
        "speech": "Audio",
        "transcription": "Audio",

        "video": "Video",
        "youtube": "Video",

        "pdf": "PDFs and other data types",
        "csv": "PDFs and other data types",
        "translation": "PDFs and other data types",
        "extract": "PDFs and other data types",

        "function": "Agentic behaviour",
        "tool": "Agentic behaviour",
        "code execution": "Agentic behaviour",
        "mcp": "Agentic behaviour",
        "grounded": "Agentic behaviour",

        "token": "Token counting & context windows",
        "context window": "Token counting & context windows",
        "caching": "Token counting & context windows",

        "rate limit": "Miscellaneous",
        "retry": "Miscellaneous",
        "concurrent": "Miscellaneous",
        "embedding": "Miscellaneous",
        "safety": "Miscellaneous",
        "litellm": "Miscellaneous",
    }

    # Convert focus to lowercase for case-insensitive matching
    focus_lower = focus.lower()

    # Find the matching section
    for keyword, section in section_mapping.items():
        if keyword in focus_lower:
            return section

    # Default to miscellaneous if no match found
    return "miscellaneous"


def create_markdown_file(title: str, description: str, python_code: str,
                        shell_code: str, example_name: str, section: str) -> Path:
    """Create a Markdown file for MkDocs documentation."""
    # Create the section directory if it doesn't exist
    # Convert section name to lowercase for directory path
    section_dir = section.lower().replace(" & ", "-").replace(" ", "-")
    docs_dir = Path("docs") / section_dir
    docs_dir.mkdir(parents=True, exist_ok=True)

    # Extract just the actual description part (first paragraph)
    # This is needed because the Gemini API sometimes includes the Python code in the description
    if description:
        # Find the first paragraph (everything before the first blank line or code)
        lines = description.split('\n')
        description_lines = []
        for line in lines:
            if not line.strip() or line.strip().startswith('#'):
                break
            description_lines.append(line)

        description = '\n'.join(description_lines).strip()

    # Create the markdown content
    markdown_content = f"# {title}\n\n"

    if description:
        markdown_content += f"{description}\n\n"

    # Add Python code section
    markdown_content += "## Example Code\n\n"
    markdown_content += f"```python\n{python_code}\n```\n\n"

    # Add shell commands section
    markdown_content += "## Running the Example\n\n"
    markdown_content += f"```sh\n{shell_code}\n```\n\n"

    # Write the markdown file
    markdown_file = docs_dir / f"{example_name}.md"
    markdown_file.write_text(markdown_content)

    return markdown_file


def update_mkdocs_yml(example_name: str, title: str, section: str) -> bool:
    """Update the mkdocs.yml file to include the new example."""
    try:
        # Read the current mkdocs.yml file
        with open("mkdocs.yml", "r") as f:
            config = yaml.safe_load(f)

        # Find the section in the navigation
        for nav_item in config.get("nav", []):
            if isinstance(nav_item, dict) and section in nav_item:
                # Found the section, add the example to it
                section_items = nav_item[section]

                # Find the position to insert (after "Overview")
                insert_pos = 1  # Default to position after "Overview"
                for i, item in enumerate(section_items):
                    if isinstance(item, dict) and "Overview" in item:
                        insert_pos = i + 1
                        break

                # Insert the new example
                section_dir = section.lower().replace(" & ", "-").replace(" ", "-")
                nav_path = f"{section_dir}/{example_name}.md"
                section_items.insert(insert_pos, {title: nav_path})

                # Write the updated config back to the file
                with open("mkdocs.yml", "w") as f:
                    yaml.dump(config, f, default_flow_style=False, sort_keys=False)

                return True

        # If we get here, the section wasn't found
        msg = f"[bold yellow]Warning: Section '{section}' not found in mkdocs.yml."
        rprint(f"{msg} Navigation not updated.[/bold yellow]")
        return False

    except Exception as e:
        rprint(f"[bold red]Error updating mkdocs.yml: {e}[/bold red]")
        return False


def main():
    rprint("[bold blue]Welcome to the Gemini Example Generator![/bold blue]")

    # Automatically determine the next example number
    next_number = get_next_example_number()

    # Ask for the text portion of the folder name
    example_name = Prompt.ask(
        "[yellow]Enter the name for this example[/yellow] (e.g., hello-world)"
    )

    # Validate example name format (should be like hello-world)
    while not re.match(r"^[a-z0-9-]+$", example_name):
        rprint(
            "[bold red]Example name should only contain lowercase letters, numbers, and hyphens[/bold red]"
        )
        example_name = Prompt.ask(
            "[yellow]Enter the name for this example[/yellow] (e.g., hello-world)"
        )

    # Construct the full folder name with numeric prefix
    folder_name = f"{next_number:03d}-{example_name}"
    rprint(f"[green]Creating example in folder: {folder_name}[/green]")

    # Ask for focus area
    focus = Prompt.ask(
        "[yellow]What specific aspect should this example focus on?[/yellow] (e.g., streaming text, multi-turn chat, etc.)"
    )

    # Ask for topical theme
    theme = Prompt.ask(
        "[yellow]Do you want a specific topical theme for this example?[/yellow] (e.g., cats, astronomy, cooking, etc. Leave blank for no theme)",
        default="",
    )

    # Ask for documentation URLs
    urls = []
    rprint(
        "[yellow]Enter documentation URLs related to this example (press Enter when done)[/yellow]"
    )
    rprint("[blue]For testing, you can use: https://ai.google.dev/tutorials/python_quickstart[/blue]")
    while True:
        url = Prompt.ask("URL", default="")
        if not url:
            break
        urls.append(url)

    if not urls:
        # For testing purposes, use a default URL
        default_url = "https://ai.google.dev/tutorials/python_quickstart"
        rprint(f"[yellow]No URLs provided. Using default URL: {default_url}[/yellow]")
        urls.append(default_url)

    # Fetch content from URLs
    rprint("\n[blue]Fetching content from URLs...[/blue]")
    docs_content = ""
    for url in urls:
        content = fetch_url_content(url)
        if content:
            docs_content += f"\n\n--- Content from {url} ---\n\n{content}"

    # Get example files and contributing guidelines
    python_example, shell_example, requests_example = get_example_files_content()
    python_format, shell_format, formatting_rules, shell_format_rules = (
        get_contributing_guidelines()
    )

    # Create the prompt
    prompt = f"""
You are an expert devrel with years of experience in creating code examples that help developers learn new technologies.

Your task today is to take some documentation from the Google Gemini SDK docs and turn it into a simple illustrative example using code.

## Focus Area
This example should specifically focus on: {focus}

{f"## Topical Theme\nThis example should incorporate the thematic elements of: {theme}" if theme else ""}

## Documentation Content
{docs_content}

## Formatting / Output rules
You will output the following:

- Python code formatted according to the guidelines below
- Shell code/output formatted according to the guidelines below
- Python requests code that replicates any curl examples found in the documentation, using the requests library (only if curl examples are present in the documentation). Note: This is stored in a separate file and is not used in the site build.
- A boolean as to whether you think it needs an image to illustrate the output (i.e., if image generation or editing is involved)

### Python File Format:
{python_format}

Python Formatting Rules:
{formatting_rules}

### Shell Script Format:
{shell_format}

Shell Script Formatting Rules:
{shell_format_rules}

## Examples
Here's an example of the Python code format:

```python
{python_example}
```

Here's an example of the shell code format:

```sh
{shell_example}
```

Here's an example of the requests code format:

```python
{requests_example}
```

Based on the documentation provided, please generate a concise, illustrative
example that demonstrates the key concepts clearly, focusing specifically on
{focus}. If the documentation contains multiple examples or topics, prioritize
content related to {focus} and ignore unrelated sections. The title line (i.e.
the first line of the Python file) should be very concise and focus on the core
thing we're focusing on (e.g. "Streaming text", "Image generation", "Editing images", "Object detection").
{f"Try to incorporate elements of the theme: {theme} in your example where it makes sense, such as in prompts, variables, or example text." if theme else ""}

For the requests_code, ONLY include this if you find actual curl examples in the documentation. If curl examples exist, translate them to Python code using the requests library. Do NOT create requests code if there are no curl examples in the documentation.
"""

    # Generate the example
    rprint("\n[blue]Generating example using Gemini...[/blue]")
    try:
        result = generate_example(prompt)

        # Create the directory structure
        example_dir = Path("examples") / folder_name
        example_dir.mkdir(parents=True, exist_ok=True)

        # Extract the example name from the folder (e.g., "basic-generation" from "001-basic-generation")
        example_name = folder_name.split("-", 1)[1]

        # Save Python file
        python_file = example_dir / f"{example_name}.py"
        python_file.write_text(result.python_code)

        # Save Shell file
        shell_file = example_dir / f"{example_name}.sh"
        shell_file.write_text(result.shell_code)

        # Save Requests file if curl examples were found
        if result.requests_code:
            requests_file = example_dir / f"{example_name}_requests.py"
            requests_file.write_text(result.requests_code)

        # Save documentation URLs to a text file
        if urls:
            docs_file = example_dir / f"{example_name}_links.txt"
            docs_file.write_text("\n".join(urls))
            rprint(f"[blue]Saved documentation links to {docs_file}[/blue]")

        # Extract title and description from the Python code
        title_match = re.match(r"^# (.+?)$", result.python_code.split("\n")[0])
        title = title_match.group(1) if title_match else example_name.replace("-", " ").title()

        # Extract description (second comment line if it exists)
        description_match = re.match(r"^# .+?\n# (.+?)$", result.python_code, re.DOTALL)
        description = description_match.group(1).strip() if description_match else ""

        # Determine which section this example belongs to
        section = determine_section(focus)

        # Create the Markdown file for MkDocs
        markdown_file = create_markdown_file(
            title, description, result.python_code, result.shell_code, example_name, section
        )
        rprint(f"[blue]Created Markdown file: {markdown_file}[/blue]")

        # Update the mkdocs.yml file
        if update_mkdocs_yml(example_name, title, section):
            rprint("[blue]Updated mkdocs.yml with new example[/blue]")

        rprint(
            f"\n[bold green]Successfully created example in {example_dir}[/bold green]"
        )

        # Notify if an image is needed
        if result.requires_image:
            rprint(
                f"\n[bold red]NOTE: This example requires an image named '{example_name}.png' in the example directory.[/bold red]"
            )

            # Create images directory if needed
            images_dir = Path("docs") / section / "images"
            images_dir.mkdir(parents=True, exist_ok=True)

            rprint(
                f"[bold yellow]Remember to add the image to both {example_dir} and {images_dir}[/bold yellow]"
            )

    except Exception as e:
        rprint(f"[bold red]Error generating example: {e}[/bold red]")


if __name__ == "__main__":
    main()
