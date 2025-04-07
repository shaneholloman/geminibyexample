#!/usr/bin/env python3
"""
Migration script to convert Gemini by Example to MkDocs and build the site.

This script automates the process of:
1. Converting the examples to Markdown
2. Installing MkDocs and dependencies if needed
3. Building the MkDocs site
4. Optionally deploying to GitHub Pages
"""

import argparse
import subprocess
import sys
from pathlib import Path


def run_command(command, description=None):
    """Run a shell command and print the output."""
    if description:
        print(f"\n{description}...")

    try:
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        print(f"Command output: {e.stdout}")
        print(f"Command error: {e.stderr}")
        return False


def check_dependencies():
    """Check if the required dependencies are installed."""
    print("Checking dependencies...")

    # Check if UV is available
    if not run_command("uv --version", "Checking UV"):
        print("Error: UV is not available. Please install UV first.")
        return False

    # Check if the pyproject.toml file exists
    if not Path("pyproject.toml").exists():
        print("Error: pyproject.toml not found.")
        return False

    # Create a virtual environment using UV's native way
    if not run_command("uv venv", "Creating virtual environment"):
        print("Error: Failed to create virtual environment.")
        return False

    # Install dependencies using UV sync
    if not run_command("uv sync", "Installing dependencies"):
        print("Error: Failed to install dependencies.")
        return False

    print("Dependencies installed successfully.")
    print("UV has created and configured the virtual environment automatically.")

    return True


def convert_examples():
    """Run the conversion script to convert examples to Markdown."""
    if not Path("convert_to_mkdocs.py").exists():
        print("Error: convert_to_mkdocs.py not found.")
        return False

    return run_command(
        "python3 convert_to_mkdocs.py", "Converting examples to Markdown"
    )


def build_mkdocs_site():
    """Build the MkDocs site."""
    if not Path("mkdocs.yml").exists():
        print("Error: mkdocs.yml not found. Run the conversion script first.")
        return False

    return run_command("mkdocs build", "Building MkDocs site")


def serve_mkdocs_site():
    """Serve the MkDocs site locally."""
    if not Path("mkdocs.yml").exists():
        print("Error: mkdocs.yml not found. Run the conversion script first.")
        return False

    return run_command("mkdocs serve", "Starting local server")


def deploy_to_github_pages():
    """Deploy the MkDocs site to GitHub Pages."""
    if not Path("mkdocs.yml").exists():
        print("Error: mkdocs.yml not found. Run the conversion script first.")
        return False

    return run_command("mkdocs gh-deploy", "Deploying to GitHub Pages")


def copy_to_docs_directory():
    """Copy the built site to the docs directory."""
    if not Path("site").exists():
        print("Error: site directory not found. Build the site first.")
        return False

    # Create docs directory if it doesn't exist
    Path("docs").mkdir(exist_ok=True)

    # Copy site contents to docs
    return run_command("cp -r site/* docs/", "Copying site to docs directory")


def create_nojekyll():
    """Create a .nojekyll file to disable Jekyll processing on GitHub Pages."""
    # Create .nojekyll in the site directory
    Path("site/.nojekyll").touch(exist_ok=True)

    # If docs directory exists, create .nojekyll there too
    if Path("docs").exists():
        Path("docs/.nojekyll").touch(exist_ok=True)

    print("Created .nojekyll files to disable Jekyll processing.")
    return True


def main():
    """Main function to run the migration process."""
    parser = argparse.ArgumentParser(description="Migrate Gemini by Example to MkDocs")
    parser.add_argument(
        "--convert-only", action="store_true", help="Only convert examples to Markdown"
    )
    parser.add_argument(
        "--build-only", action="store_true", help="Only build the MkDocs site"
    )
    parser.add_argument(
        "--serve", action="store_true", help="Serve the MkDocs site locally"
    )
    parser.add_argument("--deploy", action="store_true", help="Deploy to GitHub Pages")
    parser.add_argument(
        "--copy-to-docs",
        action="store_true",
        help="Copy the built site to the docs directory",
    )

    args = parser.parse_args()

    # If no specific actions are specified, do everything except deploy
    do_all = not (
        args.convert_only
        or args.build_only
        or args.serve
        or args.deploy
        or args.copy_to_docs
    )

    # Check dependencies
    if not check_dependencies():
        return 1

    # Convert examples
    if args.convert_only or do_all:
        if not convert_examples():
            return 1

    # Build MkDocs site
    if args.build_only or do_all:
        if not build_mkdocs_site():
            return 1

        # Create .nojekyll file
        create_nojekyll()

    # Copy to docs directory
    if args.copy_to_docs or do_all:
        if not copy_to_docs_directory():
            return 1

    # Serve MkDocs site locally
    if args.serve:
        if not serve_mkdocs_site():
            return 1

    # Deploy to GitHub Pages
    if args.deploy:
        if not deploy_to_github_pages():
            return 1

    print("\nMigration completed successfully!")
    if do_all:
        print("\nNext steps:")
        print("1. Preview the site locally: mkdocs serve")
        print("2. Deploy to GitHub Pages: mkdocs gh-deploy")

    return 0


if __name__ == "__main__":
    sys.exit(main())
