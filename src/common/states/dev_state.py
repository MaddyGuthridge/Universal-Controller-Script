"""
common > states > dev_state

Contains the abstract DeviceState base class, for script states that require
a device to be detected in order to run properly.

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""
from abc import abstractmethod
from . import IScriptState
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from devices import Device


class DeviceState(IScriptState):
    """
    Abstract state that requires a device to be detected
    """

    @classmethod
    @abstractmethod
    def create(cls, device: 'Device') -> 'DeviceState':
        """
        Create an instance of a DeviceState

        ### Args:
        * `device` (`Device`): device used by this state

        ### Returns:
        * `DeviceState`: new instance
        """
        raise NotImplementedError("This method should be implemented by "
                                  "child classes")
