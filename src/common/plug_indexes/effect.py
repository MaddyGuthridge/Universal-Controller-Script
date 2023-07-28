import mixer
from common.types import Color
from .fl_index import PluginIndex


class MixerTrack:
    """
    Helper class for accessing properties of mixer tracks
    """

    def __init__(self, index: int) -> None:
        self.__index = index

    @property
    def color(self) -> Color:
        """
        Color of the track
        """
        return Color.fromInteger(mixer.getTrackColor(self.__index))

    # TODO: Flesh out with more stuff as required


class EffectIndex(PluginIndex):
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
