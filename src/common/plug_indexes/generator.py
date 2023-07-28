
import channels
import plugins

from .fl_index import PluginIndex
from typing import Literal
from common.types import Color
from common.util.api_fixes import getGroupChannelIndex


class Channel:
    """
    Helper class for accessing properties of channels
    """

    def __init__(self, index: int) -> None:
        self.__index = index

    def triggerNote(self, note_number: int, value: float) -> None:
        """
        Trigger a note on this channel
        """
        channels.midiNoteOn(self.__index, note_number, int(value * 127))

    @property
    def color(self) -> Color:
        """
        Color of the channel
        """
        # FIXME: No support for global indexes for channel color?
        group_index = getGroupChannelIndex(self.__index)
        if group_index is None:
            return Color()
        else:
            return Color.fromInteger(channels.getChannelColor(group_index))

    # TODO: Flesh out with more stuff as required


class GeneratorIndex(PluginIndex):
    def __init__(self, index: int) -> None:
        self.__index = index

    def __repr__(self) -> str:
        return f"GeneratorIndex({self.__index}, {self.getName()!r})"

    def focus(self) -> None:
        group_index = getGroupChannelIndex(self.__index)
        if group_index is not None:
            channels.focusEditor(group_index)
        else:
            print("Cannot focus generator outside of current group")

    @property
    def index(self) -> int:
        """
        The global index of the channel rack slot that contains the plugin.
        """
        return self.__index

    @property
    def slotIndex(self) -> Literal[-1]:
        """
        This value is always `-1` for generator plugins.
        """
        return -1

    @property
    def channel(self) -> Channel:
        """
        The channel that underlies this index
        """
        return Channel(self.__index)

    def fpcGetPadSemitone(self, pad_index: int) -> int:
        """
        Returns the note number for the drum pad at the given index.

        For use with the FPC plugin.
        """
        return plugins.getPadInfo(
            self.index,
            self.slotIndex,
            1,  # Note number
            pad_index,
            True,
        )

    def fpcGetPadColor(self, pad_index: int) -> Color:
        """
        Returns the color of the drum pad at the given index.

        For use with the FPC plugin.
        """
        return Color.fromInteger(plugins.getPadInfo(
            self.index,
            self.slotIndex,
            2,  # Color
            pad_index,
            True,
        ))

    def getNoteName(self, note_number: int) -> str:
        """
        Returns the name of the note at the given index
        """
        return plugins.getName(
            self.index,
            self.slotIndex,
            2,  # Note name
            note_number,
            True,
        )
