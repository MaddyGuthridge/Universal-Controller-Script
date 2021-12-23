
from .logitem import LogItem

class Log:
    
    def __init__(self) -> None:
        self._history: list[LogItem] = []
    
    def recall(self, category: str):
        """Print out all log items that match a certain category

        Args:
            type (str): log item type
        """
        for item in self._history:
            # Check for matching entry type
            if item.cat == category or item.cat.startswith(category + '.'):
                print(item)

    def __call__(self, category: str, msg: str) -> None:
        """Log a message under a category

        Args:
            category (str): category to log into
            msg (str): message to log
        """
        self._history.append(LogItem(category, msg))

log = Log()
