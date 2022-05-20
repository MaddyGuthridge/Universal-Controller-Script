"""
controlsurfaces > controls

Contains the definitions for all base classes for control surfaces used by the
script

Authors:
* Miguel Guthridge [HDSQ#2154]
"""

__all__ = [
    'ControlSurface',
    'NullEvent',
    'Note',
    'ModWheel',
    'PitchWheel',
    'StandardModWheel',
    'StandardPitchWheel',
    'Data2PitchWheel',
    'AfterTouch',
    'ChannelAfterTouch',
    'NoteAfterTouch',
    'Pedal',
    'SustainPedal',
    'SostenutoPedal',
    'SoftPedal',
    'Button',
    'TransportButton',
    'PlayButton',
    'StopButton',
    'LoopButton',
    'RecordButton',
    'FastForwardButton',
    'RewindButton',
    'MetronomeButton',
    'NavigationControl',
    'NavigationButton',
    'DpadButtons',
    'DirectionUp',
    'DirectionDown',
    'DirectionLeft',
    'DirectionRight',
    'DirectionSelect',
    'NextPrevButton',
    'DirectionNext',
    'DirectionPrevious',
    'JogWheel',
    'StandardJogWheel',
    'ShiftedJogWheel',
    'MoveJogWheel',
    'Fader',
    'MasterFader',
    'FaderButton',
    'GenericFaderButton',
    'MasterGenericFaderButton',
    'MuteButton',
    'MasterMuteButton',
    'SoloButton',
    'MasterSoloButton',
    'ArmButton',
    'MasterArmButton',
    'SelectButton',
    'MasterSelectButton',
    'Knob',
    'MasterKnob',
    'Encoder',
    'DrumPad',
    'MacroButton',
    'SaveButton',
    'UndoRedoButton',
    'UndoButton',
    'RedoButton',
    'QuantizeButton',
    'CaptureMidiButton',
    'SwitchActiveButton',
    'SwitchActivePluginButton',
    'SwitchActiveWindowButton',
    'SwitchActiveToggleButton',
    'PauseActiveButton',
    'ControlSwitchButton',
    'HintMsg',
    'NotifMsg',
]

from .control_surface import ControlSurface
from .null_event import NullEvent
from .note import Note
from .wheels import (
    ModWheel,
    PitchWheel,
    StandardModWheel,
    StandardPitchWheel,
    Data2PitchWheel,
)
from .after_touch import (
    AfterTouch,
    ChannelAfterTouch,
    NoteAfterTouch,
)
from .pedal import (
    Pedal,
    SustainPedal,
    SostenutoPedal,
    SoftPedal,
)
from .button import Button, ControlSwitchButton
from .transport import (
    TransportButton,
    PlayButton,
    StopButton,
    LoopButton,
    RecordButton,
    FastForwardButton,
    RewindButton,
    MetronomeButton,
)
from .navigation import (
    NavigationControl,
    NavigationButton,
    DpadButtons,
    DirectionUp,
    DirectionDown,
    DirectionLeft,
    DirectionRight,
    DirectionSelect,
    NextPrevButton,
    DirectionNext,
    DirectionPrevious,
)
from .jog import (
    JogWheel,
    StandardJogWheel,
    ShiftedJogWheel,
    MoveJogWheel,
)
from .fader import Fader, MasterFader
from .fader_button import (
    FaderButton,
    GenericFaderButton,
    MasterGenericFaderButton,
    MuteButton,
    MasterMuteButton,
    SoloButton,
    MasterSoloButton,
    ArmButton,
    MasterArmButton,
    SelectButton,
    MasterSelectButton,
)
from .knob import Knob, MasterKnob
from .encoder import Encoder
from .drum_pad import DrumPad

from .macro_button import (
    MacroButton,
    SaveButton,
    UndoRedoButton,
    UndoButton,
    RedoButton,
    QuantizeButton,
    CaptureMidiButton,
)
from .activity_button import (
    SwitchActiveButton,
    SwitchActivePluginButton,
    SwitchActiveWindowButton,
    SwitchActiveToggleButton,
    PauseActiveButton,
)
from .hint_msg import HintMsg
from .notif_msg import NotifMsg
