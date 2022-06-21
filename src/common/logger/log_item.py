"""
common > logger > log_item

Contains LogItem, a class used to represent an entry in the script's log

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
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
        self.time = time.time()
        self.trace = None  # traceback.extract_stack(limit=-2)

    def __str__(self) -> str:
        """
        Convert this log item to a string, usually for printing.

        ### Returns:
        * `str`: stringified log item
        """
        from common.util.misc import formatTime
        index = f"[#{self.index:6d}]"
        time = formatTime(self.time)
        return \
            f"{index}: {time} | {self.category} : {self.message}"

    def printDetails(self):
        """
        Print full details of the log item, including time, category and
        traceback
        """
        from common.util.misc import formatLongTime
        print(
            f"Log item #{self.index} ({formatLongTime(self.time)}), "
            f"verbosity={self.verbosity}"
        )
        print(f"Category: {self.category}")
        print("----------------------------------------")
        print(self.message)
        if len(self.details):
            print()
            print(self.details)
        print("----------------------------------------")
        # print(traceback.print_list(self.trace))
