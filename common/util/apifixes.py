"""
common > util > apifixes

Contains wrapper code for FL Studio API functions which are just too awful to be
called directly.
"""

import plugins
import ui
import channels
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
    * `int`: index of a channel rack plugin if one is focused
    * `int, int`: index of a mixer plugin if one is focused
    """
    # Check if a channel rack plugin is focused
    # if ui.getFocused(7):

    # If a mixer plugin is focused
    if ui.getFocused(6):
        track = ui.getFocusedFormID() // 4194304
        slot = (ui.getFocusedFormID() - 4194304 * track) // 65536
        return track, slot
    # Otherwise, assume that a channel is selected
    # Use the channel rack index so that we always have one
    elif ui.getFocused(7):
        return (ui.getFocusedFormID(), )
    else:
        if force:
            return (channels.channelNumber(),)
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
