"""
controlsurfaces > valuestrategies > ivaluestrategy

Contains IValueStrategy: the interface for value strategies.

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]
"""

from typing import Any, Generic, TypeVar

from common.types import eventData

T = TypeVar("T")

class IValueStrategy(Generic[T]):
    """
    Represents a strategy for getting a value from an event and storing it.

    This can be used alongside basic control surface definitions to define
    relatively simple event types.
    """
    def getValueFromEvent(self, event: eventData) -> T:
        """
        Returns a value for internal use given a MIDI event.

        This value is only used by the strategy, and therefore can be of any
        reasonable type, as long as that type can be converted to a float value.

        ### Args:
        * `event` (`eventData`): event to get value from

        ### Returns:
        * `T`: any type representing the internal value of the event
        """
        raise NotImplementedError("This function needs to be overridden by "
                                  "child classes")
    
    def getValueFromFloat(self, f: float) -> T:
        """
        Convert a float between 0-1 to the internal value used by this strategy.

        ### Args:
        * `f` (`float`): A floating point value between 0-1

        ### Returns:
        * `T`: any type representing the internal value of the event
        """
        raise NotImplementedError("This function needs to be overridden by "
                                  "child classes")

    def getFloatFromValue(self, value: T) -> float:
        """
        Convert an internal value into a floating point value between 0-1

        ### Args:
        * `value` (`T`): the type representing the internal value of the event

        ### Returns:
        * `float`: A floating point value between 0-1
        """
        raise NotImplementedError("This function needs to be overridden by "
                                  "child classes")
