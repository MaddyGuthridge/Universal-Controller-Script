"""
plugs > event_filters > filters

Decorators to filter out events based on the type of event
"""

__all__ = [
    'filterButtonLift',
]

from control_surfaces import ControlShadowEvent, Button
from .decorator import do_filter


@do_filter
def filterButtonLift(control: ControlShadowEvent, index, *args, **kwargs):
    """
    Filter out button lifts so that only presses are processed
    """
    if isinstance(control.getControl(), Button):
        if control.value == 0.0:
            return False
    return True
