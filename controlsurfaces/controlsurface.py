"""
controlsurfaces > controlsurface

Contains the ControlSurface class, which defines the abstract base type for
all control surfaces

Authors:
* Miguel Guthridge [hdsq@outlook.com.au]
"""

from typing import Optional

from common import IEventPattern, MatchedEvent
from common.types import eventData, Color

class ControlSurface:
    """
    Defines an abstract base class for a control surface.

    This class is extended by all other control surfaces.
    """
    
    @staticmethod
    def getControlAssignmentPriorities() -> list[str]:
        """
        Returns a list of the control's assignment priorities

        These determine what controls are assigned to what parameters

        ### Returns:
        * `list[str]`: control assignment priorities
        """
        raise NotImplementedError("This function should be overridden in "
                                  "child classes")
    
    def __init__(self, event_pattern: IEventPattern, name: str) -> None:
        """
        Create a ControlSurface

        ### Args:
        * `event_pattern` (`IEventPattern`): pattern to use when recognising the
        event
        """
        self._pattern =  event_pattern
        self.__color = Color()
        self.__annotation = ""
        self.__value = 0
        self.__name = name

    def match(self, event: eventData) -> Optional[MatchedEvent]:
        """
        Returns a MatchedEvent if the given event matches this control surface,
        otherwise returns None

        ### Args:
        * `event` (`eventData`): event to potentially match

        ### Returns:
        * `Optional[MatchedEvent]`: match design
        """
        if self._pattern.matchEvent(event):
            
            return MatchedEvent(self, self.value)
        else:
            return None

    def setValueFromEvent(self, event: eventData) -> None:
        """
        Sets the value of an event as a float between (0.0 - 1.0) from an event

        ### Args:
        * `event` (`eventData`): event to set value from
        """
        raise NotImplementedError("This function should be overridden by a "
                                  "child class")

    ############################################################################
    # Properties

    @property
    def name(self) -> str:
        """
        The name of the control. Read only.
        """
        return self.__name

    @property
    def color(self) -> Color:
        return self.__color
    @color.setter
    def color(self, c: Color):
        self.__color = c

    @property
    def annotation(self) -> str:
        return self.__annotation
    @annotation.setter
    def annotation(self, a: str):
        self.__annotation = a

    def _getValue(self) -> float:
        """
        Getter for control surface's value. Can be overridden by an event to
        manage the value differently if necessary

        This should return a floating point value between 0-1.0
        
        NOTE: This function shouldn't be called manually, but should be accessed
        through the property

        ### Returns:
        * `float`: Value
        """
        return self.__value
    
    def _setValue(self, newValue: float) -> None:
        """
        Setter for control surface's value. Can be overridden by an event to
        manage the value differently if necessary

        This should accept a floating point value between 0-1.0
        
        NOTE: This function shouldn't be called manually, but should be accessed
        through the property

        ### Args:
        * `newValue` (`float`): Value
        """
        self.__value = newValue
    
    @property
    def value(self) -> float:
        """
        The value property represents the value of a control (eg the rotation
        of a knob, or the position of a fader). 
        
        It is gotten and set using a float between 0-1.0, but could be
        represented in other ways inside the class. The way it is gotten and set
        is determined by the functions _getValue() and _setValue() respectively.
        """
        return self._getValue()
    @value.setter
    def value(self, newValue: float) -> None:
        # Ensure value is within bounds
        if not (0 < newValue < 1):
            raise ValueError(f"Value for control {self.name} must be between "
                             f"0 and 1")
        self._setValue(newValue)

    ############################################################################
    # Events
    
    def onColorChange(self) -> None:
        """
        Called when the color of the control changes

        This can be overridden to send a MIDI message to the controller if
        required
        """
    
    def onAnnotationChange(self) -> None:
        """
        Called when the annotation of the control changes

        This can be overridden to send a MIDI message to the controller if
        required
        """

    def tick(self) -> None:
        """
        Called when a tick happens

        This can be overridden to do anything necessary to keep the control
        functioning correctly
        """
