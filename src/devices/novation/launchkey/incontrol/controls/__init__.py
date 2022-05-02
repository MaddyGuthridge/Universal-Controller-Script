"""
devices > novation > incontrol > controls

Definitions for controls shared between Novation devices
"""

__all__ = [
    'ColorInControlSurface',
    'LkDirectionNext',
    'LkDirectionPrevious',
    'LkFastForwardButton',
    'LkMk2LoopButton',
    'LkMk3LoopButton',
    'LkMk2StopButton',
    'LkMk3StopButton',
    'LkMk2PlayButton',
    'LkMk3PlayButton',
    'LkMk2RecordButton',
    'LkMk3RecordButton',
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
    'LkMk3MetronomeButton',
    'LkMk2ControlSwitchButton',
    'LkMk3ControlSwitchButton',
    'LkCaptureMidiButton',
    'LkQuantizeButton',
    'LkUndoRedoButton',
]

from .incontrolsurface import ColorInControlSurface
from .transport import (
    LkDirectionNext,
    LkDirectionPrevious,
    LkFastForwardButton,
    LkRewindButton,
    LkMk2LoopButton,
    LkMk3LoopButton,
    LkMk2StopButton,
    LkMk3StopButton,
    LkMk2PlayButton,
    LkMk3PlayButton,
    LkMk2RecordButton,
    LkMk3RecordButton,
    LkCaptureMidiButton,
    LkQuantizeButton,
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
    LkMk3MetronomeButton,
)
from .controlswitch import (
    LkMk2ControlSwitchButton,
    LkMk3ControlSwitchButton,
)
