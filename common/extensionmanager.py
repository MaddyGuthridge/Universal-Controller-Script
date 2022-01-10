
from __future__ import annotations
from typing import TYPE_CHECKING, overload

from common.types.eventdata import eventData

if TYPE_CHECKING:
    from devices import Device

class ExtensionManager:
    """
    Manages all extensions registered with the script, allowing for extensions
    to be used for plugins or devices as required.
    """
    
    _plugins: dict[str, type] = dict()
    _devices: list[type[Device]] = []
    
    def __init__(self) -> None:
        raise TypeError("ExtensionManager is a static class and cannot be instantiated.")

    @classmethod
    def registerPlugin(cls, plugin) -> None:
        pass

    @classmethod
    def registerDevice(cls, device: type[Device]) -> None:
        """
        Register a device type

        This should be called after defining the class object for a device, so
        that the class can be instantiated if the device is recognised.

        ### Args:
        * `device` (`type`, extends `device`): class to register
        
        ### Example Usage
        ```py
        # Create a device
        class MyDevice(Device):
            ...
        # Register it
        ExtensionManager.registerDevice(MyDevice)
        ```
        """
        cls._devices.append(device)

    @overload
    @classmethod
    def getDevice(cls, arg: eventData) -> Device:
        """
        Returns a new instance of a device, given a universal device enquiry
        response.

        ### Args:
        * `arg` (`str`): event to match with devices

        ### Raises:
        * `ValueError`: Device not recognised

        ### Returns:
        * `Device`: device object instance
        """
    @overload
    @classmethod
    def getDevice(cls, arg: str) -> Device:
        """
        Returns a new instance of a device, given a deviceID.

        This function should be called as a fallback when using a universal
        device enquiry fails

        ### Args:
        * `arg` (`str`): device ID

        ### Raises:
        * `ValueError`: Device not recognised

        ### Returns:
        * `Device`: device object instance
        """
    @classmethod
    def getDevice(cls, arg: eventData | str) -> Device:
        # Sysex event
        if isinstance(arg, eventData):
            for device in cls._devices:
                pattern = device.getUniversalEnquiryResponsePattern()
                if pattern is None:
                    continue
                if pattern.matchEvent(arg):
                    # If it matches the pattern, then we found the right device
                    # create an instance and return it
                    return device.create(arg)
        # Device ID
        elif isinstance(arg, str):
            for device in cls._devices:
                if device.matchDeviceId(arg):
                    # If it matches the pattern, then we found the right device
                    # create an instance and return it
                    return device.create(None)
        raise ValueError("Device not recognised")
