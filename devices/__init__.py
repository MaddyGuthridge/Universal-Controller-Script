"""
devices

Contains definitions for devices, allowing the script to interface with them

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]
"""

from .controlmatcher import IControlMatcher
from .device import Device
from .deviceshadow import DeviceShadow, EventCallback
from .controlmatcher import IControlMatcher, BasicControlMatcher

from . import controlgenerators

# Device manufacturers
from . import novation, maudio
