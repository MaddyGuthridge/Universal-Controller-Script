"""
controlsurfaces

Contains definitions for basic control surface types, which can be extended by
controllers if necessary.

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]
"""

__all__ = [
    # Base types
    'ControlSurface',
    'ControlShadow',
    # Control mappings
    'IControlHash',
    'ControlMapping',
    'ControlEvent',
    'ControlShadowEvent',
    # Value Strategies
    'IValueStrategy',
    'NoteStrategy',
    'Data2Strategy',
    'Data1Strategy',
    'ButtonData2Strategy',
    'ButtonSinglePressStrategy',
    'ForwardedStrategy',
    'ForwardedUnionStrategy',
    'NullEventStrategy',
    # Control surfaces
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
    'MuteButton',
    'SoloButton',
    'ArmButton',
    'SelectButton',
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
    'SwitchActiveButton',
    'SwitchActivePluginButton',
    'SwitchActiveWindowButton',
    'SwitchActiveToggleButton',
]

from .controlsurface import ControlSurface
from .controlshadow import ControlShadow
from .controlmapping import (
    IControlHash,
    ControlMapping,
    ControlEvent,
    ControlShadowEvent
)
from .valuestrategies import (
    IValueStrategy,
    NoteStrategy,
    Data2Strategy,
    Data1Strategy,
    ButtonData2Strategy,
    ButtonSinglePressStrategy,
    ForwardedStrategy,
    ForwardedUnionStrategy,
    NullEventStrategy,
)

from .nullevent import NullEvent
from .note import Note
from .wheels import (
    ModWheel,
    PitchWheel,
    StandardModWheel,
    StandardPitchWheel,
    Data2PitchWheel,
)
from .aftertouch import (
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
from .button import Button
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
from .faderbutton import (
    FaderButton,
    GenericFaderButton,
    MuteButton,
    SoloButton,
    ArmButton,
    SelectButton,
)
from .knob import Knob, MasterKnob
from .encoder import Encoder
from .drumpad import DrumPad

from .macrobutton import (
    MacroButton,
    SaveButton,
    UndoRedoButton,
    UndoButton,
    RedoButton,
    QuantizeButton,
    SwitchActiveButton,
    SwitchActivePluginButton,
    SwitchActiveWindowButton,
    SwitchActiveToggleButton,
)
