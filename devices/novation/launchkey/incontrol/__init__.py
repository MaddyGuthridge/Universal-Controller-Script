"""
devices > novation > launchkey > incontrol

Contains common code for managing devices that use Novation's InControl
protocol.
"""

__all__ = [
    'colors',
    'InControl',
    'InControlMatcher',
    'LkMk2DrumPad',
    'LkMk3DrumPad',
    'LkMk2ControlSwitchButton',
    'LkMk2MetronomeButton',
]

from . import colors
from .incontrol import InControl, InControlMatcher
from .drumpad import LkMk2DrumPad, LkMk3DrumPad
from .controlswitch import LkMk2ControlSwitchButton
from .metronome import LkMk2MetronomeButton
