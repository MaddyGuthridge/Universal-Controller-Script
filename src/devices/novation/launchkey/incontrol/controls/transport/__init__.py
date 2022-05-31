"""
devices > novation > launchkey > incontrol > controls > transport

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""
__all__ = [
    'LkFastForwardButton',
    'LkPlayButton',
    'LkRecordButton',
    'LkRewindButton',
    'LkQuantizeButton',
    'LkUndoRedoButton',
    'LkMk3CaptureMidiButton',
    'LkMk2LoopButton',
    'LkMk3LoopButton',
    'LkMk2StopButton',
    'LkMk3StopButton',
    'LkMk2PlayButton',
    'LkMk3PlayButton',
    'LkMk2RecordButton',
    'LkMk3RecordButton',
]

from .common import (
    LkFastForwardButton,
    LkRewindButton,
    LkQuantizeButton,
    LkUndoRedoButton,
)
from .mk2 import (
    LkMk2LoopButton,
    LkMk2StopButton,
    LkMk2PlayButton,
    LkMk2RecordButton,
)
from .mk3 import (
    LkMk3LoopButton,
    LkMk3StopButton,
    LkMk3PlayButton,
    LkMk3RecordButton,
    LkMk3CaptureMidiButton,
)
