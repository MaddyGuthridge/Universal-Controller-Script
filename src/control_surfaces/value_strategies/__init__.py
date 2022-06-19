"""
control_surfaces > value_strategies

Contains definitions for value strategies, as well as the IValueStrategy
interface.

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
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
    'NullStrategy',
]

from .value_strategy import IValueStrategy
from .note_strategy import NoteStrategy
from .data_strategy import Data2Strategy, Data1Strategy
from .twos_compliment_delta import TwosComplimentDeltaStrategy
from .button_data2_strategy import ButtonData2Strategy
from .button_single_press_strategy import ButtonSinglePressStrategy
from .forwarded_strategy import ForwardedStrategy, ForwardedUnionStrategy
from .null_strategy import NullStrategy
