"""
devices

Contains definitions for devices, allowing the script to interface with them

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""

__all__ = [
    'Device',
    'DeviceShadow',
    'EventCallback',
]

from .device import Device
from .device_shadow import DeviceShadow, EventCallback

# Device manufacturers
from . import (
    akai,
    novation,
    maudio,
    korg,
)
del (
    akai,
    novation,
    maudio,
    korg,
)
