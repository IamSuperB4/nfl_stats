"""This module handles reading files

@Author: Bradley Knorr
@Date: 1/22/2024
"""
import os
from glob import glob


def read_file(file_name: str) -> str:
    """Read a file and get contents

    Args:
        file_name (str): file name/file location

    Returns:
        str: file contents
    """
    with open(file_name, "r", encoding='UTF-8') as file:
        return file.read()

def get_files_in_folder(directory: str = None) -> list:
    """Get all file names in a folder
        - Does not check subfolders

    Args:
        directory (str): path to directory. Defaults to None.

    Returns:
        list: list of files in folder
    """
    directory = get_starting_directory(directory)

    files = [
        f
        for f in os.listdir(directory)
        if os.path.isfile(os.path.join(directory, f))
    ]

    return files

def get_files_in_folder_and_subfolders(directory: str = None) -> list:
    """Get all file names in a folder and subfolders with relative paths

    Args:
        directory (str): path to directory. Defaults to None.

    Returns:
        list: list of files in folder and recursive subfolders
    """
    directory = get_starting_directory(directory)

    return [
        os.path.join(dirpath, f)
        for (dirpath, _, filenames) in os.walk(directory)
        for f in filenames
    ]

def get_files_in_folder_and_subfolders_full_path(directory: str = None) -> list:
    """Get all file names in a folder and subfolders with full paths

    Args:
        directory (str, optional): path to directory. Defaults to None.

    Returns:
        list: list of files in folder and recursive subfolders with full paths
    """
    directory = get_starting_directory(directory)
    files_list = []

    # loop through each file in folder and sub folders
    for root, _, files in os.walk(directory):
        for file in files:
            files_list.append(os.path.join(root, file))

    return files_list

def get_file_names_in_folder_with_filetype(
    directory: str = None, file_extension: str = "*"
) -> list:
    """Return files in a folder with a certain file extension

    Args:
        directory (str, optional): path to directory. Defaults to None.
        file_extension (str, optional): file extension. Defaults to '*'.

    Returns:
        list: list of files in folder and recursive subfolders
    """
    # remove '.' from file extension if it was included in the parameter
    if file_extension.startswith("."):
        file_extension = file_extension[1:]

    full_path = get_full_path(directory)

    file_locations = glob(f"{full_path}/*.{file_extension}")

    return [os.path.basename(f) for f in file_locations]

def get_files_in_folder_with_filetype(
    directory: str = None, file_extension: str = "*"
) -> list:
    """Return files in a folder with a certain file extension

    Args:
        directory (str, optional): path to directory. Defaults to None.
        file_extension (str, optional): file extension. Defaults to '*'.

    Returns:
        list: list of files in folder and recursive subfolders
    """
    file_strings = []

    # remove '.' from file extension if it was included in the parameter
    if file_extension.startswith("."):
        file_extension = file_extension[1:]

    full_path = get_full_path(directory)

    file_locations = glob(f"{full_path}/*.{file_extension}")

    for file_location in file_locations:
        file_strings.append(read_file(file_location))

    return file_strings

@staticmethod
def get_file_names_in_folder_by_file_name_pattern(
    directory: str = None, pattern: str = "*"
) -> list:
    """Return files in a folder where file name matches a pattern

    Args:
        directory (str, optional): path to directory. Defaults to None.
        pattern (str, optional): pattern. Defaults to '*'.

    Returns:
        list: list of files in folder and recursive subfolders
    """
    full_path = get_full_path(directory)

    file_locations = glob(f"{full_path}/{pattern}")

    return [os.path.basename(f) for f in file_locations]

@staticmethod
def get_files_in_folder_by_file_name_pattern(
    directory: str = None, pattern: str = "*"
) -> list:
    """Return files in a folder where file name matches a pattern

    Args:
        directory (str, optional): path to directory. Defaults to None.
        pattern (str, optional): pattern. Defaults to '*'.

    Returns:
        list: list of files in folder and recursive subfolders
    """
    file_strings = []

    full_path = get_full_path(directory)

    file_locations = glob(f"{full_path}/{pattern}")

    for file_location in file_locations:
        file_strings.append(read_file(file_location))

    return file_strings

@staticmethod
def get_starting_directory(directory: str = None) -> str:
    """Get directory to start searches with

    Args:
        directory (str, optional): path to directory. Defaults to None.

    Returns:
        str: starting directory
    """
    # Getting the current work directory (cwd) if no directory was provided
    if directory is None:
        return os.getcwd()

    return directory

@staticmethod
def get_full_path(directory: str = None) -> str:
    """Get directory to start searches with

    Args:
        directory (str, optional): path to directory. Defaults to None.

    Returns:
        str: starting directory
    """
    # Getting the current work directory (cwd) if no directory was provided
    if directory is None:
        return os.getcwd()

    return f"{os.getcwd()}/{directory}"
