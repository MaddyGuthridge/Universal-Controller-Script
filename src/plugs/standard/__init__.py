"""
plugs > standard

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""
__all__ = [
    'fl',
    'spitfire',
    'matt_tytel',
    'fallback',
    'basicFaderBuilder',
]

from .basic_faders import basicFaderBuilder

from . import fallback
from . import fl
from . import spitfire
from . import matt_tytel
