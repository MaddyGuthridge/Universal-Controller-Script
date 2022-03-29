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
    'ButtonData2Strategy',
    'ButtonSinglePressStrategy',
    'ForwardedStrategy',
    'ForwardedUnionStrategy',
    'NullEventStrategy'
]

from .ivaluestrategy import IValueStrategy
from .notestrategy import NoteStrategy
from .datastrategy import Data2Strategy, Data1Strategy
from .buttondata2strategy import ButtonData2Strategy
from .buttonsinglepressstrategy import ButtonSinglePressStrategy
from .forwardedstrategy import ForwardedStrategy, ForwardedUnionStrategy
from .nullstrategy import NullEventStrategy
