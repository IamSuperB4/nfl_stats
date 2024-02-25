"""This module handles different types of string comprehension

@Author: Bradley Knorr
@Date: 1/22/2024
"""
import re

def get_index_of_parenthesis(expression: str, starting_index=0):
    """Find the index of the closing parenthesis for a formula

    Args:
        expression (string): expression
        starting_index (int, optional): _description_. Defaults to 0.

    Returns:
        int: index of the closing parenthesis for a formula, -1 if no closing parentheses
    """
    level = 0

    index_of_opening_parenthesis = expression.find("(")

    for index, char in enumerate(expression[starting_index:]):
        # go down one level if open parenthesis found
        if char == "(":
            level += 1
        # go up one level if closing parenthesis is found
        if char == ")":
            level -= 1
            if level == 0:
                return index_of_opening_parenthesis, index + starting_index

    return index_of_opening_parenthesis, -1

def is_string_within_quotes(
    string: str, starting_index: int, ending_index: int
) -> bool:
    """If string is inside double quotes

    Args:
        string (str): string to check
        starting_index (int): starting char index
        ending_index (int): ending char index

    Returns:
        bool: if string is inside double quotes
    """
    # remove the substring from the full string using indices
    rest_of_string = remove_substring_by_index(
        string, starting_index, ending_index
    )

    inside_quotes = False

    # loop through all characters in rest of string
    for index, char in enumerate(rest_of_string):
        # once it hits the index where the substring was removed, return if it is inside quotes
        if index >= starting_index:
            return inside_quotes
        # if quotes are found, reverse status of inside_quotes
        if char == '"':
            inside_quotes = not inside_quotes

    return False

def is_string_within_parenthesis(
    string: str, starting_index: int, ending_index: int
) -> bool:
    """If string is inside parenthesis

    Args:
        string (str): string to check
        starting_index (int): starting char index
        ending_index (int): ending char index

    Returns:
        bool: if string is inside parenthesis
    """
    # remove the substring from the full string using indices
    rest_of_string = remove_substring_by_index(
        string, starting_index, ending_index
    )

    # level of parenthesis
    level = 0

    for index, char in enumerate(rest_of_string):
        # once it hits the index where the substring was removed, return if it is
        #   inside parenthesis (level is more than 0)
        if index >= starting_index:
            return level > 0
        # if '(' is found, reverse add a level to the parenthesis
        if char == "(":
            level += 1
        # if ')' is found, reverse subtract a level to the parenthesis
        if char == ")":
            level -= 1

    return False

def remove_substring_by_index(
    string: str, starting_index: int, ending_index: int
) -> str:
    """Remove a substring from a string between 2 indices

    Args:
        string (str): string to remove substring from
        starting_index (int): starting index
        ending_index (int): ending index

    Returns:
        str: string with substring removed
    """
    string = str(string)

    first_part = string[:starting_index]
    second_part = string[ending_index:]

    return first_part + second_part

def indices_of_char_not_in_quotes(string: str, search_char: chr) -> list:
    """Get indices of specified character that are not in quotes

    Args:
        string (str): string
        search_char (chr): character to search for

    Returns:
        list: list of indices where character is found in string and not within quotes
    """
    indices_of_string_not_inside_quotes = []
    inside_quotes = False

    for index, char in enumerate(string):
        if char == search_char and not inside_quotes:
            indices_of_string_not_inside_quotes.append(index)
        if char == '"':
            inside_quotes = not inside_quotes

    return indices_of_string_not_inside_quotes

def indices_of_char_not_in_parenthesis(string: str, search_char: chr) -> list:
    """Get indices of specified character that are not within parenthesis

    Args:
        string (str): string
        search_char (chr): character to search for

    Returns:
        list: list of indices where character is found in string and not within parenthesis
    """
    indices_of_string_not_inside_parenthesis = []
    level = 0

    for index, char in enumerate(string):
        if char == search_char and level == 0:
            indices_of_string_not_inside_parenthesis.append(index)
        if char == "(":
            level += 1
        if char == ")":
            level -= 1

    return indices_of_string_not_inside_parenthesis

