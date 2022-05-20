"""
controlsurfaces > valuestrategies

Contains deinitions for value strategies, as well as the IValueStrategy
interface.

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]
"""

__all__ = [
    'IValueStrategy',
    'NoteStrategy',
    'Data2Strategy',
    'Data1Strategy',
    'TwosComplimentDeltaStrategy',
    'ButtonData2Strategy',
    'ButtonSinglePressStrategy',
    'ForwardedStrategy',
    'ForwardedUnionStrategy',
    'NullEventStrategy',
]

from .value_strategy import IValueStrategy
from .note_strategy import NoteStrategy
from .data_strategy import Data2Strategy, Data1Strategy
from .twos_compliment_delta import TwosComplimentDeltaStrategy
from .buttondata2strategy import ButtonData2Strategy
from .button_single_press_strategy import ButtonSinglePressStrategy
from .forwarded_strategy import ForwardedStrategy, ForwardedUnionStrategy
from .null_strategy import NullEventStrategy
