"""
control_surfaces > control_mapping

Defines a mapping to a control surface.

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""

# from __future__ import annotations

from abc import abstractmethod
from fl_classes import FlMidiMsg
from typing import TYPE_CHECKING
from time import time

if TYPE_CHECKING:
    from . import ControlSurface
    from . import ControlShadow


class IControlHash:
    """
    Interface for values where their hashes map to a ControlSurface or
    ControlShadow
    """

    @abstractmethod
    def __hash__(self) -> int:
        raise NotImplementedError("This method should be implemented by child "
                                  "classes")

    @abstractmethod
    def __eq__(self, __o: object) -> bool:
        raise NotImplementedError("This method should be implemented by child "
                                  "classes")

    @abstractmethod
    def getControl(self) -> 'ControlSurface':
        raise NotImplementedError("This method should be implemented by child "
                                  "classes")


class ControlMapping(IControlHash):
    """
    Defines a mapping to a control surface, which has the property that
    different instances of a mapping to the same control have the same hash.
    """

    def __init__(
        self,
        map_to: 'ControlSurface'
    ) -> None:
        self._map_to = map_to

    def __hash__(self) -> int:
        return hash(self._map_to)

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, ControlEvent):
            return self._map_to == __o._map_to
        else:
            return NotImplemented

    def getControl(self) -> 'ControlSurface':
        return self._map_to


class ControlEvent(IControlHash):
    """
    Represents an event outside the context of plugins (maps to a control
    surface). Contains info on the channel and value of the event that was
    fired.
    """

    def __init__(
        self,
        midi: FlMidiMsg,
        map_to: 'ControlSurface',
        value: float,
        channel: int,
        double: bool,
    ) -> None:
        self._midi = midi
        self._map_to = map_to
        self._value = value
        self._channel = channel
        self._double = double
        self._press_length = (
            0.0
            if map_to.isPress(value)
            else time() - map_to.last_pressed
        )

    def __repr__(self) -> str:
        return f"ControlEvent({self._map_to}, {self._value})"

    def __hash__(self) -> int:
        return hash(self._map_to)

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, ControlEvent):
            return self._map_to == __o._map_to
        else:
            return NotImplemented

    def getControl(self) -> 'ControlSurface':
        return self._map_to

    @property
    def midi(self) -> FlMidiMsg:
        """MIDI message associated with the event, which can be used to modify
        the original event if required.
        """
        return self._midi

    @property
    def value(self) -> float:
        """Value of this event, between `0-1.0`
        """
        return self._value

    @property
    def value_midi(self) -> int:
        """
        The value associated with the event, represented as a MIDI value
        between `0` and `127`.
        """
        return round(self.value * 127)

    @property
    def value_rec(self) -> int:
        """
        The value associated with the event, represented as a REC event value
        between `0` and `2 ** 16`.
        """
        return round(self.value * (2 ** 16))

    @property
    def channel(self) -> int:
        """Channel that this event was fired from.
        `-1` if not an event, or not associated with a channel
        """
        return self._channel

    @property
    def double(self) -> bool:
        """Whether this event is a double press or not
        """
        return self._double

    @property
    def coordinate(self) -> tuple[int, int]:
        """Coordinate of the control (row, column)
        """
        return self._map_to.coordinate

    @property
    def press_length(self) -> float:
        """
        How long the control was pressed for, or 0 if the control isn't
        currently pressed.
        """
        return self._press_length


class ControlShadowEvent(IControlHash):
    """
    Defines a mapping to a control shadow, where hashes are shared with
    ControlMapping objects.

    Used to represent a single event within the context of plugins, allowing
    for info about this event to be managed.
    """

    def __init__(
        self,
        map_from: ControlEvent,
        map_to: 'ControlShadow',
    ) -> None:
        self._map_from = map_from
        self._map_to = map_to

    def __repr__(self) -> str:
        return f"ControlShadowEvent({self._map_to})"

    def __hash__(self) -> int:
        return hash(self._map_from)

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, ControlEvent):
            return self._map_to == __o._map_to
        else:
            return NotImplemented

    def getControl(self) -> 'ControlSurface':
        return self._map_to.getControl()

    def getShadow(self) -> 'ControlShadow':
        return self._map_to

    @property
    def midi(self) -> FlMidiMsg:
        """
        MIDI message associated with the event, which can be used to modify
        the original event if required.
        """
        return self._map_from.midi

    @property
    def channel(self) -> int:
        """
        Channel that this event was sent from.
        `-1` if not an event, or not associated with a channel
        """
        return self._map_from.channel

    @property
    def value(self) -> float:
        """
        The value associated with this event, between `0-1.0`
        """
        return self._map_from.value

    @property
    def value_midi(self) -> int:
        """
        The value associated with the event, represented as a MIDI value
        between `0` and `127`.
        """
        return round(self.value * 127)

    @property
    def value_rec(self) -> int:
        """
        The value associated with the event, represented as a REC event value
        between `0` and `2 ** 30`.
        """
        return round(self.value * (2 ** 30))

    @property
    def double(self) -> bool:
        """Whether this event is a double press or not
        """
        return self._map_from.double

    @property
    def coordinate(self) -> tuple[int, int]:
        """Coordinate of the control (row, column)
        """
        return self._map_to.coordinate

    @property
    def press_length(self) -> float:
        """
        How long the control was pressed for, or 0 if the control isn't
        currently pressed.
        """
        return self._map_from.press_length
