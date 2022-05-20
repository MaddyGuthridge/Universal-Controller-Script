"""
devices

Contains definitions for devices, allowing the script to interface with them

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]
"""

__all__ = [
    'Device',
    'DeviceShadow',
    'EventCallback',
    'IControlMatcher',
    'BasicControlMatcher',
]

from .matchers import IControlMatcher, BasicControlMatcher
from .device import Device
from .device_shadow import DeviceShadow, EventCallback

# Device manufacturers
from . import (
    novation,
    maudio,
    korg,
)
del (
    novation,
    maudio,
    korg,
)
