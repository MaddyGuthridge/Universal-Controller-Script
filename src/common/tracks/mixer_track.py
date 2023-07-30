import mixer
from common.types import Color
from .abstract import AbstractTrack


class MixerTrack(AbstractTrack):
    """
    Helper class for accessing properties of mixer tracks
    """

    def __init__(self, index: int) -> None:
        self.__index = index

    @property
    def color(self) -> Color:
        return Color.fromInteger(mixer.getTrackColor(self.__index))

    @color.setter
    def color(self, new_color: Color) -> None:
        mixer.setTrackColor(self.__index, new_color.integer)

    @property
    def name(self) -> str:
        return mixer.getTrackName(self.__index)

    @name.setter
    def name(self, new_name: str) -> None:
        mixer.setTrackName(self.__index, new_name)

    @property
    def mute(self) -> bool:
        return mixer.isTrackMuted(self.__index)

    @mute.setter
    def mute(self, new_value: bool) -> None:
        if new_value != self.mute:
            mixer.muteTrack(self.__index)

    def muteToggle(self) -> None:
        mixer.muteTrack(self.__index)

    @property
    def solo(self) -> bool:
        return mixer.isTrackSolo(self.__index)

    @solo.setter
    def solo(self, new_value: bool) -> None:
        if new_value != self.solo:
            mixer.soloTrack(self.__index)

    def soloToggle(self) -> None:
        mixer.soloTrack(self.__index)
