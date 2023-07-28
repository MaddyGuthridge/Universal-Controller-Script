import ui
from common import consts
from . import FlIndex


class WindowIndex(FlIndex):
    """
    Represents a window in FL Studio
    """
    def __init__(self, windowIndex: int) -> None:
        self.__index = windowIndex

    def __hash__(self) -> int:
        return self.__index

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

    def focus(self) -> None:
        ui.showWindow(self.index)
