"""
devices > novation > launchkey > incontrol > controls

Definitions for controls shared between Novation Launchkey devices

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""

__all__ = [
    'ColorInControlSurface',
    'GrayscaleInControlSurface',
    'LkMk2DirectionNext',
    'LkMk2DirectionPrevious',
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
    'LkMk2Fader',
    'LkMk2MasterFader',
    'LkMk2FaderButton',
    'LkMk2MasterFaderButton',
    'LkMk2FaderSet',
    'LkMk3Fader',
    'LkMk3MasterFader',
    'LkMk3FaderButton',
    'LkMk3FaderSet',
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
    'Mk3DirectionUpSilenced',
    'Mk3DirectionDownSilenced',
    'StopSoloMuteButton',
    'LkMk3DrumPadMute',
    'LkMk3DrumPadSolo',
    'LkMk3DrumPadActivity',
    'LkMk3MiniDrumPadActivity',
    'LkPauseActive',
    'LkDeviceSelect',
]

from .incontrol_surface import ColorInControlSurface, GrayscaleInControlSurface
from .transport import (
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
    LkMk3DrumPadActivity,
    LkMk3MiniDrumPadActivity,
)
from .faders import (
    LkMk2Fader,
    LkMk2MasterFader,
    LkMk2FaderButton,
    LkMk2MasterFaderButton,
    LkMk2FaderSet,
    LkMk3Fader,
    LkMk3MasterFader,
    LkMk3FaderButton,
    LkMk3FaderSet,
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
    LkMk2DirectionNext,
    LkMk2DirectionPrevious,
    Mk3DirectionLeft,
    Mk3DirectionRight,
    MiniMk3DirectionUp,
    MiniMk3DirectionDown,
    Mk3DirectionUp,
    Mk3DirectionDown,
    Mk3DirectionUpSilenced,
    Mk3DirectionDownSilenced,
)
from .mutes import (
    StopSoloMuteButton,
)
from .activity import LkPauseActive, LkDeviceSelect
