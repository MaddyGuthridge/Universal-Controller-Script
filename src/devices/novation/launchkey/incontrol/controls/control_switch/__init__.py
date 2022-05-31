"""
devices > novation > launchkey > incontrol > controls > control_switch

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""

__all__ = [
    'LkControlSwitchButton',
    'LkMk2ControlSwitchButton',
    'LkMk3ControlSwitchButton',
]

from .control_switch import LkControlSwitchButton
from .mk2 import LkMk2ControlSwitchButton
from .mk3 import LkMk3ControlSwitchButton
