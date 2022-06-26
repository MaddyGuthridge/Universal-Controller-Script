"""
devices > novation > launchkey > incontrol > controls > metronome

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""

__all__ = [
    'LkMetronomeButton',
    'LkMk2MetronomeButton',
    'LkMk3MetronomeButton',
]

from .mk2 import LkMk2MetronomeButton
from .mk3 import LkMk3MetronomeButton
