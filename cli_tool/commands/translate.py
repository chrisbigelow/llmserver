from pathlib import Path
from typing import Optional
from utils.llm import llm_translate
import typer
import questionary


def translate(syntax: Optional[str] = typer.Option(None, help="syntax to translate the requirements doc to", case_sensitive=False), filepath: Optional[str] = typer.Option(None, help="filepath of markdown file", prompt="Enter the path to the markdown file to translate")):
    """
    Read a markdown file, perform translation, and write to a new file with '_translated' added to the filename.
    """
    if not syntax:
        syntax = questionary.select(
            "Select a translation syntax",
            choices=[
                "EASY",
                "Other",
                "Other2"
            ]).ask()
    # Ensure the file exists
    input_path = Path(filepath)
    if not input_path.exists() or not input_path.is_file():
        typer.echo(f"The file {filepath} does not exist.")
        raise typer.Exit(code=1)

    # Ensure the file is a markdown file
    if input_path.suffix != '.md':
        typer.echo(f"The file {filepath} is not a markdown file.")
        raise typer.Exit(code=1)

    # Read the content of the markdown file
    with open(input_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Call llm to translate the content
    print("Content: ", content)
    transformed_content = llm_translate(content)

    # Define the new filename with '_translated' appended before the file extension
    new_filename = input_path.stem + '_translated' + input_path.suffix
    output_path = input_path.parent / new_filename

    # Write the transformed content to the new markdown file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(transformed_content)

    typer.echo(f"Translated file saved as {output_path}")
