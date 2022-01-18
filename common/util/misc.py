"""
common > util > misc

Miscellaneous tools and things
"""

class _NoneNoPrintout:
    """
    A thing that can be returned instead of None, so that we don't get those
    ugly `None` printouts after user interaction
    """
    def __repr__(self) -> str:
        return ''

NoneNoPrintout = _NoneNoPrintout()

