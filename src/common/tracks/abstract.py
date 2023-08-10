"""
common > tracks > abstract

Abstract base class for tracks abstraction used elsewhere within the script

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""
from abc import abstractmethod
from common.types import Color


class AbstractTrack:
    """
    Abstract base class for mixer tracks and channel rack channels

    Allows for their properties to be get/set in a simplified manner
    """
    @property
    @abstractmethod
    def index(self) -> int:
        """
        Index of the track
        """

    @property
    @abstractmethod
    def color(self) -> Color:
        """
        Color of the track
        """
        ...

    @color.setter
    def color(self, new_color: Color) -> None:
        ...

    @property
    @abstractmethod
    def name(self) -> str:
        """
        Name of the track. Note that this isn't necessarily the same as the
        name of the plugin.
        """
        ...

    @name.setter
    def name(self, new_name: str) -> None:
        ...

    @property
    @abstractmethod
    def selected(self) -> bool:
        """
        Whether the track is selected
        """
        ...

    @selected.setter
    def selected(self, new_value: bool) -> None:
        if self.selected != new_value:
            self.selectedToggle()

    @abstractmethod
    def selectedToggle(self) -> None:
        """
        Toggle whether the track is selected
        """

    @property
    @abstractmethod
    def mute(self) -> bool:
        """
        Whether the track is muted
        """

    @mute.setter
    def mute(self, new_value: bool):
        if self.mute != new_value:
            self.muteToggle()

    @abstractmethod
    def muteToggle(self) -> None:
        """
        Toggle whether a track is muted
        """

    @property
    @abstractmethod
    def solo(self) -> bool:
        """
        Whether the track is solo
        """

    @solo.setter
    def solo(self, new_value: bool):
        if self.solo != new_value:
            self.soloToggle()

    @abstractmethod
    def soloToggle(self) -> None:
        """
        Toggle whether a track is solo
        """

    # TODO: Flesh out with more stuff as required
