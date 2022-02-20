"""
common > types

Contains type definitions used by the script, including:
* `Color`, used to manage colors in the script
* `eventData`, used as a shadow for the real `eventData` type when testing and
  type hinting

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]
"""

from .eventdata import EventData
from .color import Color
