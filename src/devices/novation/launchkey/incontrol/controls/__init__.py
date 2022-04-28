"""
devices > novation > incontrol > controls

Definitions for controls shared between Novation devices
"""

__all__ = [
    'InControlSurface',
    'LkDirectionNext',
    'LkDirectionPrevious',
    'LkFastForwardButton',
    'LkMk2LoopButton',
    'LkMk3LoopButton',
    'LkMk2StopButton',
    'LkMk3StopButton',
    'LkPlayButton',
    'LkRecordButton',
    'LkRewindButton',
    'LkMk2DrumPad',
    'LkMk3DrumPad',
    'LkDrumPadMatcher',
    'LkFader',
    'LkMasterFader',
    'LkFaderButton',
    'LkMasterFaderButton',
    'LkFaderSet',
    'LkKnob',
    'LkKnobSet',
    'LkMk2MetronomeButton',
    'LkMk2ControlSwitchButton',
    'LkMk3ControlSwitchButton',
    'LkCaptureMidiButton',
    'LkQuantizeButton',
    'LkMetronomeButton',
    'LkUndoRedoButton',
]

from .incontrolsurface import InControlSurface
from .transport import (
    LkDirectionNext,
    LkDirectionPrevious,
    LkFastForwardButton,
    LkPlayButton,
    LkRecordButton,
    LkRewindButton,
    LkMk2LoopButton,
    LkMk2StopButton,
    LkMk3LoopButton,
    LkMk3StopButton,
    LkCaptureMidiButton,
    LkQuantizeButton,
    LkMetronomeButton,
    LkUndoRedoButton,
)
from .drumpad import (
    LkMk2DrumPad,
    LkMk3DrumPad,
    LkDrumPadMatcher,
)
from .fader import (
    LkFader,
    LkMasterFader,
    LkFaderButton,
    LkMasterFaderButton,
    LkFaderSet,
)
from .knob import (
    LkKnob,
    LkKnobSet,
)
from .metronome import (
    LkMk2MetronomeButton,
)
from .controlswitch import (
    LkMk2ControlSwitchButton,
    LkMk3ControlSwitchButton,
)
