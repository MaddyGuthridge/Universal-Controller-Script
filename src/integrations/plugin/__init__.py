"""
integrations > plugin

Contains plugin integrations

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""
__all__ = [
    'basicPluginBuilder',
    'default_integration',
    'fl',
    'klevgrand',
    'matt_tytel',
    'spitfire',
    'xfer',
]

from .basic_faders import basicPluginBuilder
from . import (
    default_integration,
    fl,
    klevgrand,
    matt_tytel,
    spitfire,
    xfer,
)
