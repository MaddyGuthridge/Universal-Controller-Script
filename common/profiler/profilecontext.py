"""
common > profiler > profilecontext

Context manager definition for profiler
"""

import common

class ProfilerContext:
    """
    Represents a context used to profile performance in the script. Supports
    nested profiles, and presents the data in a json-like structure, to allow
    for simple analysis

    Example usage:
    
    >>> with ProfilerContext("Costly operation"):
    >>>     costlyOperation()
    >>> # Outside context
    "'Costly operation' (1000 ns)": [sub operations]
    """
    def __init__(self, name: str) -> None:
        self._name = name
    
    def __enter__(self):
        common.getContext().profiler.openProfile(self._name)

    def __exit__(self):
        common.getContext().profiler.openProfile(self._name)
