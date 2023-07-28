"""
common > plug_indexes > fl_index

Definition for FlIndex abstract base class

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""
from abc import abstractmethod
from typing import TYPE_CHECKING
import plugins

from common.consts import PARAM_CC_START


if TYPE_CHECKING:
    from .window import WindowIndex


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

    @abstractmethod
    def focus(self) -> None:
        """
        Focus the plugin or window
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
        from .window import WindowIndex
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
