import typer
from rich.progress import Progress, SpinnerColumn, TextColumn
from langchain_openai import ChatOpenAI
import subprocess
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_together import Together
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from .bazel_setup import bazel_run_tests, create_workspace_directory, create_workspace_file, setup_workspace, create_build_file
import os


def llm_translate(content):
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system",
             "Transform the following markdown into Easy Approach to Requirements Syntax (EARS), return the text as markdown with no other text, make sure to keep all the original content, just translate the words: \n\n{content}"),
        ]
    )
    output_parser = StrOutputParser()
    llm = ChatOpenAI()
    print("Translating markdown document...")
    chain = prompt | llm | output_parser
    prompt_length = len(prompt.format(content=content))
    print(f"Prompt length in tokens: {prompt_length}")
    response = chain.invoke({"content": content})
    return response


def llm_testgen(source_directory):
    model = Together(
        model="mistralai/Mixtral-8x7B-Instruct-v0.1",
        temperature=0.7,
        max_tokens=1000,
        top_k=50,
        together_api_key=os.getenv("TOGETHER_API_KEY"),
    )
    # Provide a template following the LLM's original chat template.
    prompt_template = """
    <s>[INST] Return a c++ unit test file to cover the following c++ source code file. Use Google Test (gtest). Return only the test file contents, no other text.

    File: {code} [/INST] 
    """
    prompt = ChatPromptTemplate.from_template(prompt_template)
    chain = prompt | model | StrOutputParser()

    for filename in os.listdir(source_directory):
        if filename.endswith('.cc') and not filename.endswith('_test_generated.cc'):
            source_filepath = os.path.join(source_directory, filename)
            test_filename = source_filepath.replace(
                '.cc', '_test_generated.cc')
            # if the _test_generated.cc test file does not exist, generate it
            if not os.path.exists(test_filename):
                try:
                    with open(source_filepath, 'r', encoding='utf-8') as file:
                        code = file.read()
                        with Progress(
                            SpinnerColumn(),
                            TextColumn("[progress.description]{task.description}"),
                            transient=True,
                        ) as progress:
                            progress.add_task(description="Using AI to generate code...", total=None)
                            output = chain.invoke({"code": code})
                        print(f"Generated test code for {filename}")
                        with open(test_filename, 'w', encoding='utf-8') as test_file:
                            test_file.write(output)
                except FileNotFoundError:
                    print(f"The source code file {filename} does not exist.")
                except Exception as e:
                    print(
                        f"An error occurred while processing {filename}: {e}")
            # if the _test_generated.cc test file exists, skip generation
            else:
                print(
                    f"Test file {test_filename} already exists. Skipping generation.")

    # Compile and run all generated test code using Bazel
    workspace_dir = create_workspace_directory()
    create_workspace_file(workspace_dir)
    setup_workspace(workspace_dir)
    create_build_file(workspace_dir)
    print("Compiling and running all tests with Bazel...")
    try:
        results = bazel_run_tests(workspace_dir)
        status = results.returncode
        print (f"Status: {status}")
        if status == 1:
            print("Build failed, see error.")
        if status == 3:
            print("Test code compiled successfully, but tests failed, see output.")
        if status == 0:
            print(f"Test code compiled successfully, all tests passed.")
        else:
            print(
                "Compilation or execution failed. Please check the generated test code.")
    except Exception as e:
        print(f"An error occurred: {e}")
