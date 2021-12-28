"""
logger > logitem

Contains LogItem, a class used to represent an entry in the script's log

Authors:
* Miguel Guthridge [hdsq@outlook.com.au]
"""

import time
import traceback

from .verbosity import Verbosity

class LogItem:
    
    def __init__(self, category: str, message: str, verbosity: Verbosity, index: int) -> None:
        self.category = category
        self.message = message
        self.verbosity = verbosity
        self.index = index
        self.time = time.localtime()
        self.trace = traceback.extract_stack(limit=-2)
    
    @staticmethod
    def _formatTime(time) -> str:
        return f"{time.tm_hour:02}:{time.tm_min:02}:{time.tm_sec:02}"

    def __str__(self) -> str:
        index = f"[#{self.index:5d}]"
        time  = LogItem._formatTime(self.time)
        return \
            f"{index}: {time} | {self.category.ljust(30)} : {self.message}"

    def printDetails(self):
        print(f"Log item #{self.index} ({LogItem._formatTime(self.time)})")
        print(f"Category: {self.category}")
        print(f"----------------------------------------")
        print(self.message)
        print(f"----------------------------------------")
        print(traceback.print_list(self.trace))
