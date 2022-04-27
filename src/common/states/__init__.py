"""
common > states

Defines states used by the script
"""

__all__ = [
    'IScriptState',
    'catchStateChangeException',
    'StateChangeException',
    'DeviceState',
    'MainState',
    'ForwardState',
    'DeviceNotRecognised',
    'WaitingForDevice',
]

from .scriptstate import (
    IScriptState,
    catchStateChangeException,
    StateChangeException,
)
from .devstate import DeviceState
from .mainstate import MainState
from .forwardstate import ForwardState
from .notrecognised import DeviceNotRecognised
from .devicedetect import WaitingForDevice
