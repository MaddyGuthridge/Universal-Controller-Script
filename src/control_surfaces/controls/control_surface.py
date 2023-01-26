"""
control_surfaces > controls > control_surface

Contains the ControlSurface class, which defines the abstract base type for
all control surfaces.

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""
# from __future__ import annotations

from fl_classes import FlMidiMsg
from time import time
from typing import Optional, final
from abc import abstractmethod
from common import getContext
from common.util.abstract_method_error import AbstractMethodError
from common.types import Color
from control_surfaces.event_patterns import NullPattern
from control_surfaces.value_strategies import NullStrategy
from ..event_patterns import IEventPattern
from ..value_strategies import IValueStrategy
from ..control_mapping import ControlEvent, ControlMapping
from ..managers import (
    IAnnotationManager,
    IColorManager,
    IValueManager,
    DummyAnnotationManager,
    DummyColorManager,
    DummyValueManager,
)


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
        raise AbstractMethodError()

    @staticmethod
    def isPress(value: float) -> bool:
        """
        Returns whether a value (0-1.0) for this control should count as a
        press.

        Control surface definitions override this method in order to provide
        double press functionality.

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
        event_pattern: Optional[IEventPattern] = None,
        value_strategy: Optional[IValueStrategy] = None,
        coordinate: tuple[int, int] = (0, 0),
        annotation_manager: Optional[IAnnotationManager] = None,
        color_manager: Optional[IColorManager] = None,
        value_manager: Optional[IValueManager] = None,
    ) -> None:
        """
        Create an ControlSurface

        ### Args:
        * `event_pattern`: an [event pattern](event_pattern.md) that can be
          used to recognize the event. If not provided, the control can never
          be matched.

        * `value_strategy`: a [value strategy](value_strategy.md) that can be
          used to determine a value from events. If not provided, the control
          won't get values.

        * `coordinate`: the coordinate of the control in the format
          `(row, column)`. Defaults to `(0, 0)`.

        * `annotation_manager`: a manager to provide functionality of sharing
          annotations with a device. This can be used to control text displays
          associated with a control, or to control a global LED text display.

        * `color_manager`: a manager to provide functionality of sharing colors
          with a device. This can be used to control LEDs on controls.

        * `value_manager`: a manager to provide functionality of sharing values
          with a device. This can be used to drive motorized controls.
        """
        if event_pattern is None:
            event_pattern = NullPattern()
        self.__pattern = event_pattern
        self.__color = Color()
        self.__prev_color = Color()
        self.__annotation = ""
        self.__prev_annotation = ""
        self.__value = 0.0
        self.__prev_value = 0.0
        if value_strategy is None:
            value_strategy = NullStrategy()
        self.__value_strategy = value_strategy
        self.__coord = coordinate

        # Attributes to make our pressed thing work better
        self.__needs_update = False
        self.__got_update = False

        # Managers for control
        if annotation_manager is not None:
            self.__annotation_manager = annotation_manager
        else:
            self.__annotation_manager = DummyAnnotationManager()
        if color_manager is not None:
            self.__color_manager = color_manager
        else:
            self.__color_manager = DummyColorManager()
        if value_manager is not None:
            self.__value_manager = value_manager
        else:
            self.__value_manager = DummyValueManager()

        # The time that this control was pressed last
        self.__last_press_time = 0.0
        # The time that this control was tweaked last
        self.__last_tweak_time = 0.0

    def __repr__(self) -> str:
        """
        String representation of the control surface
        """
        return \
            f"{self.__class__}, ({self.__coord}, {self.value})"

    @final
    def getPattern(self) -> IEventPattern:
        """
        Returns the event pattern used by this control surface

        This allows validation to be performed if using the control within a
        particular control matcher.

        ### Returns:
        * `IEventPattern`: pattern
        """
        return self.__pattern

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
    def match(self, event: FlMidiMsg) -> Optional[ControlEvent]:
        """
        Returns a control event if the given event matches this
        control surface, otherwise returns None

        ### Args:
        * `event` (`FlMidiMsg`): event to potentially match

        ### Returns:
        * `Optional[ControlEvent]`: control mapping, if the event maps
        """
        if self.__pattern.matchEvent(event):
            self.__value = self.__value_strategy.getValueFromEvent(
                event, self.__value)
            channel = self.__value_strategy.getChannelFromEvent(event)
            self.__needs_update = True
            self.__got_update = False
            t = time()
            self.__last_tweak_time = t
            if self.isPress(self.value):
                double_press = t - self.__last_press_time \
                    <= getContext().settings.get("controls.double_press_time")
                self.__last_press_time = t
            else:
                double_press = False
            return ControlEvent(event, self, self.value, channel, double_press)
        else:
            return None

    ###########################################################################
    # Properties

    @property
    def coordinate(self) -> tuple[int, int]:
        """
        Coordinate of the control (row, column). Read only.
        """
        return self.__coord

    @property
    def color(self) -> Color:
        """
        Represents the color of the control

        On compatible controllers, this can be displayed on the control using
        LED lighting.
        """
        return self.__color

    @color.setter
    def color(self, c: Color):
        self.__got_update = True
        if self.__color != c:
            self.__color = c

    @property
    def annotation(self) -> str:
        """
        Represents the annotation of the control

        On compatible controllers, this can be displayed as text near the
        control.
        """
        return self.__annotation

    @annotation.setter
    def annotation(self, a: str):
        if self.__annotation != a:
            self.__annotation = a

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
        return self.__value

    @value.setter
    def value(self, val: float) -> None:
        # Ensure value is within bounds
        if not (0 <= val <= 1):
            raise ValueError(
                "Value for control must be between 0 and 1"
            )
        if self.__value != val:
            self.__value = val
            self.__needs_update = True
            self.__got_update = False

    @property
    def value_midi(self) -> int:
        """
        The value of the control, represented as a MIDI value between `0` and
        `127`.
        """
        return round(self.value * 127)

    @value_midi.setter
    def value_midi(self, val: int) -> None:
        self.value = val / 127

    @property
    def value_rec(self) -> int:
        """
        The value of the control, represented as a REC event value between `0`
        and `2 ** 16`.
        """
        return round(self.value * (2 ** 16))

    @value_rec.setter
    def value_rec(self, val: int) -> None:
        self.value = val / (2 ** 16)

    @property
    def needs_update(self) -> bool:
        """
        Represents whether the value of the control has changed since the last
        time the color was set.
        """
        return self.__needs_update

    @property
    def got_update(self) -> bool:
        """
        Represents whether the value of the control has changed since the last
        time the color was set, and was since updated.
        """
        return self.__got_update

    @property
    def last_pressed(self) -> float:
        """
        Returns the last time that the control was pressed

        ### Returns:
        * `float`: unix time of last tweak
        """
        return self.__last_press_time

    @property
    def last_tweaked(self) -> float:
        """
        Returns the last time that the control was tweaked

        ### Returns:
        * `float`: unix time of last tweak
        """
        return self.__last_tweak_time

    @property
    def press_length(self) -> float:
        """
        How long the control has been pressed for, or 0 if the control isn't
        currently pressed.
        """
        if self.value:
            return time() - self.__last_press_time
        return 0.0

    ###########################################################################
    # Events

    @final
    def doTick(self, thorough: bool) -> None:
        """
        Called when a tick happens

        This function is used to call the main tick method which is overridden
        by child classes.

        ### Args:
        * thorough (`bool`): Whether a full tick should be done.
        """
        # If it's a thorough tick, force all the properties to update on the
        # device
        # Otherwise, only update them if they need it (ie the property changed)
        if thorough or self.__color != self.__prev_color:
            self.__color_manager.onColorChange(self.color)
        if thorough or self.__annotation != self.__prev_annotation:
            self.__annotation_manager.onAnnotationChange(self.annotation)
        if thorough or self.__value != self.__prev_value:
            self.__value_manager.onValueChange(self.value)
        self.tick()
        self.__color_manager.tick()
        self.__annotation_manager.tick()
        self.__value_manager.tick()
        if self.__got_update:
            self.__needs_update = False
            self.__got_update = False
        self.__prev_color = self.__color
        # Set color back to off, so that we don't have to worry about things
        # not getting updated correctly
        self.__color = Color()
        self.__prev_annotation = self.__annotation
        self.__prev_value = self.__value

    def tick(self) -> None:
        """
        Called when a tick happens

        This can be overridden to do anything necessary to keep the control
        functioning correctly.
        """
