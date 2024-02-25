"""Custom version of a logger for the console
"""

from styles import Text


class ConsoleWriter:
    """
    This module handles printing debug information to the console

    Import:
        from helper import Console_Writer

    Example:
        initialization:
            console_writer = Console_Writer(1)

        usage:
            console_writer.print()

    Attributes:
        level (string): Which server to connect to (ie SalesTool or EASOP)
        tab_level (string): Which database to connect to.
            Or Experlogix environment or EASOP database
        tabbed_over (sqlalchemy MockConnection): sqlalchemy db engine

    @Author: Bradley Knorr
    @Date: 11/23/2023
    @Credit:
    """

    def __init__(self, debug_level: int):
        """Initialzes console debugger

        Args:
            level (int): level of debugging
        """
        self.level = debug_level
        self.tab_level = 0
        self.tabbed_over = False

    def print(self, level, text_list, color_list=list, new_line=True):
        """Print to the console, with text color for each section of text

        Args:
            level (int): debug level
            text_list (any|list): text or list of text strings to print to line
            color_list (any|list): matching list to text_list to print text a color
            new_line (bool, optional): whether to print a new line after line. Defaults to True.
        """
        if level >= self.level:
            # if lists aren't a list, convert to a list
            if not isinstance(text_list, list):
                text_list = [text_list]
            elif not isinstance(color_list, list):
                color_list = [color_list]

            # if console is not tabbed over, tab over to tab level
            if not self.tabbed_over:
                print("\t" * self.level, end="")

            # print each text string the specified color in color_list
            for i, text in enumerate(text_list):
                # if there is a color for text, print that color
                if len(color_list) > i and color_list[i] is not None:
                    print(Text.add_color(text, color_list[i]), end="")
                # print text to console without color
                else:
                    print(text, end="")

            # if new line specified, print new line
            if new_line:
                self.print_new_line(level)

    def print_new_line(self, level: int):
        """Print a new line

        Args:
            level (int): debug level
        """
        if level >= self.level:
            print()
            self.tabbed_over = False

    def print_tab_over(self, level: int, add_tabs: int = 0):
        """Print tabs at beginning of new line in console, or one new tab on current line

        Args:
            level (int): debug level
            tab_over_once (bool): whether to only tab over once because this line has already
                been tabbed over
        """
        if level >= self.level:
            if not self.tabbed_over:
                print("\t" * self.level, end="")
                self.tabbed_over = True
            elif add_tabs > 0:
                print("\t" * add_tabs, end="")

    def move_tab_level(self, level: int, increase_tab_level=1):
        """Increase tab level by specified amount. Decrease tab level with a negative number

        Args:
            level (int): debug level
            increase_tab_level (int, optional): how much to increase tab level. Defaults to 1.
        """
        if level >= self.level:
            self.tab_level += increase_tab_level

            # tab level can't be negative
            if self.tab_level < 0:
                self.tab_level = 0
            if increase_tab_level > 0:
                self.print_tab_over(level, True)
