
from abc import abstractmethod
import plugins

from .fl_index import FlIndex
from common.consts import PARAM_CC_START
from common.types import Color


class AbstractTrack:
    """
    Abstract base class for mixer tracks and channel rack channels

    Allows for their properties to be get/set in a simplified manner
    """
    @abstractmethod
    @property
    def color(self) -> Color:
        """
        Color of the track
        """
        ...

    @color.setter
    def color(self, new_color: Color) -> None:
        ...

    @abstractmethod
    @property
    def name(self) -> str:
        """
        Name of the track. Note that this isn't necessarily the same as the
        name of the plugin.
        """
        ...

    @name.setter
    def name(self, new_name: str) -> None:
        ...

    # TODO: Flesh out with more stuff as required


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

    @abstractmethod
    @property
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
        return plugins.getPluginName(self.index, self.slotIndex, False, True)
