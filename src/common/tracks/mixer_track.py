"""
common > tracks > abstract

Wrapper around mixer tracks in FL Studio API

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""

import mixer
from common.types import Color
from .abstract import AbstractTrack


class MixerTrack(AbstractTrack):
    """
    Helper class for accessing properties of mixer tracks
    """

    def __init__(self, index: int) -> None:
        self.__index = index

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, MixerTrack):
            return __value.index == self.__index
        return NotImplemented

    def __gt__(self, __value: object) -> bool:
        if isinstance(__value, MixerTrack):
            return self.index > __value.index
        return NotImplemented

    def __lt__(self, __value: object) -> bool:
        if isinstance(__value, MixerTrack):
            return self.index < __value.index
        return NotImplemented

    @property
    def index(self) -> int:
        return self.__index

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
    def selected(self) -> bool:
        return mixer.isTrackSelected(self.__index)

    @selected.setter
    def selected(self, new_value: bool) -> None:
        if self.selected != new_value:
            mixer.selectTrack(self.__index)

    def selectedToggle(self) -> None:
        mixer.selectTrack(self.__index)

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

    @property
    def volume(self) -> float:
        """
        Volume of a track, from 0 - 1, where 0.8 is 100% volume
        """
        return mixer.getTrackVolume(self.__index)

    @volume.setter
    def volume(self, new_volume: float) -> None:
        mixer.setTrackVolume(self.__index, new_volume)

    @property
    def pan(self) -> float:
        """
        Panning of a track, from -1 to 1 where 0 is centred
        """
        return mixer.getTrackPan(self.__index)

    @pan.setter
    def pan(self, new_pan: float) -> None:
        mixer.setTrackPan(self.__index, new_pan)

    @property
    def stereo_separation(self) -> float:
        """
        Stereo separation of a mixer track, ranges from -1 to 1
        """
        return mixer.getTrackStereoSep(self.__index)

    @stereo_separation.setter
    def stereo_separation(self, new_sep: float) -> None:
        mixer.setTrackStereoSep(self.__index, new_sep)

    @property
    def armed(self) -> bool:
        """
        Whether the track is armed for recording
        """
        return mixer.isTrackArmed(self.__index)

    @armed.setter
    def armed(self, new_value: bool) -> None:
        if new_value != self.armed:
            mixer.armTrack(self.__index)

    def armedToggle(self) -> None:
        """
        Toggle whether a track is armed for recording
        """
        mixer.armTrack(self.__index)
