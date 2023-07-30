import mixer
from .plugin import PluginIndex
from common.tracks import MixerTrack


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
