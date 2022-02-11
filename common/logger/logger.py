"""
common > logger > logger

Contains the definition of the log class, which maintains the script's log,
and allows for log information to be searched and recalled

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]
"""

__all__ = [
    'log'
]

from .logitem import LogItem
from .verbosity import Verbosity, DEFAULT, ERROR

from ..util.misc import NoneNoPrintout

class Log:
    """
    Represents the log of the script.

    This allows information such as errors or warnings to be logged and searched
    through as required.
    """
    def __init__(self) -> None:
        self._history: list[LogItem] = []
    
    @staticmethod
    def _shouldPrint(item: LogItem, category: str=None, verbosity:Verbosity=None) -> bool:
        """Returns whether the logger should print an item
        
        * By default (no category or verbosity specified), it checks whether the
          item's categories are in the watched categories. If so, it will print
          out if the verbosity is less than the given verbosity, or the
          `logger.max_watched_verbosity` setting if that isn't provided.
          Otherwise it will print out if the verbosity is less than the given
          verbosity, or the `logger.max_verbosity` setting if that isn't 
          provided.
        * If a category is specified, it will print if the item is in that
          category and the verbosity is less than the given verbosity, or the
          `logger.max_watched_verbosity` setting if that isn't provided.

        Args:
        * `item` (`LogItem`): item to check
        * `category` (`str`, optional): category  to filter by. Defaults to `None`.
        * `verbosity` (`Verbosity`, optional): greatest verbosity to print. Defaults to `None`.
        
        Returns:
        * `bool`: whether it was printed
        """
        # Make sure we log things, even if the context isn't loaded
        # They will still (hopefully) be recallable later
        import common
        try:
            context = common.getContext()
        except common.contextmanager.MissingContextException:
            verbosity = DEFAULT
        else:
            if verbosity is None:
                # TODO: Potentially buggy if a `.` isn't the next char in the
                # watched category
                if any(item.category.startswith(c)
                       for c in context.settings.get("logger.watched_categories")):
                    verbosity = context.settings.get("logger.max_watched_verbosity")
                else:
                    verbosity = context.settings.get("logger.max_verbosity")
        
        assert(verbosity is not None)
        if item.verbosity <= verbosity:
            return True
        else:
            return False
    
    @staticmethod
    def _shouldDetailedPrint(item: LogItem) -> bool:
        """
        Returns whether the logger should do a detailed printout of the item.

        Reserved for errors that the user should be notified of.

        ### Args:
        * `item` (`LogItem`): item to check

        ### Returns:
        * `bool`: whether we should detailed print it
        """
        # Make sure we log things, even if the context isn't loaded
        # They will still (hopefully) be recallable later
        import common
        try:
            verbosity = common.getContext().settings.get("logger.critical_verbosity")
        except common.contextmanager.MissingContextException:
            verbosity = ERROR
        return item.verbosity <= verbosity
    
    @staticmethod
    def _conditionalPrint(item: LogItem, category: str=None, verbosity:Verbosity=None) -> bool:
        """If the logger should print this particular item, prints it. It does
        a detailed print if required.
        
        * By default (no category or verbosity specified), it checks whether the
          item's categories are in the watched categories. If so, it will print
          out if the verbosity is less than the given verbosity, or the
          `logger.max_watched_verbosity` setting if that isn't provided.
          Otherwise it will print out if the verbosity is less than the given
          verbosity, or the `logger.max_verbosity` setting if that isn't 
          provided.
        * If a category is specified, it will print if the item is in that
          category and the verbosity is less than the given verbosity, or the
          `logger.max_watched_verbosity` setting if that isn't provided.

        Args:
        * `item` (`LogItem`): item to check
        * `category` (`str`, optional): category  to filter by. Defaults to `None`.
        * `verbosity` (`Verbosity`, optional): greatest verbosity to print. Defaults to `None`.
        
        Returns:
        * `bool`: whether it was printed
        """
        if Log._shouldDetailedPrint(item):
            item.printDetails()
            print()
            return True
        elif Log._shouldPrint(item, category, verbosity):
            print(item)
            print()
            return True
        else:
            return False
    
    def __len__(self) -> int:
        return len(self._history)
    
    def length(self) -> int:
        """
        Returns the length of the log

        ### Returns:
        * `int`: log length
        """
        return len(self)

    def recall(self, category: str = "", verbosity: Verbosity = DEFAULT, number: int = -1):
        """
        Recall and print all matching log entries for the provided category at 
        the given verbosity level or higher, with the latest item being logged
        last

        ### Args:
        * `category` (`str`, optional): category to match, defaults to all.
        * `verbosity` (`Verbosity`, optional): verbosity level. Defaults to `DEFAULT`.
        * `number` (`int`, optional): number of values to recall, defaults to all.
        """
        # Figure out what to print
        num_prints = 0
        num_skips = 0
        prints: list[LogItem] = []
        for item in reversed(self._history):
            # Print if required
            if self._shouldPrint(item, category, verbosity):
                num_prints += 1
                prints.insert(0, item)
            else:
                num_skips += 1
            if num_prints == number:
                break
        
        # Then print it
        print(f"----------------------------------------")
        print("Begin recall:")
        for item in prints:
            print(item)
        print(f"({num_skips} item{'s' if num_skips != 1 else ''} skipped)")
        print("End recall")
        print(f"----------------------------------------")
        return NoneNoPrintout
    
    def inspect(self, itemNumber: int):
        """
        Inspect and print the details of a log entry.
        
        This is a helper function for debugging.

        ### Args:
        * `itemNumber` (`int`): entry number
        """
        self._history[itemNumber].printDetails()
        
        return NoneNoPrintout

    def __call__(self, category: str, msg: str, verbosity: Verbosity = DEFAULT, detailed_msg: str = '') -> None:
        """
        Add a message to the log

        The message is stored in the log history, as well as being printed if
        it falls under one of the printable categories, or is at a verbosity
        level high enough to demand attention

        ### Args:
        * `category` (`str`): category to log under
        * `msg` (`str`): message to log
        * `verbosity` (`Verbosity`, optional): verbosity to log under. Defaults to `DEFAULT`.
        """
        # TODO: Maybe get traceback
        item = LogItem(category, msg, detailed_msg, verbosity, len(self._history))
        self._history.append(item)
        # Print if required
        self._conditionalPrint(item)

log = Log()
