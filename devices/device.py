"""
devices > device

Contains the Device class, used to represent a MIDI controller device within
the script.

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]
"""
# from __future__ import annotations

from typing import Optional, final
from common import IEventPattern
from common import ProfilerContext
from common.types import EventData
from controlsurfaces import ControlShadow

from controlsurfaces import ControlEvent
from devices import IControlMatcher
from abc import abstractmethod

class Device:
    """
    Base class for device types.

    All device objects should inherit from this definition and implement its
    functions.
    """
    def __init__(self, control_matcher: IControlMatcher) -> None:
        """
        Create a device object.

        This __init__ call should be conducted by a subclass, providing the
        control matcher to the parent class so that events can be matched
        correctly.

        ### Args:
        * `control_matcher` (`IControlMatcher`): Control matching strategy.
        """
        self._matcher = control_matcher

    @classmethod
    @abstractmethod
    def create(cls, event: Optional[EventData]) -> 'Device':
        """
        Create an instance of this device

        This method is called when a device is recognised and should return an
        instance of that particular device.

        ### Args:
        * `event` (`eventData`, optional): event used to recognise device, or
          None if not applicable (eg when using deviceId)

        ### Returns:
        * `Device`: instance of device object
        """
        raise NotImplementedError("This method must be overridden by child "
                                  "classes")

    @staticmethod
    @abstractmethod
    def getId() -> str:
        """
        Returns the id of the device, in the form:

        "Manufacturer.Model.Mark.Variant"

        ### Returns:
        * `str`: device id
        """
        raise NotImplementedError("This method must be overridden by child "
                                  "classes")

    @abstractmethod
    def getDeviceNumber(self) -> int:
        """
        Returns the number of a device

        This is used by devices to help with forwarding events to the main
        script

        ### Returns:
        * `int`: device number
              * `1`: Main device
              * other values: other device numbers.
        """
        raise NotImplementedError("This method must be overridden by child "
                                  "classes")

    @staticmethod
    @abstractmethod
    def getUniversalEnquiryResponsePattern() -> Optional[IEventPattern]:
        """
        Returns the event pattern from which a device can be recognised so that
        its representation can be loaded, or None, if this device can't be
        matched using this pattern.

        ### Returns:
        * `IEventPattern`: pattern to match universal device enquiry, or None if
          can't be matched.
        """
        raise NotImplementedError("This method must be overridden by child "
                                  "classes")

    @staticmethod
    @abstractmethod
    def matchDeviceName(name: str) -> bool:
        """
        Returns whether this device matches the name given, where the name is
        the return value of `device.getName()`.

        This is used as a fallback for  matching the device if no universal
        device enquiry response is given.

        ### Args:
        * `name` (`str`): name of the device

        ### Returns:
        * `bool`: whether there was a match
        """
        raise NotImplementedError("This method must be overridden by child "
                                  "classes")

    @staticmethod
    @abstractmethod
    def getDrumPadSize() -> tuple[int, int]:
        """
        Returns the size of the grid of drum pads used by the controller

        By default this returns 0x0, but it should be overridden by device
        objects if the device has drum pads

        ### Returns:
        * `tuple[int, int]`: rows, cols
        """
        return 0, 0

    def initialise(self) -> None:
        """
        Called when the device is first recognised, and when FL Studio allows
        communication.

        Can be overridden by child classes.
        """

    # def deinitialise(self) -> None:
    #     """
    #     Called when FL Studio is going to start blocking communication, such as
    #     when a render is going to begin, or when exiting.
    #
    #     Can be overridden by child classes.
    #     """

    def tick(self) -> None:
        """
        Called frequently, so that the device can perform any required actions,
        such as maintaining a heartbeat event.

        Can be overridden by child classes.

        WARNING: Ensure that the super function is still called or control
        surfaces won't get ticked correctly
        """
        for c in self._matcher.getControls():
            # with ProfilerContext("Tick control"):
                c.tick()

    @final
    def matchEvent(self, event: EventData) -> Optional[ControlEvent]:
        """
        Match an event from the device, so that the script can operate on it.

        This shouldn't be overridden by child classes.

        ### Returns:
        * `MatchedEvent`: event data
        """
        return self._matcher.matchEvent(event)

    @final
    def getControlShadows(self, group:str=None) -> list[ControlShadow]:
        """
        Returns a list of new control shadows representing all the controls
        available on the device.

        This shouldn't be overridden by child classes.

        ### Returns:
        * `list[ControlSurface]`: Control shadows
        """
        return [ControlShadow(c) for c in self._matcher.getControls(group)]

    @final
    def getGroups(self) -> set[str]:
        """
        Returns a set of groups that controls are placed into.

        Refer to the documentation for the group property in the ControlSurface
        type.

        This shouldn't be overridden by child classes.

        ### Returns:
        * `set[str]`: Set of groups
        """
        return self._matcher.getGroups()
