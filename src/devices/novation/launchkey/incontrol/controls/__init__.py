"""
devices > novation > incontrol > controls

Definitions for controls shared between Novation devices
"""

__all__ = [
    'ColorInControlSurface',
    'GrayscaleInControlSurface',
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
    'LkMk3CaptureMidiButton',
    'LkQuantizeButton',
    'LkUndoRedoButton',
    'Mk3DirectionLeft',
    'Mk3DirectionRight',
    'MiniMk3DirectionUp',
    'MiniMk3DirectionDown',
    'Mk3DirectionUp',
    'Mk3DirectionDown',
    'StopSoloMuteButton',
    'LkMk3DrumPadMute',
    'LkMk3DrumPadSolo',
    'getMiniMuteControls',
]

from .incontrol_surface import ColorInControlSurface, GrayscaleInControlSurface
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
    LkMk3CaptureMidiButton,
    LkQuantizeButton,
    LkUndoRedoButton,
)
from .drum_pad import (
    LkMk2DrumPad,
    LkMk3DrumPad,
    LkDrumPadMatcher,
    LkMk3DrumPadMute,
    LkMk3DrumPadSolo,
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
from .control_switch import (
    LkMk2ControlSwitchButton,
    LkMk3ControlSwitchButton,
)
from .navigation import (
    Mk3DirectionLeft,
    Mk3DirectionRight,
    MiniMk3DirectionUp,
    MiniMk3DirectionDown,
    Mk3DirectionUp,
    Mk3DirectionDown,
)
from .mutes import (
    StopSoloMuteButton,
    getMiniMuteControls,
)
