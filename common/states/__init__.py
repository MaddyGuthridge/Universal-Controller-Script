"""
common > states

Defines states used by the script
"""

__all__ = [
    'IScriptState',
    'catchStateChangeException',
    'StateChangeException',
    'MainState',
    'DeviceNotRecognised',
    'WaitingForDevice',
]

from .scriptstate import (
    IScriptState,
    catchStateChangeException,
    StateChangeException,
)
from .mainstate import MainState
from .notrecognised import DeviceNotRecognised
from .devicedetect import WaitingForDevice
