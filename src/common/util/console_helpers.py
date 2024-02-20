"""
common > util > console_helpers

Contains helper functions for interacting with the script through the
console, which may assist in debugging, or using the script with a controller
that doesn't have as many built-in commands.

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""

__all__ = [
    'help',
    'credits'
]

import consts

from typing import Callable
from .misc import _NoneNoPrintout, NoneNoPrintout


def printReturn(func: Callable) -> Callable:
    """
    Wrap a function so that its return is printed instead of being returned to
    FL Studio

    Useful for interface functions, as FL Studio removes newlines which is
    kinda yucky

    ### Args:
    * `func` (`Callable[[], str]`): Function

    ### Returns:
    * `Callable[[], _NoneNoPrintout]`: Wrapped function
    """
    def wrapper(*args, **kwargs) -> _NoneNoPrintout:
        ret = func(*args, **kwargs)
        print(ret)
        return NoneNoPrintout
    return wrapper


class ConsoleCommand:
    """
    Allows a printout to be generated when a user types a command
    """

    def __init__(self, printout: str) -> None:
        self.printout = printout

    def __repr__(self) -> str:
        print(self.printout)
        return ''

    def __call__(self) -> None:
        print(self)


help = ConsoleCommand(
    f"Universal Controller Script\n"
    f"Version: {consts.getVersionString()}\n"
    f"---------------------------\n"
    f"For documentation, visit the project's GitHub:\n"
    f"  {consts.WEBSITE}\n"
    f"To speak to a human, join our Discord server:\n"
    f"  {consts.DISCORD}\n"
    f"---------------------------\n"
    f"List of commands (enter into the console to use it):\n"
    f" * help(): display this message\n"
    f" * log(): log a message\n"
    f"    * log.recall([opt] category): recall log entries from a category\n"
    f"    * log.inspect(entry_number): print info about a log entry\n"
    f" * credits(): print credits for the script\n"
    f" * reset(): reset the script and reload modular components\n"
    f" * pluginParamCheck(): launch the plugin parameter checker interface\n"
)

# Damn this is an awful way of formatting this, but I can't think of anything
# better
_newline = '\n'
_credit_str = "\n".join(
    f"{key}:{_newline}{_newline.join([f' * {p}' for p in value])}"
    for key, value in consts.AUTHORS.items()
)
credits = ConsoleCommand(
    f"Credits:\n"
    f"{_credit_str}\n"
    f"---------------------------\n"
    f"This project is free and open source, under the GNU GPL v3 License.\n"
    f"A copy of this is available in the file 'LICENSE'.\n"
)
