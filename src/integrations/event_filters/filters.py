"""
integrations > event_filters > filters

Decorators to filter out events based on the type of event

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
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
