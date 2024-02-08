import subprocess
import os
import shutil  # Import shutil for directory removal


import os
import shutil
import subprocess


def setup_workspace(workspace_dir, test_name, source_name):
    # Create the workspace directory if it doesn't exist
    os.makedirs(workspace_dir, exist_ok=True)

    # Create a subdirectory for source files within the workspace
    src_dir = os.path.join(workspace_dir, "src")
    os.makedirs(src_dir, exist_ok=True)

    # Assuming the target test files are in the current directory, move them to src_dir
    for extension in ['.cc', '.h']:  # Check for both C++ source and header files
        test_file_name = f"{test_name}{extension}"
        if os.path.exists(test_file_name):
            print("Found target test file to move...")
            shutil.move(test_file_name, os.path.join(src_dir, test_file_name))

    # Assuming the target source files are in the current directory, move them to src_dir
    for extension in ['.cc', '.h']:  # Check for both C++ source and header files
        source_file_name = f"{source_name}{extension}"
        if os.path.exists(source_file_name):
            print("Found target source file to move...")
            shutil.move(source_file_name, os.path.join(
                src_dir, source_file_name))

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


def create_build_file_small_test(workspace_dir, test_name, source_name):
    src_dir = os.path.join(workspace_dir, "src")
    build_file_path = os.path.join(src_dir, "BUILD")
    with open(build_file_path, "w") as build_file:
        build_file_content = f"""
cc_library(
    name = "{source_name}",
    srcs = ["{source_name}.cc"],
    hdrs = ["{source_name}.h"],
)

cc_test(
    name = "{test_name}",
    size = "small",
    srcs = ["{test_name}.cc"],
    deps = [
        ":{source_name}",
        "@com_google_googletest//:gtest_main",
    ],
)
"""
        build_file.write(build_file_content)


def bazel_run_tests(test_target_name):
    source_target_name = test_target_name.replace('_generated', '')
    workspace_dir = os.path.abspath("my_workspace")
    setup_workspace(workspace_dir, test_target_name, source_target_name)
    create_build_file_small_test(workspace_dir, test_target_name, source_target_name)
    try:
        subprocess.run(["bazel", "test", "--cxxopt=-std=c++14",
                        f"//src:{test_target_name}"], check=True, cwd=workspace_dir)
        print("Test completed successfully.")
    except subprocess.CalledProcessError as e:
        print("Failed to run tests.")
        print(e)
