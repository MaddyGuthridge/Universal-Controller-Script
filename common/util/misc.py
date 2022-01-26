"""
common > util > misc

Miscellaneous tools and things
"""

import sys

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
    elif hasattr(obj, '__iter__') and not isinstance(obj, (str, bytes, bytearray)):
        size += sum([sizeof(i, seen) for i in obj])
    return size
