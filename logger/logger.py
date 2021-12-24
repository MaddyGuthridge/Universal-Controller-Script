
from .logitem import LogItem
from .verbosity import Verbosity, DEFAULT, MOST_VERBOSE

class Log:
    
    def __init__(self) -> None:
        self._history: list[LogItem] = []
    
    @staticmethod
    def _conditionalPrint(item: LogItem, category: str=None, verbosity:Verbosity=None) -> None:
        """If the logger should print this particular item, prints it
        
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
        """
    
    def recall(self, category: str, verbosity: Verbosity = DEFAULT):
        """
        Recall and print all matching log entries for the provided category at 
        the given verbosity level or higher.

        ### Args:
        * `category` (`str`): category to match
        * `verbosity` (`Verbosity`, optional): verbosity level. Defaults to `DEFAULT`.
        """
        for item in self._history:
            # Print if required
            self._conditionalPrint(item, category, verbosity)

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
        # Print if required
        self._conditionalPrint(item)

log = Log()
