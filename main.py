#!/bin/python3
"""
List all of the files in the current Git repository, perfect for piping
"""
import os
import re


def fetch_git_rootdir(relative_directory: str = "./") -> str | None:
    absolute_directory = os.path.abspath(relative_directory)
    directory_files = os.listdir(relative_directory)

    if ".git" in directory_files:
        return relative_directory
    # When we reach the root folder '/', return None
    elif absolute_directory == '/':
        return None
    else:
        return fetch_git_rootdir(relative_directory + "../")


def find_gitignore_patterns(git_root_directory: str) -> list[str]:
    gitignore_path = os.path.join(git_root_directory, ".gitignore")

    if os.path.exists(gitignore_path):
        with open(gitignore_path) as gitignore_file:
            gitignore_patterns = [pattern[:-2] for pattern in  # [:-2] removes
                                                               # trailing '\n'
                                  gitignore_file.readlines()
                                  if pattern[:-2] != ""]  # Remove blank lines

        return gitignore_patterns

    # If no .gitignore file found, return an empty list
    else:
        return []


def path_in_gitignore(file: str, gitignore: list[str]) -> bool:
    for pattern in gitignore:
        if pattern in file:
            return True
    return False


def path_has_hidden_dir(path: str) -> bool:
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
    path_is_hidden = hidden_dir_regex.match(path)

    if path_is_hidden:
        return True
    else:
        return False


def list_files_recursively(root_directory: str, gitignore: list[str]) -> None:
    for current_dir, dirs, files in os.walk(root_directory):

        # Boost performance by removing the hidden/ignored folders
        # so os.walk doesn't access them and waste time
        i = 0
        while i < len(dirs):
            directory = "".join([dirs[i], "/"])

            if path_in_gitignore(directory, gitignore) or \
               path_has_hidden_dir(directory):

                dirs.remove(dirs[i])
                continue

            i += 1

        # [2:] index to remove ./ in start of file
        file_relative_paths = [os.path.join(current_dir, file)[2:]
                               for file in files]

        for file in file_relative_paths:
            if path_in_gitignore(file, gitignore) or \
               path_has_hidden_dir(file):
                continue
            else:
                print(file)


def main() -> int:
    root_dir = fetch_git_rootdir()

    if root_dir is None:
        root_dir = "./"

    gitignore_patterns = find_gitignore_patterns(root_dir)

    list_files_recursively(root_dir, gitignore_patterns)

    return 0


if __name__ == "__main__":
    main()
