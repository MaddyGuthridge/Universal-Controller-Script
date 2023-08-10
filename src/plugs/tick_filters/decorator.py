"""
plugs > tick_filters > decorator

A horrible decorator for decorating decorators.

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""
from typing import Callable
from typing_extensions import TypeAlias
from common.plug_indexes.fl_index import FlIndex

TickCallback: TypeAlias = Callable[[FlIndex], bool]


def do_filter(callback: TickCallback):
    """
    Decorator to decorate our decorators

    This removes the massive amount of repeated code used by index filters.

    The callback is called with the given args and returns whether the main
    function should process the event.

    This has to be the most horrendous decorator I have ever written
    """
    def decorator(
        method: bool = True,
        enforce: bool = False,
        filtered_return: bool = False,
    ) -> Callable[[Callable], TickCallback]:
        """
        Filter decorator

        Filters out events where events don't match a certain specification

        ### Args:
        * `method` (`bool`, optional): Whether the function to call is a method
          containing a `self` argument or not. Defaults to `True`.

        * `enforce` (`bool`, optional): Whether an error should be raised if we
          are given the wrong type of index. Defaults to `False`.

        * `filtered_return` (`bool`, optional): What the default return value
          should be when an event is filtered, if we're not enforcing the
          filter. Defaults to `False`.
        """
        def wrapper_creator(func) -> TickCallback:
            if method:
                def wrapper_method(
                    self,
                    index: FlIndex,
                    *args,
                ) -> bool:
                    if callback(index):
                        return func(self, index, *args)  # type: ignore
                    if enforce:
                        raise TypeError("Index not filtered correctly")
                    return filtered_return
                # Can't be bothered to actually get this working correctly
                return wrapper_method  # type: ignore
            else:
                def wrapper(
                    index: FlIndex,
                    *args,
                ) -> bool:
                    if callback(index):
                        return func(index, *args)  # type: ignore
                    if enforce:
                        raise TypeError("Index not filtered correctly")
                    return filtered_return
                return wrapper
        return wrapper_creator
    return decorator
