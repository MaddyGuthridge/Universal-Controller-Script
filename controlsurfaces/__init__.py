"""
controlsurfaces

Contains definitions for basic control surface types, which can be extended by
controllers if necessary.

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]
"""

from . import consts
from .controlsurface import ControlSurface
from .controlshadow import ControlShadow
from .controlmapping import ControlMapping
from .valuestrategies import *

from .nullevent import *
from .note import Note
from .wheels import *
from .aftertouch import *
from .pedal import *
from .button import *
from .transport import *
from .navigation import *
from .jog import *
from .fader import Fader
from .knob import Knob
from .encoder import Encoder
from .drumpad import DrumPad
