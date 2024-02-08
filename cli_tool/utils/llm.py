import typer
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_together import Together
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from .install_test_lib import install_gtest
from .install_test_lib import bazel_run_tests
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


def llm_testgen(test_filepath):
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
    test_filename = test_filepath.replace('.cc', '_generated.cc')
    if not os.path.exists(test_filename):
        try:
            with open(test_filepath, 'r', encoding='utf-8') as file:
                code = file.read()
                output = chain.invoke({"code": code})
                print("Generated test code:", code)
                with open(test_filename, 'w', encoding='utf-8') as test_file:
                    test_file.write(output)
        except FileNotFoundError:
            print("The source code file does not exist.")
        except Exception as e:
            print(f"An error occurred: {e}")
    else:
        print(f"Test file {test_filename} already exists. Skipping generation.")
    
    # Compile and run the generated test code
    print("Compiling and running test...")
    # compile_command = f'g++ -std=c++14 -o test_output {test_filename} -lgtest -lpthread && ./test_output'
    
    try:
        # Attempt to compile and run the generated test code
        # compile_status = os.system(compile_command)
        compile_status = bazel_run_tests(test_filename.replace('.cc', ''))
        if compile_status != 0:
            # print("Compilation failed, attempting to install Google Test...")
            # install_gtest()
            # print("Re-attempting compilation...")
            # compile_status = os.system(compile_command)
            print("Compilation failed, see error.")
        if compile_status == 0:
            print(f"Test code compiled and ran successfully.")
        else:
            print("Compilation or execution failed. Please check the generated test code.")
    except Exception as e:
        print(f"An error occurred: {e}")



