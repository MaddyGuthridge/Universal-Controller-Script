"""
plugs > event_filters > filters

Decorators to filter out events based on the type of event
"""

__all__ = [
    'filterButtonLift',
]

from typing import Any
from common.util.api_fixes import UnsafePluginIndex
from control_surfaces import ControlShadowEvent, Button

# TODO: Remove repeated code here (maybe use a class decorator with a
# __call__() function?)


def filterButtonLift(func, method: bool = True):
    """
    Filter out button lifts so that only presses are processed

    ### Args:
    * `func` (`EventCallback`): Function to decorate
    * `method` (`bool`, optional): Whether to include a self parameter.
      Defaults to `True`.

    ### Returns:
    * `EventCallback`: decorated function
    """
    if method:
        def wrapper_method(
            self,
            control: ControlShadowEvent,
            index: UnsafePluginIndex,
            *args: Any,
            **kwargs: Any
        ) -> bool:
            # Filter button lifts
            if isinstance(control.getControl(), Button):
                if control.value == 0.0:
                    return True
            return func(self, control, index, *args, **kwargs)
        return wrapper_method
    else:
        def wrapper(
            control: ControlShadowEvent,
            index: UnsafePluginIndex,
            *args: Any,
            **kwargs: Any
        ) -> bool:
            # Filter button lifts
            if isinstance(control.getControl(), Button):
                if control.value == 0.0:
                    return True
            return func(control, index, *args, **kwargs)
        return wrapper
