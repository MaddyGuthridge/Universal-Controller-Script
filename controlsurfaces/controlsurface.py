"""
controlsurfaces > controlsurface

Contains the ControlSurface class, which defines the abstract base type for
all control surfaces

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]
"""
# from __future__ import annotations

from typing import Optional

from common import IEventPattern
from common.types import eventData, Color

from .valuestrategies import IValueStrategy

from .controlshadow import ControlShadow
from .controlmapping import ControlMapping

class ControlSurface:
    """
    Defines an abstract base class for a control surface.

    This class is extended by all other control surfaces.
    """
    
    @staticmethod
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
    
    def __init__(
        self,
        event_pattern: IEventPattern,
        value_strategy: IValueStrategy,
        group: str,
        coordinate:tuple[int, int]=(0, 0)
    ) -> None:
        """
        Create a ControlSurface

        ### Args:
        * `event_pattern` (`IEventPattern`): pattern to use when recognising the
          event
        * `value_strategy` (`IValueStrategy`): strategy for getting values from
          events
        * `group` (`str`): group that this control belongs to. Controls in
          different groups are never assigned together.
        * `coordinate` (`tuple[int, int]`, optional): coordinate of controls.
          Used if controls form a 2D grid (eg, drum pads). Defaults to (0, 0).
        """
        self._pattern =  event_pattern
        self.__color = Color()
        self.__annotation = ""
        self.__value = None
        self.__value_strategy = value_strategy
        self.__group = group
        self.__coord = coordinate
        
    def getMapping(self) -> ControlMapping:
        """
        Returns a mapping to this control

        Mappings are used to refer to a control without being able to easily
        modify its value.

        ### Returns:
        * `ControlMapping`: A mapping to this control
        """
        return ControlMapping(self)

    def match(self, event: eventData) -> Optional[ControlMapping]:
        """
        Returns a control mapping of this control if the given event matches this 
        control surface, otherwise returns None

        ### Args:
        * `event` (`eventData`): event to potentially match

        ### Returns:
        * `Optional[ControlMapping]`: control mapping, if the event maps
        """
        if self._pattern.matchEvent(event):
            self.__value = self.__value_strategy.getValueFromEvent(event)
            return self.getMapping()
        else:
            return None

    ############################################################################
    # Properties
    
    @property
    def coordinate(self) -> tuple[int, int]:
        """
        Coordinate of the control. Read only.
        """
        return self.__coord
    
    @property
    def group(self) -> str:
        """
        The group that this control is a member of.
        """
        return self.__group

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
        prev = self.__color
        self.__color = c
        if prev != c:
            self.onColorChange()

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
        prev = self.__annotation
        self.__annotation = a
        if prev != a:
            self.onAnnotationChange()
    
    @property
    def value(self) -> float:
        """
        The value property represents the value of a control (eg the rotation
        of a knob, or the position of a fader). 
        
        It is gotten and set using a float between 0-1.0, but could be
        represented in other ways inside the class. The way it is gotten and set
        is determined by the functions _getValue() and _setValue() respectively.
        """
        return self.__value_strategy.getFloatFromValue(self.__value)
    @value.setter
    def value(self, newValue: float) -> None:
        # Ensure value is within bounds
        if not (0 < newValue < 1):
            raise ValueError(f"Value for control must be between "
                             f"0 and 1")
        self.__value = self.__value_strategy.getValueFromFloat(newValue)

    ############################################################################
    # Events
    
    def onColorChange(self) -> None:
        """
        Called when the color of the control changes

        This can be overridden to send a MIDI message to the controller if
        required, so that the color can be shown on compatible controls.
        """
    
    def onAnnotationChange(self) -> None:
        """
        Called when the annotation of the control changes

        This can be overridden to send a MIDI message to the controller if
        required, so that the annotation can be shown on compatible controls.
        """
    
    def onValueChange(self) -> None:
        """
        Called when the value of the control changes

        This can be overridden to send a MIDI message to the controller if
        required, so that the value can be shown on compatible controls.
        """

    def tick(self) -> None:
        """
        Called when a tick happens

        This can be overridden to do anything necessary to keep the control
        functioning correctly
        """
