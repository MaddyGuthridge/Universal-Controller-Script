"""
common > logger > logger

Contains the definition of the log class, which maintains the script's log,
and allows for log information to be searched and recalled

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""

__all__ = [
    'log'
]
from typing import Optional
from .log_item import LogItem
from .verbosity import Verbosity, DEFAULT, ERROR, NOTE


class Log:
    """
    Represents the log of the script.

    This allows information such as errors or warnings to be logged and
    searched through as required.
    """

    def __repr__(self) -> str:
        print("\n".join([
            "Log: contains logging information from the script",
            "Commands:",
            " * length(): returns the length of the log",
            " * recall(): recall log entries",
            " * inspect(index): print detailed info about a log entry",
        ]))
        return ""

    def __init__(self) -> None:
        self._history: list[LogItem] = []

    @staticmethod
    def _shouldPrint(
        item: LogItem,
        category: Optional[str] = None,
        verbosity: Optional[Verbosity] = None
    ) -> bool:
        """Returns whether the logger should print an item

        * By default (no category or verbosity specified), it checks whether
          the item's categories are in the watched categories. If so, it will
          print out if the verbosity is less than the given verbosity, or the
          `logger.max_watched_verbosity` setting if that isn't provided.
          Otherwise it will print out if the verbosity is less than the given
          verbosity, or the `logger.max_verbosity` setting if that isn't
          provided.
        * If a category is specified, it will print if the item is in that
          category and the verbosity is less than the given verbosity, or the
          `logger.max_watched_verbosity` setting if that isn't provided.

        Args:
        * `item` (`LogItem`): item to check
        * `category` (`str`, optional): category  to filter by. Defaults to
          `None`.
        * `verbosity` (`Verbosity`, optional): greatest verbosity to print.
          Defaults to `None`.

        Returns:
        * `bool`: whether it was printed
        """
        # If a category was provided, ignore all events not from it
        if category is not None and not item.category.startswith(category):
            return False

        # Make sure we log things, even if the context isn't loaded
        # They will still (hopefully) be recallable later
        import common
        try:
            context = common.getContext()
        except common.context_manager.MissingContextException:
            verbosity = DEFAULT
        else:
            if verbosity is None:
                # TODO: Potentially buggy if a `.` isn't the next char in the
                # watched category
                if any(item.category.startswith(c)
                       for c in context.settings.get(
                           "logger.watched_categories"
                )):
                    verbosity = context.settings.get(
                        "logger.max_watched_verbosity")
                else:
                    verbosity = context.settings.get("logger.max_verbosity")

        assert verbosity is not None
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
            verbosity: Verbosity = common.getContext().settings.get(
                "logger.critical_verbosity"
            )
        except common.context_manager.MissingContextException:
            verbosity = ERROR
        return item.verbosity <= verbosity

    @staticmethod
    def _conditionalPrint(
        item: LogItem,
        category: Optional[str] = None,
        verbosity: Optional[Verbosity] = None
    ) -> bool:
        """If the logger should print this particular item, prints it. It does
        a detailed print if required.

        * By default (no category or verbosity specified), it checks whether
          the item's categories are in the watched categories. If so, it will
          print out if the verbosity is less than the given verbosity, or the
          `logger.max_watched_verbosity` setting if that isn't provided.
          Otherwise it will print out if the verbosity is less than the given
          verbosity, or the `logger.max_verbosity` setting if that isn't
          provided.
        * If a category is specified, it will print if the item is in that
          category and the verbosity is less than the given verbosity, or the
          `logger.max_watched_verbosity` setting if that isn't provided.

        Args:
        * `item` (`LogItem`): item to check
        * `category` (`str`, optional): category  to filter by. Defaults to
          `None`.
        * `verbosity` (`Verbosity`, optional): greatest verbosity to print.
          Defaults to `None`.

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

    def recall(
        self,
        category: Optional[str] = None,
        verbosity: Optional[Verbosity] = None,
        number: int = -1
    ):
        """
        Recall and print all matching log entries for the provided category at
        the given verbosity level or higher, with the latest item being logged
        last

        ### Args:
        * `category` (`str`, optional): category to match, defaults to all.
        * `verbosity` (`Verbosity`, optional): verbosity level. Defaults to
          `DEFAULT`.
        * `number` (`int`, optional): number of values to recall, defaults to
          all.
        """
        from common.util.misc import NoneNoPrintout
        # Figure out what to print
        num_prints = 0
        num_skips = 0
        prints: list[LogItem] = []
        v = DEFAULT if verbosity is None else verbosity
        for item in reversed(self._history):
            # Print if required
            if self._shouldPrint(item, category, v):
                num_prints += 1
                prints.insert(0, item)
            else:
                num_skips += 1
            if num_prints == number:
                break

        # Then print it
        print("----------------------------------------")
        print("Recalling", end='')
        if number != -1:
            if number == 1:
                print(" most recent entry", end='')
            else:
                print(f" most recent {number} entries", end='')
        if category is not None:
            print(f" from category '{category}'", end='')
        if verbosity is not None:
            print(f" at verbosity={verbosity}", end='')
        print("...")

        for item in prints:
            print(item)
        print(f"({num_skips} item{'s' if num_skips != 1 else ''} skipped)")
        print("End recall")
        print("----------------------------------------")
        return NoneNoPrintout

    def inspect(self, itemNumber: int):
        """
        Inspect and print the details of a log entry.

        This is a helper function for debugging.

        ### Args:
        * `itemNumber` (`int`): entry number
        """
        from common.util.misc import NoneNoPrintout
        self._history[itemNumber].printDetails()

        return NoneNoPrintout

    def __call__(
        self,
        category: str,
        msg: str,
        verbosity: Verbosity = DEFAULT,
        detailed_msg: str = ''
    ) -> None:
        """
        Add a message to the log

        The message is stored in the log history, as well as being printed if
        it falls under one of the printable categories, or is at a verbosity
        level high enough to demand attention

        ### Args:
        * `category` (`str`): category to log under
        * `msg` (`str`): message to log
        * `verbosity` (`Verbosity`, optional): verbosity to log under. Defaults
          to `DEFAULT`.
        """
        import common
        try:
            discarded = common.getContext().settings.get(
                "logger.discard_verbosity"
            )
        except common.context_manager.MissingContextException:
            discarded = NOTE
        if verbosity > discarded:
            return
        # TODO: Maybe get traceback
        item = LogItem(category, msg, detailed_msg,
                       verbosity, len(self._history))
        self._history.append(item)
        # Print if required
        self._conditionalPrint(item)


log = Log()
