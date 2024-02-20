"""
common > plug_indexes > plugin

Type definitions for plugin indexes.

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""
from abc import abstractmethod
import plugins

from .fl_index import FlIndex
from consts import PARAM_CC_START
from common.tracks import AbstractTrack


class PluginIndex(FlIndex):
    @property
    @abstractmethod
    def index(self) -> int:
        """
        The primary index of this plugin.

        * Global index on the channel rack for generators.
        * Mixer track for effects.
        """
        ...

    @property
    @abstractmethod
    def slotIndex(self) -> int:
        """
        The slot index for effects. `-1` for generators.
        """
        ...

    @property
    @abstractmethod
    def track(self) -> AbstractTrack:
        """
        The track or channel underlying this function.
        """
        ...

    def isValid(self) -> bool:
        """
        `True` when the plugin is valid.
        """
        return plugins.isValid(self.index, self.slotIndex, True)

    def isVst(self) -> bool:
        """
        `True` when the plugin is a VST.
        """
        if self.isValid():
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
        """
        Name of the plugin. Note that this isn't necessarily the same as the
        name of the channel/track it resides on
        """
        try:
            return plugins.getPluginName(
                self.index,
                self.slotIndex,
                False,
                True,
            )
        except TypeError:
            return 'Invalid plugin'

    def presetNext(self) -> None:
        """
        Navigate to the next preset for the plugin
        """
        plugins.nextPreset(self.index, self.slotIndex, True)

    def presetPrevious(self) -> None:
        """
        Navigate to the previous preset for the plugin
        """
        plugins.prevPreset(self.index, self.slotIndex, True)