def split_string_by_indices(string: str, indices: list, delimiter_length=1) -> list:
    """Split string on indices, leaving leaving character in tact

    Args:
        string (str): string to split
        indices (list): list of indices to split on
        delimiter_length (int, optional): length of delimiter string where
            splits are happening. Defaults to 1.

    Returns:
        list: list of substrings from split
    """
    # Creating an empty list to store the parts
    parts = []

    # Iterating over the string
    for i in enumerate(indices):
        # Splitting the string at the current index
        if i == 0:
            parts.append(string[: indices[i]])
        else:
            parts.append(string[indices[i - 1] + delimiter_length : indices[i]])

    # Adding the remaining part of the string
    if len(indices) > 0 and len(string) >= indices[-1] + delimiter_length:
        parts.append(string[indices[-1] + delimiter_length :])

    return parts

def split_string_by_char_not_in_quotes(string: str, char: chr) -> list:
    """Split string by a character that is not in quotes

    Args:
        string (str): string to split
        char (chr): delimiter

    Returns:
        list: list of substrings from split
    """
    indices = indices_of_char_not_in_parenthesis(string, char)

    return split_string_by_indices(string, indices)

def split_string_by_char_not_in_parenthesis(string: str, char: chr) -> list:
    """Split string by a character that is not in parenthesis

    Args:
        string (str): string to split
        char (chr): delimiter

    Returns:
        list: list of substrings from split
    """
    indices = indices_of_char_not_in_parenthesis(string, char)

    return split_string_by_indices(string, indices)

def split_string_by_char_not_in_parenthesis_or_quotes(
    string: str, char: chr
) -> list:
    """Split string by a character that is not in parenthesis or quotes

    Args:
        string (str): string to split
        char (chr): delimiter

    Returns:
        list: list of substrings from split
    """
    # get indices of char not in quotes
    indices_in_quotes = indices_of_char_not_in_quotes(string, char)

    # get indices of char not in parenthesis
    indices_in_parenthesis = indices_of_char_not_in_parenthesis(string, char)

    # filter list to just indices that are not in quotes OR parenthesis
    indices = list(set(indices_in_quotes) & set(indices_in_parenthesis))

    # put indices back in order from after filter
    indices.sort()

    return split_string_by_indices(string, indices)

def replace_mulitiple_substrings(
    string: str, replacements: dict, ignore_case=False
) -> str:
    """Given a string and a replacement map, it returns the replaced string

    Args:
        string (str): string to execute replacements on
        replacements (dict): replacement dictionary {value to find: value to replace}
        ignore_case (bool, optional): whether the match should be case insensitive.
            Defaults to False.

    Returns:
        str: replaced string
    """
    # if dictionary exists
    if not replacements:
        return string

    # If case insensitive, we need to normalize the old string so that later a replacement
    # can be found. For instance with {"HEY": "lol"} we should match and find a replacement
    #   for "hey", "HEY", "hEy", etc.
    if ignore_case:

        def normalize_old(s: str):
            return s.lower()

        re_mode = re.IGNORECASE

    else:

        def normalize_old(s: str):
            return s

        re_mode = 0

    replacements = {normalize_old(key): val for key, val in replacements.items()}

    # Place longer ones first to keep shorter substrings from matching where the longer ones
    #   should take place
    # For instance given the replacements {'ab': 'AB', 'abc': 'ABC'} against the string
    #   'hey abc', it should produce 'hey ABC' and not 'hey ABc'
    rep_sorted = sorted(replacements, key=len, reverse=True)
    rep_escaped = map(re.escape, rep_sorted)

    # Create a big OR regex that matches any of the substrings to replace
    pattern = re.compile("|".join(rep_escaped), re_mode)

    # For each match, look up the new string in the replacements,
    #   being the key the normalized old string
    return pattern.sub(
        lambda match: replacements[normalize_old(match.group(0))], string
    )

def strip_whitespace(text: str, keep_single_spaces=True) -> str:
    """Strip excess whitespace from a string

    Args:
        text (string): text to remove excess whitespace

    Returns:
        string: text without excess whitespace
    """
    lst = text.split('"')
    for i, item in enumerate(lst):
        if not i % 2:
            lst[i] = re.sub(r"\s+", " " if keep_single_spaces else "", item)
    return '"'.join(lst)
