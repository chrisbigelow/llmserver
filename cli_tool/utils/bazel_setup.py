import subprocess
import os
import shutil
import os
import shutil
import subprocess
import glob


def create_workspace_directory():
    workspace_dir = os.path.abspath("my_workspace")
    # Create the workspace directory if it doesn't exist
    os.makedirs(workspace_dir, exist_ok=True)

    # Create a subdirectory for source files within the workspace
    src_dir = os.path.join(workspace_dir, "src")
    os.makedirs(src_dir, exist_ok=True)
    return workspace_dir


def create_workspace_file(workspace_dir):
    # Change the current directory to the workspace directory
    os.chdir(workspace_dir)

    # Create the WORKSPACE file
    with open("WORKSPACE", "w") as workspace_file:
        workspace_file.write("""
load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_archive")

http_archive(
  name = "com_google_googletest",
  urls = ["https://github.com/google/googletest/archive/refs/tags/v1.14.0.zip"],
  strip_prefix = "googletest-1.14.0",
)
""")


def create_build_file(workspace_dir):
    src_dir = os.path.join(workspace_dir, "src")
    build_file_path = os.path.join(src_dir, "BUILD")

    cc_libraries = []
    cc_tests = []

    # Iterate over files in src_dir to categorize them
    for filename in os.listdir(src_dir):
        if filename.endswith(".cc") and not filename.endswith("_test_generated.cc"):
            # For .cc files, add to cc_library. Assume corresponding .h exists.
            name = filename[:-3]  # Strip .cc extension for name
            cc_libraries.append(f"""
cc_library(
    name = "{name}",
    srcs = ["{filename}"],
    hdrs = ["{name}.h"],
)
""")
        elif filename.endswith("_test_generated.cc"):
            # For _test_generated.cc files, add to cc_test
            # Strip _test_generated.cc extension for name
            name = filename[:-len("_test_generated.cc")]
            cc_tests.append(f"""
cc_test(
    name = "{name}_test",
    size = "small",
    srcs = ["{filename}"],
    deps = [
        ":{name}",
        "@com_google_googletest//:gtest_main",
    ],
)
""")
    # Combine all library and test entries into the build file content
    build_file_content = "\n".join(cc_libraries + cc_tests)
    # Write the combined content to the BUILD file
    with open(build_file_path, "w") as build_file:
        build_file.write(build_file_content)


def setup_workspace(workspace_dir):
    print("Setting up workspace...")
    # Check if the current working directory is the workspace_dir
    current_working_dir = os.path.abspath(os.getcwd())
    workspace_dir_abs = os.path.abspath(workspace_dir)
    
    if current_working_dir == workspace_dir_abs:
        os.chdir("..")  # Move one level up in the directory structure
    src_dir = os.path.join(workspace_dir, "src")
    os.makedirs(src_dir, exist_ok=True)  # Ensure the src directory exists

    # Copy all .cc and .h files to the src_dir
    for extension in ['.cc', '.h']:
        print("Current working directory:", os.getcwd())
        for file_path in glob.glob(f"*{extension}"):
            print("FILE PATH: ", file_path)
            destination_path = os.path.join(
                src_dir, os.path.basename(file_path))
            if os.path.abspath(file_path) != os.path.abspath(destination_path):
                print(f"Copying {file_path} to {destination_path}...")
                shutil.copy(file_path, destination_path)
            else:
                print(
                    f"Skipping copy as source and destination are the same for {file_path}")


def bazel_run_tests(workspace_dir):
    try:
        # Run all test targets within the workspace
        results = subprocess.run(["bazel", "test", "--cxxopt=-std=c++14", "..."],
                                 check=True, cwd=workspace_dir)
        print("All tests ran successfully.")
        return results
    except subprocess.CalledProcessError as e:
        print("Failed to run tests.")
        print(e)
