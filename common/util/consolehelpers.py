"""
common > util > consolehelpers

Contains helper functions for interacting with the script through the
console, which may assist in debugging.
"""

__all__ = [
    'help',
    'credits',
    'log'
]

import common

from logger import log

class ConsoleCommand:
    """
    Allows a printout to be generated when a user types a command
    """
    
    def __init__(self, printout: str) -> None:
        self.printout = printout
    
    def __repr__(self) -> str:
        return self.printout

    def __call__(self) -> None:
        print(self)

help = ConsoleCommand(
    f"Universal Controller Script\n"
    f"Version: {common.consts.getVersionString()}\n"
    f"---------------------------\n"
    f"For documentation, visit the project's GitHub:\n"
    f"  {common.consts.WEBSITE}\n"
    f"To speak to a human, join our Discord server:\n"
    f"  {common.consts.DISCORD}\n"
    f"---------------------------\n"
    f"List of commands (enter into the console to use it):\n"
    f" * help: display this message\n"
    f" * log:\n"
    f"    * log.recall(): recall log entries\n"
    f"    * log.details(entry_number): print info about a log entry\n"
    f" * credits: print credits for the script\n"
)

# Damn this is an awful way of formatting this, but I can't think of anything
# better
_credit_str = "\n".join(f"{key}:\n{'\n'.join([f' * {p}' for p in value])}" for key, value in common.consts.AUTHORS)
credits = ConsoleCommand(
    f"Credits:\n"
    f"{_credit_str}\n"
    f"---------------------------\n"
    f"This project is free and open source, under the GNU GPL v3 License.\n"
    f"A copy of this license is available in the file 'LICENSE'.\n"
)
