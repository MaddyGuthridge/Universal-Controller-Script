"""
common > plug_indexes > effect

Type definitions for effect plugin indexes.

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""
import mixer
from .plugin import PluginIndex
from common.tracks import MixerTrack


class EffectIndex(PluginIndex):
    """
    Represents the index to an effect plugin
    """
    def __init__(self, index: int, slotIndex: int) -> None:
        self.__index = index
        self.__slot = slotIndex

    def __repr__(self) -> str:
        return \
            f"EffectIndex({self.__index}, {self.__slot}, {self.getName()!r})"

    def focus(self) -> None:
        mixer.focusEditor(self.__index, self.__slot)

    @property
    def track(self) -> MixerTrack:
        """
        The mixer track that underlies this index
        """
        return MixerTrack(self.__index)

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
