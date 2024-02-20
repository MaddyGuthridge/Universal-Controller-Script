"""
common > tracks > channel

Wrapper around channel properties in FL Studio API

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""
import channels

from .abstract import AbstractTrack
from typing import Optional, TypeVar, Callable, Union
from typing_extensions import ParamSpec, Concatenate
from common.types import Color
from common.util.api_fixes import getGroupChannelIndex


T = TypeVar('T')
R = TypeVar('R')
P = ParamSpec('P')


def channelAction(
    callback: Callable[Concatenate[int, P], T],
    default_return: R,
    global_index: int,
    *args: P.args,
    **kwargs: P.kwargs,
) -> Union[T, R]:
    """
    Perform an action on a channel, only if it is possible to do so using
    global indexes.

    Because the FL Studio API doesn't support global indexes, this wrapper is
    used to ensure

    ### Args

    * `callback`: function to call if possible - it should take a grouped index
      as its first arg then, accept the remaining arguments given to this
      function.

    * `default_return` (`R`): return value if the callback cannot be safely
      called.

    * `global_index` (`int`): global index of channel to act on.

    * `*args`, `**kwargs`: remaining args for callback

    ### Returns

    If the callback was called, a `tuple` of

    * `True`: indicating success
    * `T`: return value of `callback`

    Or if it wasn't called, a `tuple` of

    * `False`: indicating failure
    * `R`: the given default return

    ### Usage

    ```py
    success, value = channelAction(
        channels.getChannelVolume,
        'No volume',  # Default value
        10,  # Channel has global index of 10
        True,  # Get volume in decibels rather than as a percentage
    )

    if success:
        reveal_type(value)  # float
    else:
        reveal_type(value)  # Literal['No volume']
    ```
    """
    group_index = getGroupChannelIndex(global_index)

    if group_index is None:
        return default_return
    else:
        return callback(group_index, *args, **kwargs)


class Channel(AbstractTrack):
    """
    Helper class for accessing properties of channels
    """

    def __init__(self, index: int) -> None:
        self.__index = index

    @property
    def index(self) -> int:
        """
        Global index of the channel
        """
        return self.__index

    @property
    def group_index(self) -> Optional[int]:
        """
        Index of the channel, respecting groups
        """
        return getGroupChannelIndex(self.__index)

    def triggerNote(
        self,
        note_number: int,
        value: float,
        channel: Optional[int] = None,
    ) -> None:
        """
        Trigger a note on this channel
        """
        if channel is None:
            channel = -1
        channels.midiNoteOn(
            self.__index,
            note_number,
            int(value * 127),
            # NOTE: Currently FL Studio won't set the note color correctly
            # from this channel
            channel,
        )

    @property
    def color(self) -> Color:
        """
        Color of the channel
        """
        return Color.fromInteger(channelAction(
            channels.getChannelColor,
            0,
            self.__index
        ))

    @color.setter
    def color(self, new_color: Color) -> None:
        channelAction(
            channels.setChannelColor,
            None,
            self.__index,
            new_color.integer,
        )

    @property
    def name(self) -> str:
        return channelAction(
            channels.getChannelName,
            '',
            self.__index
        )

    @name.setter
    def name(self, new_name: str) -> None:
        channelAction(
            channels.setChannelName,
            None,
            self.__index,
            new_name,
        )

    @property
    def selected(self) -> bool:
        return channelAction(
            channels.isChannelSelected,
            False,
            self.__index,
        )

    @selected.setter
    def selected(self, new_value: bool) -> None:
        if self.selected != new_value:
            channelAction(
                channels.selectChannel,
                None,
                self.__index,
            )

    def selectedToggle(self) -> None:
        channelAction(
            channels.selectChannel,
            None,
            self.__index,
        )

    @property
    def mute(self) -> bool:
        return channelAction(
            channels.isChannelMuted,
            False,
            self.__index,
        )

    @mute.setter
    def mute(self, new_value: bool) -> None:
        if new_value != self.mute:
            channelAction(
                channels.muteChannel,
                None,
                self.__index,
            )

    def muteToggle(self) -> None:
        channelAction(
            channels.muteChannel,
            None,
            self.__index,
        )

    @property
    def solo(self) -> bool:
        return channelAction(
            channels.isChannelSolo,
            False,
            self.__index,
        )

    @solo.setter
    def solo(self, new_value: bool) -> None:
        if new_value != self.solo:
            channelAction(
                channels.soloChannel,
                None,
                self.__index,
            )

    def soloToggle(self) -> None:
        channelAction(
            channels.soloChannel,
            None,
            self.__index,
        )

    @property
    def volume(self) -> float:
        """
        Volume of a channel, from 0 - 1, where 0.78125 is the default
        """
        return channelAction(
            channels.getChannelVolume,
            0.0,
            self.__index,
        )

    @volume.setter
    def volume(self, new_volume: float) -> None:
        channelAction(
            channels.setChannelVolume,
            None,
            self.__index,
            new_volume,
        )

    @property
    def pan(self) -> float:
        """
        Panning of a channel, from -1 to 1 where 0 is centred
        """
        return channelAction(
            channels.getChannelPan,
            0.0,
            self.__index,
        )

    @pan.setter
    def pan(self, new_pan: float) -> None:
        channelAction(
            channels.setChannelPan,
            None,
            self.__index,
            new_pan,
        )
