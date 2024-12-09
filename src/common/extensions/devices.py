"""
common > extensions > devices

Code responsible for registering and managing devices

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""
from typing import TYPE_CHECKING, Optional
from common.types.decorator import SymmetricDecorator
from common.util.events import bytes_to_string

if TYPE_CHECKING:
    from devices import Device


_devices: dict[bytes, type['Device']] = {}


def get_device_matching_id(device_id: bytes) -> Optional[type['Device']]:
    """
    Return a device definition that matches the given device ID

    Check is performed against the minimum number of bytes between the given
    device ID and the device IDs of registered device definitions

    ### Args:
    * `device_id` (`bytes`): device ID to match against

    ### Returns:
    * `Optional[type[Device]]`: device, if found
    """
    for check_id, device in _devices.items():
        for byte_a, byte_b in zip(device_id, check_id):
            if byte_a != byte_b:
                break
        else:
            # Reached the end of the loop without hitting `break`, therefore
            # this device matches
            return device

    # None of the devices matched
    return None


def register(device_id: bytes) -> SymmetricDecorator[type['Device']]:
    """
    Register a device definition to be associated with the given `device_id`

    This device definition will be used when a device is detected that matches
    the given `device_id`, meaning that when iterating over the given bytes,
    all bytes of the connected device's ID are equal.

    ### Usage

    ```py
    @devices.register(bytes([
        0xF0, 0x7E, 0x00, 0x06, 0x02, 0x00, 0x20, 0x29, 0x01, 0x01, 0x00, 0x00
    ]))
    class MyDevice(Device):
        ...
    ```

    ### Args
    * `device_id` (`bytes`): device ID to match against

    ### Returns
    * `Decorator[Device]`: _description_
    """
    def inner(device_definition: type['Device']) -> type['Device']:
        # Do the error checking inside `inner` so we can give a nicer error
        # message, and to make sure people don't abuse decorators to register
        # multiple devices with one outer `register` call
        if (found_dev := get_device_matching_id(device_id)) is not None:
            device_id_str = bytes_to_string(device_id)
            raise ValueError(
                f"A device matching device_id {device_id_str} has already "
                f"been registered.\n\n"
                f"Attempted to register: {device_definition}\n"
                f"Previously registered device: {found_dev}"
            )

        _devices[device_id] = device_definition
        return device_definition

    return inner


def get_registered_devices() -> dict[bytes, type['Device']]:
    """
    Returns a dictionary mapping registered device IDs to the corresponding
    device definitions

    Will be used by the meta code generator to create a script file for all
    supported devices

    ### Returns:
    * `dict[bytes, Device]`: device definition mapping
    """
    return _devices
