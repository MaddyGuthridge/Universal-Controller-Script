
import channels
import plugins

from .plugin import PluginIndex, AbstractTrack
from typing import Literal, TypeVar, ParamSpec, Concatenate, Callable, Union
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

    def triggerNote(self, note_number: int, value: float) -> None:
        """
        Trigger a note on this channel
        """
        channels.midiNoteOn(self.__index, note_number, int(value * 127))

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


class GeneratorIndex(PluginIndex):
    def __init__(self, index: int) -> None:
        self.__index = index

    def __repr__(self) -> str:
        return f"GeneratorIndex({self.__index}, {self.getName()!r})"

    def focus(self) -> None:
        group_index = getGroupChannelIndex(self.__index)
        if group_index is not None:
            channels.focusEditor(group_index)
        else:
            print("Cannot focus generator outside of current group")

    @property
    def index(self) -> int:
        """
        The global index of the channel rack slot that contains the plugin.
        """
        return self.__index

    @property
    def slotIndex(self) -> Literal[-1]:
        """
        This value is always `-1` for generator plugins.
        """
        return -1

    @property
    def track(self) -> Channel:
        """
        The channel that underlies this index
        """
        return Channel(self.__index)

    def fpcGetPadSemitone(self, pad_index: int) -> int:
        """
        Returns the note number for the drum pad at the given index.

        For use with the FPC plugin.
        """
        return plugins.getPadInfo(
            self.index,
            self.slotIndex,
            1,  # Note number
            pad_index,
            True,
        )

    def fpcGetPadColor(self, pad_index: int) -> Color:
        """
        Returns the color of the drum pad at the given index.

        For use with the FPC plugin.
        """
        return Color.fromInteger(plugins.getPadInfo(
            self.index,
            self.slotIndex,
            2,  # Color
            pad_index,
            True,
        ))

    def getNoteName(self, note_number: int) -> str:
        """
        Returns the name of the note at the given index
        """
        return plugins.getName(
            self.index,
            self.slotIndex,
            2,  # Note name
            note_number,
            True,
        )
