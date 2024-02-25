"""This module handles handling different datatypes, and does this in 2 primary ways:
        1. Datatype conversions
        2. Datatype checks

    @Author: Bradley Knorr
    @Date: 1/22/2024
"""

import numbers
from custom_errors import DataTypeError

###################################################################################################
#
# Conversions
#
###################################################################################################

def convert_string_to_unknown_datatype(
    value: str, string_in_quotes=False
) -> str | numbers.Number | bool:
    """Convert a string to an unknown datatype

    Args:
        value (str): string to convert
        string_in_quotes (bool, optional): whether strings are in quotes. Defaults to True.

    Returns:
        str|numbers.Number|bool: string converted to proper datatype
    """
    # if string is in quotes, remove quotes
    if string_in_quotes:
        # if string, remove quotes
        return value.replace('"', "")

    # if bool, convert to a bool
    if string_is_bool(value):
        return convert_string_to_bool(value)

    # if number, convert to a number
    if string_is_number(value):
        return convert_string_to_number(value)

    # value is a string, so return as is
    return value

def convert_string_to_number(value: str) -> numbers.Number:
    """Convert a string to a number

    Args:
        value (str): string value to convert to number

    Raises:
        DataTypeError: string cannot be converted to a number

    Returns:
        numbers.Number: numerical value
    """
    # if value is a number wrapped in a string, return numerical value
    if string_is_number(value):
        number = float(value)

        # if property is an int set property to a int
        if number.is_integer():
            return int(number)

        return number

    raise DataTypeError(value, "cannot be converted to type", "Number")

def convert_string_to_bool(value: str) -> bool:
    """Convert a string to a bool

    Args:
        value (str): string value to convert to bool

    Raises:
        DataTypeError: string cannot be converted to a bool

    Returns:
        bool: boolean value
    """
    # if value is a boolean wrapped in a string, return boolean value
    if isinstance(value, str) and (
        value.lower() == "true" or value.lower() == "false"
    ):
        return value.lower() == "true"

    raise DataTypeError(value, "cannot be converted to type", "bool")

###################################################################################################
#
# Checks
#
###################################################################################################

def string_is_number(value: str) -> bool:
    """Check if string is a number

    Args:
        value (str): string value

    Returns:
        bool: if string is a number
    """
    try:
        float(value)
        return True
    except ValueError:
        return False

def string_is_bool(value: str) -> bool:
    """Check if string is a boolean

    Args:
        value (str): string value

    Returns:
        bool: if string is a boolean
    """
    return value.lower() == "true" or value.lower() == "false"
