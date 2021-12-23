
from .logitem import LogItem
from .verbosity import Verbosity, DEFAULT, MOST_VERBOSE

class Log:
    
    def __init__(self) -> None:
        self._history: list[LogItem] = []
    
    def _shouldPrint(self, item: LogItem, category: str=None, verbosity:Verbosity=None) -> bool:
        """Returns whether the logger should print this particular item.
        
        By default (no category or verbosity specified), it checks whether it

        Args:
         * `item` (`LogItem`): item to check
         * `category` (`str`, optional): category  to filter by. Defaults to `None`.
         * `verbosity` (`Verbosity`, optional): greatest verbosity to print. Defaults to `None`.

        Returns:
         * `bool`: whether to print
        """
        # TODO: Implement using settings
        return True
    
    def recall(self, category: str, verbosity: Verbosity = DEFAULT):
        """
        Recall and print all matching log entries for the provided category at 
        the given verbosity level or higher.

        ### Args:
        * `category` (`str`): category to match
        * `verbosity` (`Verbosity`, optional): verbosity level. Defaults to `DEFAULT`.
        """
        for item in self._history:
            # Check for matching entry types
            if self._shouldPrint(item, category, verbosity):
                print(item)

    def __call__(self, category: str, msg: str, verbosity: Verbosity = DEFAULT) -> None:
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
        item = LogItem(category, msg, verbosity)
        self._history.append(item)
        if self._shouldPrint(item):
            print(item)

log = Log()
