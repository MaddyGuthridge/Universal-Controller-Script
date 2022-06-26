"""
common > types

Contains type definitions used by the script, including:
* `Color`, used to manage colors in the script
* `FlMidiMsg`, used as a shadow for the real `FlMidiMsg` type when testing and
  type hinting

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""

__all__ = [
    'Color',
    'BoolS',
    'TrueS',
    'FalseS',
]

from .color import Color
from .bool_s import BoolS, TrueS, FalseS
