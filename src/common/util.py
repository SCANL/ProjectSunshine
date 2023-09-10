import configparser
import logging
import os
from builtins import filter
from pathlib import Path
from typing import Any, List

import pandas

from src.common.error_handler import handle_error, ErrorSeverity
from src.model.input import Input

log = logging.getLogger(__name__)


def get_config_setting(section: str, name: str) -> str:
    """
        Retrieve a specific configuration value from a configuration file.

        Args:
            section (str): The name of the section in the configuration file.
            name (str): The name of the configuration setting within the section.

        Returns:
            str: The requested configuration value.
    """
    directory_path = os.path.dirname(os.path.realpath(__file__))
    config_path = os.path.join(directory_path, 'config.txt')

    config = configparser.ConfigParser()
    config.read(config_path)
    try:
        return config[section][name]
    except:
        log.exception(msg='Config setting %s not available.' %
                      str(section + name), exc_info=True)


def get_file_name(file_path: str) -> str:
    """
        Extract the file name from a given file path.

        Args:
            file_path (str): The full path to the file, including its name.

        Returns:
            str: The file name extracted from the file path.
    """
    head, tail = os.path.split(file_path)
    return tail


def remove_list_nestings(l: List[Any]) -> List[Any]:
    """
        Flatten a nested list, removing all levels of nesting.

        Args:
            l (List[Any]): The nested list to be flattened.

        Returns:
            List[Any]: A flat list with all elements from the input list.
    """
    output = []
    for i in l:
        if type(i) == list:
            remove_list_nestings(i)
        else:
            output.append(i)
    return output


def get_supported_file_extensions() -> List[str]:
    """
        Get a list of supported file extensions.

        Returns:
            List[str]: A list of supported file extensions.
    """
    return ['.java', '.cs']


def read_input(path_string: str) -> List[Any]:
    """
        Read and process input data from a CSV file.

        Args:
            path_string (str): The path to the input CSV file.

        Returns:
            List[Any]: A list of Input objects, each representing a file and associated metadata.
    """
    input_data = pandas.read_csv(path_string)
    if len(input_data) == 0:
        error_message = "Input CSV file cannot be empty: \'%s\'" % str(
            path_string)
        handle_error('Main', error_message, ErrorSeverity.Critical, True)

    files = []
    file_extensions = get_supported_file_extensions()
    for i, item in input_data.iterrows():
        path = Path(item[0])
        path_string = str(path)

        if os.path.isdir(path_string):
            source_files = [p for p in path.rglob(
                '*') if p.suffix in file_extensions]
            for file in source_files:
                input_item = Input(str(file), item[1], item[2])
                files.append(input_item)

        elif os.path.isfile(path_string):
            if path_string.lower().endswith(tuple(file_extensions)):
                input_item = Input(path_string, item[1], item[2])
                files.append(input_item)
        else:
            error_message = "Invalid files provided in input CSV file: \'%s\'" % str(
                path_string)
            handle_error('Main', error_message, ErrorSeverity.Critical, True)

    if len(files) == 0:
        error_message = "Invalid files provided in input CSV file: \'%s\'" % str(
            path_string)
        handle_error('Main', error_message, ErrorSeverity.Critical, True)

    return files
