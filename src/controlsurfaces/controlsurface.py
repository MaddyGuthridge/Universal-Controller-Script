"""
controlsurfaces > controlsurface

Contains the ControlSurface class, which defines the abstract base type for
all control surfaces

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]
"""
# from __future__ import annotations

from time import time
from typing import Optional, final
from abc import abstractmethod

from common import getContext
from .eventpattern import IEventPattern
from common.types import EventData, Color

from .valuestrategies import IValueStrategy

from .controlmapping import ControlEvent, ControlMapping


class ControlSurface:
    """
    Defines an abstract base class for a control surface.

    This class is extended by all other control surfaces.
    """

    @staticmethod
    @abstractmethod
    def getControlAssignmentPriorities() -> 'tuple[type[ControlSurface], ...]':
        """
        Returns a list of the control's assignment priorities

        These determine what controls are assigned to what parameters. If an
        assignment can't be made to this type, then it will be made to the next
        available type in the list, and so on...

        ### Returns:
        * `list[type]`: control assignment priorities
        """
        raise NotImplementedError("This function should be overridden in "
                                  "child classes")

    @staticmethod
    def isPress(value: float) -> bool:
        """
        Returns whether a value (0-1.0) for this control should count as a
        press.

        You must override this method in order to provide double press
        functionality.

        This is used to create the doublePress property for ControlEvent
        objects

        ### Args:
        * `value` (`float`): value to check

        ### Returns:
        * `bool`: whether this value should be counted as a press
        """
        return False

    def __init__(
        self,
        event_pattern: IEventPattern,
        value_strategy: IValueStrategy,
        coordinate: tuple[int, int] = (0, 0)
    ) -> None:
        """
        Create a ControlSurface

        ### Args:
        * `event_pattern` (`IEventPattern`): pattern to use when recognising
          the event
        * `value_strategy` (`IValueStrategy`): strategy for getting values from
          events
        * `group` (`str`): group that this control belongs to. Controls in
          different groups are never assigned together.
        * `coordinate` (`tuple[int, int]`, optional): coordinate of controls.
          Used if controls form a 2D grid (eg, drum pads). Defaults to (0, 0).
        """
        self._pattern = event_pattern
        self._color = Color()
        self._annotation = ""
        self._value = value_strategy.getValueFromFloat(0.0)
        self._value_strategy = value_strategy
        self._coord = coordinate
        self._needs_update = False
        self._got_update = False

        # The time that this control was pressed last
        self._press = 0.0
        # The time that this control was tweaked last
        self._tweak = 0.0

    def __repr__(self) -> str:
        """
        String representation of the control surface
        """
        return \
            f"{self.__class__}, ({self._coord}, {self.value})"

    @final
    def getMapping(self) -> ControlMapping:
        """
        Returns a mapping to this control, for the purpose of acting as a key
        to the control in a dictionary.

        Mappings are used to refer to a control without being able to easily
        modify its value.

        ### Returns:
        * `ControlMapping`: A mapping to this control
        """
        return ControlMapping(self)

    @final
    def match(self, event: EventData) -> Optional[ControlEvent]:
        """
        Returns a control event if the given event matches this
        control surface, otherwise returns None

        ### Args:
        * `event` (`eventData`): event to potentially match

        ### Returns:
        * `Optional[ControlEvent]`: control mapping, if the event maps
        """
        if self._pattern.matchEvent(event):
            self._value = self._value_strategy.getValueFromEvent(event)
            channel = self._value_strategy.getChannelFromEvent(event)
            self._needs_update = True
            self._got_update = False
            t = time()
            self._tweak = t
            if self.isPress(self.value):
                double_press = t - self._press \
                    <= getContext().settings.get("controls.double_press_time")
                self._press = t
            else:
                double_press = False
            return ControlEvent(self, self.value, channel, double_press)
        else:
            return None

    ###########################################################################
    # Properties

    @property
    def coordinate(self) -> tuple[int, int]:
        """
        Coordinate of the control. Read only.
        """
        return self._coord

    @property
    def color(self) -> Color:
        """
        Represents the color of the control

        On compatible controllers, this can be displayed on the control using
        LED lighting.
        """
        return self._color

    @color.setter
    def color(self, c: Color):
        self._got_update = True
        if self._color != c:
            self._color = c
            self.onColorChange(c)

    @property
    def annotation(self) -> str:
        """
        Represents the annotation of the control

        On compatible controllers, this can be displayed as text near the
        control.
        """
        return self._annotation

    @annotation.setter
    def annotation(self, a: str):
        if self._annotation != a:
            self._annotation = a
            self.onAnnotationChange(a)

    @property
    def value(self) -> float:
        """
        The value property represents the value of a control (eg the rotation
        of a knob, or the position of a fader).

        It is gotten and set using a float between 0-1.0, but could be
        represented in other ways inside the class. The way it is gotten and
        set is determined by the functions _getValue() and _setValue()
        respectively.
        """
        return self._value_strategy.getFloatFromValue(self._value)

    @value.setter
    def value(self, v: float) -> None:
        # Ensure value is within bounds
        if not (0 <= v <= 1):
            raise ValueError(
                "Value for control must be between 0 and 1"
            )
        val = self._value_strategy.getValueFromFloat(v)
        if self._value != val:
            self._value = val
            self._needs_update = True
            self._got_update = False
            self.onValueChange(self.value)

    @property
    def needs_update(self) -> bool:
        """
        Represents whether the value of the control has changed since the last
        time the color was set.
        """
        return self._needs_update

    @property
    def got_update(self) -> bool:
        """
        Represents whether the value of the control has changed since the last
        time the color was set, and was since updated.
        """
        return self._got_update

    @property
    def last_tweaked(self) -> float:
        """
        Returns the last time that the control was tweaked

        ### Returns:
        * `float`: unix time of last tweak
        """
        return self._tweak

    ###########################################################################
    # Events

    def onColorChange(self, new: Color) -> None:
        """
        Called when the color of the control changes

        This can be overridden to send a MIDI message to the controller if
        required, so that the color can be shown on compatible controls.

        ## Args:
        * `new` (`Color`): The new value
        """

    def onAnnotationChange(self, new: str) -> None:
        """
        Called when the annotation of the control changes

        This can be overridden to send a MIDI message to the controller if
        required, so that the annotation can be shown on compatible controls.

        ## Args:
        * `new` (`str`): The new value
        """

    def onValueChange(self, new: float) -> None:
        """
        Called when the value of the control changes

        This can be overridden to send a MIDI message to the controller if
        required, so that the value can be shown on compatible controls.

        ## Args:
        * `new` (`float`): The new value as a float between `0` and `1`
        """

    @final
    def doTick(self) -> None:
        """
        Called when a tick happens

        This function is used to call the main tick method which is overridden
        by child classes
        """
        self.tick()
        if self._got_update:
            self._needs_update = False
            self._got_update = False

    def tick(self) -> None:
        """
        Called when a tick happens

        This can be overridden to do anything necessary to keep the control
        functioning correctly
        """
