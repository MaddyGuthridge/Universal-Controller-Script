"""
common > util > misc

Miscellaneous tools and things

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""

import math
import sys
import time


class _NoneNoPrintout:
    """
    A thing that can be returned instead of None, so that we don't get those
    ugly `None` printouts after user interaction
    """

    def __repr__(self) -> str:
        return ''


NoneNoPrintout = _NoneNoPrintout()


def sizeof(obj, seen=None):
    """
    Recursively finds size of objects.

    Source:
    https://goshippo.com/blog/measure-real-size-any-python-object/
    """
    size = sys.getsizeof(obj)
    if seen is None:
        seen = set()
    obj_id = id(obj)
    if obj_id in seen:
        return 0
    # Important mark as seen *before* entering recursion to gracefully handle
    # self-referential objects
    seen.add(obj_id)
    if isinstance(obj, dict):
        size += sum([sizeof(v, seen) for v in obj.values()])
        size += sum([sizeof(k, seen) for k in obj.keys()])
    elif hasattr(obj, '__dict__'):
        size += sizeof(obj.__dict__, seen)
    elif hasattr(obj, '__iter__') and not isinstance(
        obj,
        (str, bytes, bytearray)
    ):
        size += sum([sizeof(i, seen) for i in obj])
    return size


def formatTime(t: float) -> str:
    """
    Format time as a string

    ### Args:
    * `time` (`time`): time to format

    ### Returns:
    * `str`: formatted time
    """
    t_obj = time.localtime(t)
    return f"{t_obj.tm_hour:02}:{t_obj.tm_min:02}:{t_obj.tm_sec:02}"


def formatLongTime(t: float) -> str:
    """
    Format time as a string including milliseconds

    ### Args:
    * `time` (`time`): time to format

    ### Returns:
    * `str`: formatted time
    """
    t_obj = time.localtime(t)
    ms = f"{t - math.floor(t):.3}".lstrip("0.")
    return f"{t_obj.tm_hour:02}:{t_obj.tm_min:02}:{t_obj.tm_sec:02}.{ms}"


def clamp(value: float, lower: float, upper: float) -> float:
    """
    Clamp value between lower and upper

    ### Args:
    * `value` (`float`): value to clamp
    * `lower` (`float`): lowest allowed value
    * `upper` (`float`): greatest allowed value

    ### Returns:
    * `float`: clamped value
    """
    return min(max(value, lower), upper)
