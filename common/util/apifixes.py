"""
common > util > apifixes

Contains wrapper code for FL Studio API functions which are just too awful to
be called directly.
"""

import plugins
import ui
import channels
import mixer
import playlist

from typing import Union, Optional
from common.consts import PARAM_CC_START

GeneratorIndex = tuple[int]
UnsafeGeneratorIndex = Optional[GeneratorIndex]

EffectIndex = tuple[int, int]
UnsafeEffectIndex = Optional[EffectIndex]

PluginIndex = Union[GeneratorIndex, EffectIndex]
UnsafePluginIndex = Optional[PluginIndex]

WindowIndex = int
UnsafeWindowIndex = Optional[int]

UnsafeIndex = Union[UnsafePluginIndex, UnsafeWindowIndex]


def getFocusedPluginIndex(force: bool = False) -> UnsafePluginIndex:
    """
    Fixes the horrible ui.getFocusedFormIndex() function

    Values are returned as tuples so that they can be unwrapped when

    Args:
    * `force` (`bool`, optional): whether to return the selected plugin on the
      channel rack if none are explicitly active

    Returns:
    * `None`: if no plugin is focused
    * `int`: grouped index of a channel rack plugin if one is focused
    * `int, int`: index of a mixer plugin if one is focused
    """
    # Check if a channel rack plugin is focused
    # if ui.getFocused(7):
    form_id = ui.getFocusedFormID()

    # If a mixer plugin is focused
    if ui.getFocused(6):
        track = form_id // 4194304
        slot = (form_id - 4194304 * track) // 65536
        return track, slot
    # Otherwise, assume that a channel is selected
    # Use the channel rack index so that we always have one
    elif ui.getFocused(7):
        # NOTE: When using groups, ui.getFocusedFormID() returns the index
        # respecting groups, instead of the global index, yuck
        if form_id == -1:
            # Plugin outside current group or invalid
            return None
        return (form_id,)
    else:
        if force:
            return (channels.selectedChannel(),)
        else:
            return None


def getFocusedWindowIndex() -> Optional[int]:
    """
    Fixes the horrible ui.getFocusedFormIndex() function

    Values are returned as tuples so that they can be unwrapped when

    Returns:
        * `None`: if no window is focused
        * `int`: index of window
    """
    # Check if a channel rack plugin is focused
    if getFocusedPluginIndex() is not None:
        return None
    else:
        ret = ui.getFocusedFormID()
        if ret == -1:
            return None
        return ret

# def getPluginName(index: UnsafeIndex) -> str:
#     """
#     Returns the name of a plugin
#
#     ### Args:
#     * `index` (`PluginIndex`): index of plugin
#
#     ### Returns:
#     * `str`: plugin name
#     """
#     # Nothing selected
#     if index is None:
#         return ""
#
#     # FL Window
#     if isinstance(index, int):
#         return {
#             0: "Mixer",
#             1: "Channel Rack",
#             2: "Playlist",
#             3: "Piano Roll",
#             4: "Browser"
#         }[index]
#
#     # Generator
#     elif len(index) == 1:
#         return plugins.get


def isPluginVst(index: PluginIndex) -> bool:
    """
    Returns whether a plugin is a VST

    ### Args:
    * `index` (`PluginIndex`): plugin index
    """
    return plugins.getParamCount(*index) > PARAM_CC_START


def getSelectedPlaylistTrack() -> int:
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


def catchUnsafeOperation(func):
    """
    Decorator to prevent exceptions due to unsafe operations

    ### Args:
    * `func` (`Callable`): function to decorate
    """
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except TypeError as e:
            if e.args != ("Operation unsafe at current time",):
                raise e
    return wrapper


def getSelectedDockMixerTracks() -> dict[int, list[int]]:
    """
    Returns a list of the selected mixer tracks for each dock side, not
    including master or current

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
    for i in range(1, mixer.trackCount() - 1):
        if mixer.isTrackSelected(i):
            tracks[mixer.getTrackDockSide(i)].append(i)

    return tracks


def getSelectedMixerTracks() -> list[int]:
    """
    Returns a list of the selected mixer tracks, not including master or
    current

    ### Returns:
    * `list[int]`: track selections
    """
    tracks: list[int] = []
    for i in range(1, mixer.trackCount() - 1):
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
