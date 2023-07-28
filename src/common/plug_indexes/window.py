from common import consts
from . import FlIndex


class WindowIndex(FlIndex):
    """
    Represents a window in FL Studio
    """
    def __init__(self, windowIndex: int) -> None:
        self.__index = windowIndex

    @property
    def index(self) -> int:
        """
        The index of the window.
        """
        return self.__index

    def __repr__(self) -> str:
        return f"WindowIndex({self.__index}, {self.getName()!r})"

    def getName(self) -> str:
        return consts.WINDOW_NAMES[self.__index]
