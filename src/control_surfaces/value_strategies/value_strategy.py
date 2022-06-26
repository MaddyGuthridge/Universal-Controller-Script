"""
control_surfaces > value_strategies > value_strategy

Contains IValueStrategy: the interface for value strategies.

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""

from abc import abstractmethod
from fl_classes import FlMidiMsg


class IValueStrategy:
    """
    Represents a strategy for getting a value from an event and storing it.

    This can be used alongside basic control surface definitions to define
    relatively simple event types.
    """
    @abstractmethod
    def getValueFromEvent(self, event: FlMidiMsg, value: float) -> float:
        """
        Returns a value given a MIDI event and the current value.

        ### Args:
        * `event` (`FlMidiMsg`): event to get value from
        * `value` (`float`): current value, for use with relative controllers

        ### Returns:
        * `float`: value
        """
        raise NotImplementedError("This function needs to be overridden by "
                                  "child classes")

    @abstractmethod
    def getChannelFromEvent(self, event: FlMidiMsg) -> int:
        """
        Return the channel number associated with an event

        ### Args:
        * `event` (`FlMidiMsg`): event to analyze

        ### Returns:
        * `int`: channel number or `-1` for no channel
        """
        raise NotImplementedError("This function needs to be overridden by "
                                  "child classes")
