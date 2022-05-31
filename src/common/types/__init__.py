"""
common > types

Contains type definitions used by the script, including:
* `Color`, used to manage colors in the script
* `EventData`, used as a shadow for the real `eventData` type when testing and
  type hinting

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""

__all__ = [
    'Color',
    'EventData',
]

from .event_data import EventData
from .color import Color
