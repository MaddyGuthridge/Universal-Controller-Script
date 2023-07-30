import ui
import consts
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

    # Hopefully this duplicate code can be fixed if I get a better answer to
    # https://stackoverflow.com/q/75000973/6335363
    MIXER: 'WindowIndex'
    CHANNEL_RACK: 'WindowIndex'
    PLAYLIST: 'WindowIndex'
    PIANO_ROLL: 'WindowIndex'
    BROWSER: 'WindowIndex'


WindowIndex.MIXER = WindowIndex(0)
WindowIndex.CHANNEL_RACK = WindowIndex(1)
WindowIndex.PLAYLIST = WindowIndex(2)
WindowIndex.PIANO_ROLL = WindowIndex(3)
WindowIndex.BROWSER = WindowIndex(4)
