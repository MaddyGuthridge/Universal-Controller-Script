"""
devices > novation > launchkey > incontrol > controls > faders

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""
__all__ = [
    'LkMk2Fader',
    'LkMk2MasterFader',
    'LkMk2FaderButton',
    'LkMk2MasterFaderButton',
    'LkMk2FaderSet',
    'LkMk3Fader',
    'LkMk3MasterFader',
    'LkMk3FaderButton',
    'LkMk3FaderSet',
]

from .mk2 import (
    LkMk2Fader,
    LkMk2MasterFader,
    LkMk2FaderButton,
    LkMk2MasterFaderButton,
    LkMk2FaderSet,
)
from .mk3 import (
    LkMk3Fader,
    LkMk3MasterFader,
    LkMk3FaderButton,
    LkMk3FaderSet,
)
