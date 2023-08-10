"""
common > util > api_fixes

Contains wrapper code for FL Studio API functions which are just too awful to
be called directly.

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""

import general
import ui
import channels
import mixer
import playlist

from common.profiler import profilerDecoration
from typing import Optional, TYPE_CHECKING


if TYPE_CHECKING:
    from common.plug_indexes import WindowIndex, PluginIndex


@profilerDecoration("getFocusedPluginIndex")
def getFocusedPluginIndex(force: bool = False) -> Optional['PluginIndex']:
    """
    Fixes the horrible ui.getFocusedFormIndex() function

    Values are returned as tuples so that they can be unwrapped when being
    passed to other API functions

    Args:
    * `force` (`bool`, optional): whether to return the selected plugin on the
      channel rack if none are explicitly active

    Returns:
    * `None`: if no plugin is focused
    * `int`: grouped index of a channel rack plugin if one is focused
    * `int, int`: index of a mixer plugin if one is focused
    """
    from common.plug_indexes import GeneratorIndex, EffectIndex
    # If a mixer plugin is focused
    if ui.getFocused(6):
        form_id = ui.getFocusedFormID()
        track = form_id // 4194304
        slot = (form_id - 4194304 * track) // 65536
        return EffectIndex(track, slot)
    # Otherwise, assume that a channel is selected
    # Use the channel rack index so that we always have one
    elif ui.getFocused(7):
        form_id = ui.getFocusedFormID()
        if form_id == -1:
            # Plugin invalid?
            return None
        # Since the form ID respects groups, we need to convert it to a global
        # index
        channel = channels.getChannelIndex(form_id)
        return GeneratorIndex(channel)
    else:
        if force:
            return GeneratorIndex(channels.selectedChannel())
        else:
            return None


@profilerDecoration("getFocusedWindowIndex")
def getFocusedWindowIndex() -> Optional['WindowIndex']:
    """
    Fixes the horrible ui.getFocused() function

    Returns:
        * `None`: if no window is focused
        * `int`: index of window
    """
    from common.plug_indexes import WindowIndex
    for i in range(5):
        if ui.getFocused(i):
            return WindowIndex(i)
    return None


def catchUnsafeOperation(func):
    """
    Decorator to prevent exceptions due to unsafe operations

    ### Args:
    * `func` (`Callable`): function to decorate
    """
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except TypeError as e:
            if e.args != ("Operation unsafe at current time",):
                raise e
    return wrapper


def getSelectedDockMixerTracks() -> dict[int, list[int]]:
    """
    Returns a list of the selected mixer tracks for each dock side, not
    including current

    * 0: tracks docked to left
    * 1: tracks in centre
    * 2: tracks docked to right

    ### Returns:
    * `dict[int, list[int]]`: track selections
    """
    tracks: dict[int, list[int]] = {
        0: [],
        1: [],
        2: [],
    }
    for i in range(mixer.trackCount() - 1):
        if mixer.isTrackSelected(i):
            tracks[mixer.getTrackDockSide(i)].append(i)

    return tracks


def getSelectedMixerTracks() -> list[int]:
    """
    Returns a list of the selected mixer tracks, not including current

    ### Returns:
    * `list[int]`: track selections
    """
    tracks: list[int] = []
    for i in range(mixer.trackCount() - 1):
        if mixer.isTrackSelected(i):
            tracks.append(i)

    return tracks


def getMixerDockSides() -> dict[int, list[int]]:
    """
    Returns a list of the dock sides for tracks on the mixer

    * 0: tracks docked to left
    * 1: tracks in centre
    * 2: tracks docked to right

    ### Returns:
    * `dict[int, list[int]]`: track selections
    """
    tracks: dict[int, list[int]] = {
        0: [],
        1: [],
        2: [],
    }
    for i in range(mixer.trackCount() - 1):
        tracks[mixer.getTrackDockSide(i)].append(i)

    return tracks


def getSelectedChannels(global_mode: bool) -> list[int]:
    """
    Returns a list of the selected channels on the channel rack

    ### Args:
    * `bool`: whether to check channels outside of the current group

    ### Returns:
    * `list[int]`: list of selected channels (using global indexes)
    """
    num_channels = channels.channelCount(global_mode)
    selections: list[int] = []
    for ch in range(num_channels):
        if channels.isChannelSelected(channels.getChannelIndex(ch)):
            if global_mode:
                ch = channels.getChannelIndex(ch)
            selections.append(ch)
    return selections


def getFirstPlaylistSelection() -> int:
    """
    Returns the index of the first currently selected playlist track, or `1` if
    no tracks are currently selected

    ### Returns:
    * `int`: selected track
    """
    for i in range(1, playlist.trackCount()):
        if playlist.isTrackSelected(i):
            return i
    return 1


def getSelectedPlaylistTracks() -> list[int]:
    """
    Returns a list of the selected tracks on the playlist

    ### Returns:
    * `list[int]`: list of selected track
    """
    selections: list[int] = []
    for i in range(1, playlist.trackCount() + 1):
        if playlist.isTrackSelected(i):
            selections.append(i)
    return selections


def getUndoPosition() -> tuple[int, int]:
    """
    Returns a tuple of two ints representing the position in the undo history

    ### Returns:
    * `tuple[int, int]`: position in undo history, number of items in undo
      history
    """
    return general.getUndoHistoryPos(), general.getUndoHistoryCount()


def getGroupChannelIndex(global_index: int) -> Optional[int]:
    """
    Returns the group index of the channel at the given global index

    ### Returns
    * `int`: group index, or
    * `None`: channel does not exist in the current group
    """
    for i in range(channels.channelCount()):
        global_i = channels.getChannelIndex(i)
        if global_i == global_index:
            return i
        elif global_i > global_index:
            # Short-circuit: we went past it
            # This works because grouped channels are still kept in the same
            # order as their global order
            return None

    # Reached the end and didn't find it
    return None
