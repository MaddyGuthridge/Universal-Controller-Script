"""
common > extension_manager > devices

Contains the definition for the DeviceCollection class

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""
from typing import TYPE_CHECKING
from common.exceptions import DeviceRecognizeError, DeviceInitializeError
from common.util.events import eventToString
from fl_classes import FlMidiMsg


if TYPE_CHECKING:
    from devices import Device


class DeviceCollection:
    """Collection of devices registered to the script
    """
    def __init__(self) -> None:
        self.__devices: list[type['Device']] = []

    def register(self, device: type['Device']) -> None:
        """
        Register a standard plugin

        This should be called after defining the class object for a plugin, so
        that the class can be instantiated if the plugin is in use.

        ### Args:
        * `device` (`type[Device]`): device to register

        ### Example Usage
        ```py
        # Create a device
        class MyDevice(Device):
            ...
        # Register it
        ExtensionManager.devices.register(MyDevice)
        ```
        """
        self.__devices.append(device)

    def get(self, arg: 'FlMidiMsg | str') -> 'Device':
        """
        Returns a new instance of a device, given a universal device enquiry
        response or a device identifier (as a fallback)

        ### Args:
        * `arg` (``FlMidiMsg | str`): event to match with devices

        ### Raises:
        * `ValueError`: Device not recognized

        ### Returns:
        * `Device`: device object instance
        """
        # Device name
        if isinstance(arg, str):
            for device in self.__devices:
                if device.matchDeviceName(arg):
                    # If it matches the pattern, then we found the right device
                    # create an instance and return it
                    try:
                        return device.create(None)
                    except Exception as e:
                        raise DeviceInitializeError(
                            "Failed to initialise device") from e
            raise DeviceRecognizeError(
                f"Device not recognized, using device name {arg}")
        # Sysex event
        # elif isinstance(arg, FlMidiMsg):
        # Can't runtime type check for MIDI events
        else:
            for device in self.__devices:
                pattern = device.getUniversalEnquiryResponsePattern()
                if pattern is None:
                    pass
                elif pattern.matchEvent(arg):
                    # If it matches the pattern, then we found the right device
                    # create an instance and return it
                    try:
                        return device.create(arg)
                    except Exception as e:
                        raise DeviceInitializeError(
                            "Failed to initialise device") from e
            raise DeviceRecognizeError(
                f"Device not recognized, using response "
                f"pattern {eventToString(arg)}"
            )

    def getById(self, id: str) -> 'Device':
        """
        Returns a new instance of a device, given a device ID, which should
        match a return value of Device.getId()

        FIXME: This doesn't work since device IDs aren't statically determined

        ### Raises:
        * `ValueError`: Device not found

        ### Returns:
        * `Device`: matching device
        """
        for device in self.__devices:
            if id in device.getSupportedIds():
                try:
                    return device.create(id=id)
                except Exception as e:
                    raise DeviceInitializeError(
                        "Failed to initialise device") from e
        raise DeviceRecognizeError(f"Device with ID {id} not found")

    def all(self) -> list[type['Device']]:
        return list(self.__devices)

    def __len__(self) -> int:
        return len(self.__devices)

    def inspect(self, dev: type['Device']) -> str:
        """
        Returns info about a device

        ### Args:
        * `dev` (`type[Device]`): device to inspect

        ### Returns:
        * `str`: device info
        """
        if dev in self.__devices:
            return f"{dev} (registered)"
        else:
            return f"{dev} (not registered)"
