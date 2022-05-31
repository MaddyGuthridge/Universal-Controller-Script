"""
control_surfaces > controls > transport

Defines transport control surfaces

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""
__all__ = [
    'TransportButton',
    'PlayButton',
    'StopButton',
    'LoopButton',
    'RecordButton',
    'FastForwardButton',
    'RewindButton',
    'MetronomeButton',
]

from ..event_patterns import IEventPattern
from control_surfaces.value_strategies import IValueStrategy
from .button import Button


class TransportButton(Button):
    """
    Represents buttons used for transport within FL Studio
    """

    def __init__(
        self,
        event_pattern: IEventPattern,
        value_strategy: IValueStrategy
    ) -> None:
        super().__init__(event_pattern, value_strategy)


class PlayButton(TransportButton):
    """
    Represents a play button
    """


class StopButton(TransportButton):
    """
    Represents a stop button
    """


class LoopButton(TransportButton):
    """
    Represents a loop button.

    This maps to change the loop mode in FL Studio between pattern and song.
    """


class RecordButton(TransportButton):
    """
    Represents a record button
    """


class FastForwardButton(TransportButton):
    """
    Represents a fast-forward button
    """


class RewindButton(TransportButton):
    """
    Represents a rewind button
    """


class MetronomeButton(TransportButton):
    """
    Represents a metronome button

    This toggles the metronome in FL Studio
    """
