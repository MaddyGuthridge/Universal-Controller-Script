"""
common > profiler > profilecontext

Context manager definition for profiler
"""

import common
from typing import TypeVar, Callable
from typing_extensions import ParamSpec

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
        c = common.getContext()
        if c.profiler is not None:
            c.profiler.openProfile(self._name)

    def __exit__(self, exc_type, exc_value, exc_traceback):
        c = common.getContext()
        if c.profiler is not None:
            c.profiler.closeProfile()


Params = ParamSpec("Params")
RT = TypeVar("RT")

def profilerDecoration(name):
    def decorator(func: Callable[Params, RT]) -> Callable[Params, RT]:
        def wrapper(*args, **kwargs):
            with ProfilerContext(name):
                return func(*args, **kwargs)
        return wrapper
    return decorator
