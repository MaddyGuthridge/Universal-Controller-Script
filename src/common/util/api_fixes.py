"""
common > util > api_fixes

Contains wrapper code for FL Studio API functions which are just too awful to
be called directly.
"""

import plugins
import ui
import channels
import mixer
import playlist

from typing import Union, Optional
from common.profiler import profilerDecoration, ProfilerContext
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


# HACK: A terrible horrible no good really bad global variable to make sure
# that we hopefully avoid crashes in getFocusedPluginIndex
generator_previously_active = 0


def reset_generator_active():
    """Horrible hacky function to hopefully work around a bug in FL Studio"""
    global generator_previously_active
    if generator_previously_active != 0:
        generator_previously_active -= 1


@profilerDecoration("getFocusedPluginIndex")
def getFocusedPluginIndex(force: bool = False) -> UnsafePluginIndex:
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
    # HACK: Move this elsewhere
    global generator_previously_active
    with ProfilerContext("getFocused"):
        # for i in range(8):
        #     print(f"    {ui.getFocused(i)=}, {i=}")
        ui_6 = ui.getFocused(6)
        ui_7 = ui.getFocused(7)
    # If a mixer plugin is focused
    if ui_6:
        # HACK: Error checking to hopefully avoid a crash due to bugs in FL
        # Studio
        if generator_previously_active:
            print("getFocusedPluginIndex() crash prevention")
            return None
        with ProfilerContext("getFocusedFormID @ mixer"):
            form_id = ui.getFocusedFormID()
        track = form_id // 4194304
        slot = (form_id - 4194304 * track) // 65536
        return track, slot
    # Otherwise, assume that a channel is selected
    # Use the channel rack index so that we always have one
    elif ui_7:
        generator_previously_active = 3
        with ProfilerContext("getFocusedFormID @ cr"):
            form_id = ui.getFocusedFormID()
        # NOTE: When using groups, ui.getFocusedFormID() returns the index
        # respecting groups, instead of the global index, yuck
        if form_id == -1:
            # Plugin outside current group or invalid
            return None
        return (form_id,)
    else:
        generator_previously_active = 3
        if force:
            with ProfilerContext("selectedChannel"):
                ret = (channels.selectedChannel(),)
            return ret
        else:
            return None


@profilerDecoration("getFocusedWindowIndex")
def getFocusedWindowIndex() -> Optional[int]:
    """
    Fixes the horrible ui.getFocused() function

    Returns:
        * `None`: if no window is focused
        * `int`: index of window
    """
    for i in range(5):
        if ui.getFocused(i):
            return i
    return None


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
    try:
        return plugins.getParamCount(*index) > PARAM_CC_START
    except TypeError:
        return False


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


def getSelectedChannels(global_mode: bool) -> list[int]:
    """
    Returns a list of the selected channels on the channel rack

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
