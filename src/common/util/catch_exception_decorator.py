"""
common > util > catch_exception_decorator

Contains `catchExceptionDecorator` which can be used
"""
from typing import Callable, Optional, TypeVar
from typing_extensions import ParamSpec
# from functools import wraps


P = ParamSpec("P")
T = TypeVar("T")
ExcType = TypeVar("ExcType", bound=Exception)


def catchExceptionDecorator(
    exc_type: type[ExcType],
    callback: Optional[Callable[[ExcType], None]] = None,
):
    """
    A decorator for catching exceptions of a certain type, and optionally
    calling a given function when exceptions are given

    ### Args:
    * `exc_type` (`type[Exception]`): type of exception to catch
    * `callback` (`Callable`, optional): callback function for when exceptions
      are caught. Should accept a reference to the exception that was raised.

    ### Usage

    * Catch any `TypeError`s that happen within function `f`

    ```py
    @catchExceptionDecorator(TypeError)
    def f():
        ...
    ```

    * Catch any `IndexError`s that happen within function `h`, and call
      function `g` if one happens

    ```py
    def g(err: ValueError):
        print("A value error occurred:", err)

    @catchExceptionDecorator(ValueError, callback=g)
    def h():
        ...
    ```
    """
    def decorator(func: Callable[P, T]) -> Callable[P, T]:
        # @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except exc_type as e:
                if callback is not None:
                    callback(e)
        return wrapper
    return decorator
