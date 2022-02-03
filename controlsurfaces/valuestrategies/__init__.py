"""
controlsurfaces > valuestrategies

Contains deinitions for value strategies, as well as the IValueStrategy
interface.

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]
"""
from .ivaluestrategy import IValueStrategy

from .datastrategy import Data2Strategy, Data1Strategy
from .buttondata2strategy import ButtonData2Strategy
from .buttonsinglepressstrategy import ButtonSinglePressStrategy
from .forwardedstrategy import ForwardedStrategy
from .nullstrategy import NullEventStrategy
