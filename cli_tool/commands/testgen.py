from utils.llm import llm_testgen
from typing import Optional
import typer


def testgen(test_filepath: Optional[str] = typer.Option(None, help="filepath of file to generate test for", prompt="Enter the path to the c++ file to generate a test for")):
    llm_testgen(test_filepath)
