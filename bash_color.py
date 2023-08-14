""" Provides ways to colorize strings in the terminal. """

from dataclasses import dataclass


@dataclass
class Color:
    """ANSI escape sequences for colors."""

    PURPLE = "\033[95m"
    CYAN = "\033[96m"
    DARKCYAN = "\033[36m"
    BLUE = "\033[94m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    DARKGREY = "\033[90m"
    END = "\033[0m"


def colorize(string: str, color: Color):
    """Colorize a string."""
    return color + string + Color.END
