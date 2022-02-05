"""
common > util > apifixes

Contains wrapper code for FL Studio API functions which are just too awful to be
called directly.
"""

import ui

from typing import Union, Optional

PluginIndex = Union[tuple[int], tuple[int, int]]
UnsafePluginIndex = Optional[PluginIndex]
WindowIndex = int
UnsafeWindowIndex = Optional[int]
UnsafeIndex = Union[UnsafePluginIndex, UnsafeWindowIndex]

def getFocusedPluginIndex() -> UnsafePluginIndex:
    """
    Fixes the horrible ui.getFocusedFormIndex() function
    
    Values are returned as tuples so that they can be unwrapped when 

    Returns:
        * `None`: if no plugin is focused
        * `int`: index of a channel rack plugin if one is focused
        * `int, int`: index of a mixer plugin if one is focused
    """
    # Check if a channel rack plugin is focused
    if ui.getFocused(7):
        return (ui.getFocusedFormID(), )
    # Otherwise, check if a mixer plugin is focused
    elif ui.getFocused(6):
        track = ui.getFocusedFormID() // 4194304
        slot = (ui.getFocusedFormID() - 4194304 * track) // 65536
        return track, slot
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
