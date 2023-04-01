"""
control_surfaces > controls

Contains the definitions for all base classes for control surfaces used by the
script.

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""

__all__ = [
    'ControlSurface',
    'NullControl',
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
    'GenericFader',
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
    'GenericKnob',
    'Knob',
    'MasterKnob',
    'Encoder',
    'ModXY',
    'ModX',
    'ModY',
    'DrumPad',
    'ToolSelector',
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
    'Ambient',
    'ActivitySwitcher',
]

from .control_surface import ControlSurface
from .null_control import NullControl
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
from .fader import GenericFader, Fader, MasterFader
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
from .knob import GenericKnob, Knob, MasterKnob
from .encoder import Encoder
from .mod_xy import ModXY, ModX, ModY
from .drum_pad import DrumPad
from .tool_selector import ToolSelector

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
from .ambient import Ambient
from .activity_switcher import ActivitySwitcher
