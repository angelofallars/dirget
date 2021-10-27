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


def main() -> int:
    current_dir = "./"

    # Search up until a folder with .git is found
    while True:
        current_dir_files = os.listdir(current_dir)

        if ".git" in current_dir_files:
            break
        else:
            # Go up one directory
            current_dir += "../"

        if os.getcwd() == '/':
            stderr.write("ERROR: You are not in a git repository.\n")
            return 1

    # List all files from the current git directory recursively
    for pwd, dirs, files in os.walk(current_dir, topdown=False):
        # TODO - Ignore files listed in .gitignore

        if path_has_hidden_dir(pwd):
            continue

        for name in files:
            # Ignore hidden files that start with .
            if name[0] != ".":
                print(os.path.join(pwd, name)[2:])  # [2:] index to remove ./

    return 0


if __name__ == "__main__":
    main()
