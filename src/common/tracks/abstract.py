
from abc import abstractmethod
from common.types import Color


class AbstractTrack:
    """
    Abstract base class for mixer tracks and channel rack channels

    Allows for their properties to be get/set in a simplified manner
    """
    @abstractmethod
    @property
    def index(self) -> int:
        """
        Index of the track
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

    @abstractmethod
    @property
    def mute(self) -> bool:
        """
        Whether the track is muted
        """

    @mute.setter
    def mute(self, new_value: bool):
        ...

    def muteToggle(self) -> None:
        """
        Toggle whether a track is muted
        """
        self.mute = not self.mute

    @abstractmethod
    @property
    def solo(self) -> bool:
        """
        Whether the track is solo
        """

    @solo.setter
    def solo(self, new_value: bool):
        ...

    def soloToggle(self) -> None:
        """
        Toggle whether a track is solo
        """
        self.solo = not self.solo

    # TODO: Flesh out with more stuff as required
