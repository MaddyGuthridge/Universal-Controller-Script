"""
devices > device

Contains the Device class, used to represent a MIDI controller device within
the script.

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""
# from __future__ import annotations

from typing import Optional, final
from common.profiler import profilerDecoration, ProfilerContext
from common.util.abstract_method_error import AbstractMethodError
from control_surfaces.event_patterns import IEventPattern
from fl_classes import FlMidiMsg
from control_surfaces import ControlShadow

from control_surfaces import ControlEvent
from control_surfaces.matchers import IControlMatcher
from abc import abstractmethod


class Device:
    """
    Base class for device types.

    All device objects should inherit from this definition and implement its
    functions.

    ## Methods to implement:
    For full documentation, refer to the docstrings for each function.

    ### Class methods

    * `create(cls, event: Optional[FlMidiMsg]) -> Device`: create an instance
      of this device

    ### Static methods

    * `getUniversalEnquiryResponsePattern() -> Optional[IEventPattern]`:
      Get the event pattern for a universal device enquiry response

    * `matchDeviceName(name: str) -> bool`: Return whether this device matches
      the given name of a device (used as a fallback method for device
      matching)

    * `getDrumPadSize() -> tuple[int, int]`: Return the number of rows and
      columns in the drum pad grid.

    ### Instance methods

    * `getId(self) -> str`: Return the device ID

    * `getDeviceNumber(self) -> int`: Return the device number

    ## Optional methods

    * `initialize(self)`: Called when we initialize the device

    * `deinitialize(self)`: Called when we deinitialize the device

    * `tick(self)`: Called frequently to allow for
      devices to perform any required actions.
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
    def create(
        cls,
        event: Optional[FlMidiMsg] = None,
        id: Optional[str] = None,
    ) -> 'Device':
        """
        Create an instance of this device

        This method is called when a device is recognized and should return an
        instance of that particular device.

        ### Args:
        * `event` (`FlMidiMsg`, optional): event used to recognize device, or
          None if not applicable (eg when using deviceId). Defaults to None.

        * `id` (`str`, optional): ID used to map to the device.

        ### Returns:
        * `Device`: instance of device object
        """
        raise AbstractMethodError(cls)

    @classmethod
    @abstractmethod
    def getSupportedIds(cls) -> tuple[str, ...]:
        """
        Returns the IDs of all devices that can be handled by this device
        definition

        ### Returns:
        * `tuple[str]`: all supported device IDs
        """
        raise AbstractMethodError(cls)

    @abstractmethod
    def getId(self) -> str:
        """
        Returns the id of the recognized device, in the form:

        "Manufacturer.Model.Mark.Variant"

        ### Returns:
        * `str`: device id
        """
        raise AbstractMethodError(self)

    def getDeviceNumber(self) -> int:
        """
        Returns the number of a device

        This is used by devices to help with forwarding events to the main
        script.

        By default this returns 1.

        ### Returns:
        * `int`: device number
              * `1`: Main device
              * other values: other device numbers.
        """
        return 1

    @classmethod
    def getUniversalEnquiryResponsePattern(cls) -> Optional[IEventPattern]:
        """
        Returns the event pattern from which a device can be recognized so that
        its representation can be loaded, or None, if this device can't be
        matched using this pattern.

        By default this returns None

        ### Returns:
        * `IEventPattern`: pattern to match universal device enquiry, or None
          if can't be matched.
        """
        return None

    @classmethod
    def matchDeviceName(cls, name: str) -> bool:
        """
        Returns whether this device matches the name given, where the name is
        the return value of `device.getName()`.

        This is used as a fallback for  matching the device if no universal
        device enquiry response is given.

        By default, this won't match anything

        ### Args:
        * `name` (`str`): name of the device

        ### Returns:
        * `bool`: whether there was a match
        """
        return False

    @classmethod
    def getDrumPadSize(cls) -> tuple[int, int]:
        """
        Returns the size of the grid of drum pads used by the controller

        By default this returns 0x0, but it should be overridden by device
        objects if the device has drum pads

        ### Returns:
        * `tuple[int, int]`: rows, cols
        """
        return 0, 0

    def initialize(self) -> None:
        """
        Called when the device is first recognized, and when FL Studio allows
        communication.

        Can be overridden by child classes.
        """

    def deinitialize(self) -> None:
        """
        Called when FL Studio is going to start blocking communication, such
        as when a render is going to begin, or when exiting.

        Can be overridden by child classes.
        """

    @final
    @profilerDecoration("device")
    def doTick(self) -> None:
        """
        Called frequently, so that the device can perform any required actions,
        such as maintaining a heartbeat event.

        This method forwards ticks onto other parts of the controller as well
        as to its own tick() method which is overridden by child classes
        """
        with ProfilerContext("object"):
            self.tick()
        with ProfilerContext("matcher"):
            self._matcher.tick(False)

    def tick(self) -> None:
        """
        Called frequently, so that the device can perform any required actions,
        such as maintaining a heartbeat event.

        Can be overridden by child classes.
        """

    @final
    def matchEvent(self, event: FlMidiMsg) -> Optional[ControlEvent]:
        """
        Match an event from the device, so that the script can operate on it.

        This shouldn't be overridden by child classes.

        ### Returns:
        * `MatchedEvent`: event data
        """
        return self._matcher.matchEvent(event)

    @final
    def getControlShadows(self) -> list[ControlShadow]:
        """
        Returns a list of new control shadows representing all the controls
        available on the device.

        This shouldn't be overridden by child classes.

        ### Returns:
        * `list[ControlSurface]`: Control shadows
        """
        return [ControlShadow(c) for c in self._matcher.getControls()]
