"""
common > plug_indexes

Type definitions for plugin indexes.

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""
from abc import abstractmethod
from typing import Literal
import channels

import plugins
from common import consts

from common.consts import PARAM_CC_START
from common.types.color import Color


class FlIndex:
    """
    Represents an index to a plugin or window in FL Studio
    """
    @abstractmethod
    def getName(self) -> str:
        """
        Returns the name of the plugin/window at the given index
        """
        ...

    def asWindowIndex(self) -> 'WindowIndex':
        """
        Cast this to a WindowIndex

        Raises an error if the index was not a WindowIndex

        ### Raises:
        * `TypeError`: type cast failed

        ### Returns:
        * `WindowIndex`: this index, but now guaranteed to be a WindowIndex
        """
        if isinstance(self, WindowIndex):
            return self
        raise TypeError(f'Cannot cast to WindowIndex, type is {self}')

    def asPluginIndex(self) -> 'PluginIndex':
        """
        Cast this to a PluginIndex

        Raises an error if the index was not a PluginIndex

        ### Raises:
        * `TypeError`: type cast failed

        ### Returns:
        * `PluginIndex`: this index, but now guaranteed to be a PluginIndex
        """
        if isinstance(self, PluginIndex):
            return self
        raise TypeError(f'Cannot cast to PluginIndex, type is {self}')


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


class PluginIndex(FlIndex):
    @abstractmethod
    @property
    def index(self) -> int:
        """
        The primary index of this plugin.

        * Global index on the channel rack for generators.
        * Mixer track for effects.
        """
        ...

    @abstractmethod
    @property
    def slotIndex(self) -> int:
        """
        The slot index for effects. `-1` for generators.
        """
        ...

    @property
    def isValid(self) -> bool:
        """
        `True` when the plugin is valid.
        """
        return plugins.isValid(self.index, self.slotIndex, True)

    @property
    def isVst(self) -> bool:
        """
        `True` when the plugin is a VST.
        """
        if self.isValid:
            paramCount = plugins.getParamCount(
                self.index,
                self.slotIndex,
                True,
            )
            # A plugin is assumed to be a VST if it has over 4096 params
            return paramCount > PARAM_CC_START
        else:
            return False

    def getName(self) -> str:
        return plugins.getPluginName(self.index, self.slotIndex, False, True)


class GeneratorIndex(PluginIndex):
    def __init__(self, index: int) -> None:
        self.__index = index

    def __repr__(self) -> str:
        return f"GeneratorIndex({self.__index}, {self.getName()!r})"

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

    def triggerNote(self, note_number: int, value: float) -> None:
        """
        Trigger a note on the given channel
        """
        channels.midiNoteOn(self.index, note_number, int(value * 127))


class EffectIndex(PluginIndex):
    def __init__(self, index: int, slotIndex: int) -> None:
        self.__index = index
        self.__slot = slotIndex

    def __repr__(self) -> str:
        return \
            f"EffectIndex({self.__index}, {self.__slot}, {self.getName()!r})"

    @property
    def index(self) -> int:
        """
        The mixer track that contains the plugin.
        """
        return self.__index

    @property
    def slotIndex(self) -> int:
        """
        The mixer slot that contains the plugin.
        """
        return self.__slot
