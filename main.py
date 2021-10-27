#!/bin/python3
"""Recursively search directories until a .git folder is found,
   then list the files with `ls -R`"""
import os
import re
from sys import stderr


def path_has_hidden_dir(directory: str) -> bool:
    hidden_dir_regex = re.compile(r".*/\.[^/\.].*")
    if hidden_dir_regex.match(directory):
        return True
    else:
        return False


# Return the specifications in the .gitignore file if it exists,
# otherwise return none
def get_git_ignore(directory: str) -> list[str] | None:
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

        return git_ignore

    else:
        return None


def fetch_git_rootdir(relative_directory: str = "./") -> str | None:
    directory_files = os.listdir(relative_directory)
    absolute_directory = os.path.abspath(relative_directory)

    if ".git" in directory_files:
        return relative_directory
    elif absolute_directory == '/':  # '/' = the root dir in Unix-based systems
        return None
    else:
        return fetch_git_rootdir(relative_directory + "../")


def main() -> int:
    git_rootdir = fetch_git_rootdir()

    if git_rootdir is None:
        stderr.write("ERROR: You are not in a git repository.\n")
        return 1

    git_ignore = get_git_ignore(git_rootdir)

    # List all files from the current git directory recursively
    for pwd, dirs, files in os.walk(git_rootdir, topdown=False):

        if path_has_hidden_dir(pwd):
            continue

        for name in files:
            # [2:] index to remove ./ in start of file
            current_file_dir = os.path.join(pwd, name)[2:]
            file_is_hidden = False

            # Ignore files listed in .gitignore
            if git_ignore is not None:
                for ignore_file in git_ignore:
                    if ignore_file in current_file_dir:
                        file_is_hidden = True
                        break

                if file_is_hidden:
                    continue

            # Ignore hidden files that start with .
            if name[0] != ".":
                print(current_file_dir)

    return 0


if __name__ == "__main__":
    main()
