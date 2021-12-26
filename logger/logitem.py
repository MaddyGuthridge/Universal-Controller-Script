
from .verbosity import Verbosity

class LogItem:
    
    def __init__(self, category: str, message: str, verbosity: Verbosity) -> None:
        self.category = category
        self.message = message
        self.verbosity = verbosity
