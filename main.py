#!/bin/python3
"""
List all of the files in the current Git repository, perfect for piping
"""
import os
import re
from sys import stderr
from timer import Timer


def fetch_git_rootdir(relative_directory: str = "./") -> str | None:
    directory_files = os.listdir(relative_directory)
    absolute_directory = os.path.abspath(relative_directory)

    if ".git" in directory_files:
        return relative_directory
    elif absolute_directory == '/':  # '/' = the root dir in Unix-based systems
        return None
    else:
        return fetch_git_rootdir(relative_directory + "../")


# Return the specifications in the .gitignore file
def get_git_ignore(directory: str) -> list[str]:
    git_ignore_path = os.path.join(directory, ".gitignore")
    git_ignore = []

    if os.path.exists(git_ignore_path):
        git_ignore_raw = open(git_ignore_path).readlines()

        for i in range(len(git_ignore_raw)):
            # Remove blank lines
            if git_ignore_raw[i] != "\n":
                git_ignore.append(git_ignore_raw[i])

        # Remove the ending '\n' from entries
        for i in range(len(git_ignore)):
            git_ignore[i] = git_ignore[i][:-2]

    # An empty list is returned if no .gitignore file found
    return git_ignore


def file_in_git_ignore(file: str, git_ignore: list[str]) -> bool:
    for pattern in git_ignore:
        if pattern in file:
            return True

    return False


def path_has_hidden_dir(directory: str) -> bool:
    hidden_dir_regex = re.compile(r"""
                                     # Case 1
                                     (
                                        .*      # Anything before
                                        /       # Forward slash
                                        \.      # Period
                                        [^/\.]  # Ignore ./ and ../
                                        .*      # Anything after

                                     # Case 2
                                     |
                                        ^\.     # Just a period at the start
                                        [^/\.]  # Ignore ./ and ../
                                        .*      # Anything after
                                     )
                                   """, re.VERBOSE)

    if hidden_dir_regex.match(directory):
        return True
    else:
        return False


def main() -> int:
    timer = Timer()

    git_rootdir = fetch_git_rootdir()
    print(f"fetch_git_root_dir completed in {timer.break_lap()} s")

    if git_rootdir is None:
        stderr.write("ERROR: You are not in a git repository.\n")
        return 1

    git_ignore = get_git_ignore(git_rootdir)
    print(f"get_git_ignore completed in {timer.break_lap()} s")

    # List all files from the current git directory recursively
    for pwd, dirs, files in os.walk(git_rootdir, topdown=False):

        # Improve performance by checking if the working directory
        # is hidden or in .gitignore right away
        if file_in_git_ignore(pwd, git_ignore) or \
           path_has_hidden_dir(pwd):
            continue

        for file_name in files:
            # [2:] index to remove ./ in start of file
            current_file = os.path.join(pwd, file_name)[2:]

            if not file_in_git_ignore(current_file, git_ignore) and \
               not path_has_hidden_dir(current_file):
                print(current_file)

    return 0


if __name__ == "__main__":
    main()
