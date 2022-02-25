"""
plugs > eventfilters > index

Contains filters for filtering by plugin and window indexes
"""
from typing import Any
from common.util.apifixes import UnsafePluginIndex
from controlsurfaces import ControlShadowEvent

def toPluginIndex(func, method:bool=True):
    """
    Filter out events when the index is not a plugin

    ### Args:
    * `func` (`EventCallback`): Function to decorate
    * `method` (`bool`, optional): Whether to include a self parameter. Defaults
      to `True`.

    ### Returns:
    * `EventCallback`: decorated function
    """
    if method:
        def wrapper_method(self, control: ControlShadowEvent, index: UnsafePluginIndex, *args: Any, **kwargs: Any) -> bool:
            if not isinstance(index, tuple):
                return False
            return func(self, control, index, *args, **kwargs)
        return wrapper_method
    else:
        def wrapper(control: ControlShadowEvent, index: UnsafePluginIndex, *args: Any, **kwargs: Any) -> bool:
            if not isinstance(index, tuple):
                return False
            return func(control, index, *args, **kwargs)
        return wrapper

def toGeneratorIndex(func, method:bool=True):
    """
    Filter out events when the index is not a generator plugin

    ### Args:
    * `func` (`EventCallback`): Function to decorate
    * `method` (`bool`, optional): Whether to include a self parameter. Defaults
      to `True`.

    ### Returns:
    * `EventCallback`: decorated function
    """
    if method:
        def wrapper_method(self, control: ControlShadowEvent, index: UnsafePluginIndex, *args: Any, **kwargs: Any) -> bool:
            if not isinstance(index, tuple) or len(index) != 1:
                return False
            return func(self, control, index, *args, **kwargs)
        return wrapper_method
    else:
        def wrapper(control: ControlShadowEvent, index: UnsafePluginIndex, *args: Any, **kwargs: Any) -> bool:
            if not isinstance(index, tuple) or len(index) != 1:
                return False
            return func(control, index, *args, **kwargs)
        return wrapper

def toEffectIndex(func, method:bool=True):
    """
    Filter out events when the index is not an effect plugin

    ### Args:
    * `func` (`EventCallback`): Function to decorate
    * `method` (`bool`, optional): Whether to include a self parameter. Defaults
      to `True`.

    ### Returns:
    * `EventCallback`: decorated function
    """
    if method:
        def wrapper_method(self, control: ControlShadowEvent, index: UnsafePluginIndex, *args: Any, **kwargs: Any) -> bool:
            if not isinstance(index, tuple) or len(index) != 2:
                return False
            return func(self, control, index, *args, **kwargs)
        return wrapper_method
    else:
        def wrapper(control: ControlShadowEvent, index: UnsafePluginIndex, *args: Any, **kwargs: Any) -> bool:
            if not isinstance(index, tuple) or len(index) != 2:
                return False
            return func(control, index, *args, **kwargs)
        return wrapper

def toWindowIndex(func, method:bool=True):
    """
    Filter out events when the index is not a window

    ### Args:
    * `func` (`EventCallback`): Function to decorate
    * `method` (`bool`, optional): Whether to include a self parameter. Defaults
      to `True`.

    ### Returns:
    * `EventCallback`: decorated function
    """
    if method:
        def wrapper_method(self, control: ControlShadowEvent, index: UnsafePluginIndex, *args: Any, **kwargs: Any) -> bool:
            if not isinstance(index, int):
                return False
            return func(self, control, index, *args, **kwargs)
        return wrapper_method
    else:
        def wrapper(control: ControlShadowEvent, index: UnsafePluginIndex, *args: Any, **kwargs: Any) -> bool:
            if not isinstance(index, int):
                return False
            return func(control, index, *args, **kwargs)
        return wrapper

def toSafeIndex(func, method:bool=True):
    """
    Filter out events when the index is None

    ### Args:
    * `func` (`EventCallback`): Function to decorate
    * `method` (`bool`, optional): Whether to include a self parameter. Defaults
      to `True`.

    ### Returns:
    * `EventCallback`: decorated function
    """
    if method:
        def wrapper_method(self, control: ControlShadowEvent, index: UnsafePluginIndex, *args: Any, **kwargs: Any) -> bool:
            if index is None:
                return False
            return func(self, control, index, *args, **kwargs)
        return wrapper_method
    else:
        def wrapper(control: ControlShadowEvent, index: UnsafePluginIndex, *args: Any, **kwargs: Any) -> bool:
            if index is None:
                return False
            return func(control, index, *args, **kwargs)
        return wrapper
