"""
common > logger > logitem

Contains LogItem, a class used to represent an entry in the script's log

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]
"""

import time
# import traceback

from .verbosity import Verbosity

class LogItem:
    """
    Internal representation of an item that has been logged
    """
    def __init__(
        self,
        category: str,
        message: str,
        details: str,
        verbosity: Verbosity,
        index: int
    ) -> None:
        """
        Create a LogItem

        ### Args:
        * `category` (`str`): category to log under
        * `message` (`str`): message to log
        * `details` (`str`): detailed message if required
        * `verbosity` (`Verbosity`): verbosity to log at
        * `index` (`int`): index of this log item
        """
        self.category = category
        self.message = message
        self.details = details
        self.verbosity = verbosity
        self.index = index
        self.time = time.localtime()
        self.trace = None # traceback.extract_stack(limit=-2)
    
    @staticmethod
    def _formatTime(time) -> str:
        """
        Static helper function for formatting time as a string

        ### Args:
        * `time` (`time`): time to format

        ### Returns:
        * `str`: formatted time
        """
        return f"{time.tm_hour:02}:{time.tm_min:02}:{time.tm_sec:02}"

    def __str__(self) -> str:
        """
        Convert this log item to a string, usually for printing.

        ### Returns:
        * `str`: stringified log item
        """
        index = f"[#{self.index:5d}]"
        time  = LogItem._formatTime(self.time)
        return \
            f"{index}: {time} | {self.category.ljust(30)} : {self.message}"

    def printDetails(self):
        """
        Print full details of the log item, including time, category and
        traceback
        """
        print(f"Log item #{self.index} ({LogItem._formatTime(self.time)})")
        print(f"Category: {self.category}")
        print(f"----------------------------------------")
        print(self.message)
        if len(self.details):
            print()
            print(self.details)
        print(f"----------------------------------------")
        # print(traceback.print_list(self.trace))
