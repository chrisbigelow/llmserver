from utils.llm import llm_testgen
from typing import Optional
import os
import typer

def testgen(test_directory: Optional[str] = typer.Option(os.getcwd(), help="filepath of file to generate test for", prompt="Enter the path to the c++ file to generate a test for")):
    llm_testgen(test_directory)
