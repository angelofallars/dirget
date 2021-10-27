#!/bin/python3
"""Recursively search directories until a .git folder is found,
   then list the files with `ls -R`"""
import os
import re

mypath = "./"


def path_has_hidden_dir(directory: str) -> bool:
    hidden_dir_regex = re.compile(r".*/\.[^/\.].*")

    if hidden_dir_regex.match(directory):
        return True
    else:
        return False


# Search up until a folder with .git is found
while True:
    current_dir_files = os.listdir(mypath)

    if ".git" in current_dir_files:
        break
    else:
        # Go up one directory
        mypath += "../"


# List all files from the current git directory recursively
for pwd, dirs, files in os.walk(mypath, topdown=False):
    if path_has_hidden_dir(pwd):
        continue

    for name in files:
        if name[0] != ".":
            print(os.path.join(pwd, name)[2:])  # Start from 2: to remove ./
