
"""This module is for styling text for the console

@Author: Bradley Knorr
@Date: 8/31/2023
"""

from colorama import Fore, Style

def add_color(text: str, color: str) -> str:
    """Add color to text in the console

    Args:
        text (any): text to add color to
        color (str): color

    Returns:
        str: text with color
    """
    colors_dict: dict = {
        "BLACK": Fore.BLACK,
        "RED": Fore.RED,
        "GREEN": Fore.GREEN,
        "YELLOW": Fore.YELLOW,
        "BLUE": Fore.BLUE,
        "MAGENTA": Fore.MAGENTA,
        "CYAN": Fore.CYAN,
        "WHITE": Fore.WHITE,
        "RESET": Fore.RESET,
        "LIGHTBLACK_EX": Fore.LIGHTBLACK_EX,
        "LIGHTRED_EX": Fore.LIGHTRED_EX,
        "LIGHTGREEN_EX": Fore.LIGHTGREEN_EX,
        "LIGHTYELLOW_EX": Fore.LIGHTYELLOW_EX,
        "LIGHTBLUE_EX": Fore.LIGHTBLUE_EX,
        "LIGHTMAGENTA_EX": Fore.LIGHTMAGENTA_EX,
        "LIGHTCYAN_EX": Fore.LIGHTCYAN_EX,
        "LIGHTWHITE_EX": Fore.LIGHTWHITE_EX,
    }

    return colors_dict[color.upper()] + str(text) + Style.RESET_ALL

def add_style(text: str) -> str:
    """Add styles to text in the console

    Args:
        text (any): text to add color to
        styles (list): color
        color (str): color

    Returns:
        str: text with styling
    """
    return text
