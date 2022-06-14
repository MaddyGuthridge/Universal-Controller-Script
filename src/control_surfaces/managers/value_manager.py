"""
control_surfaces > managers > value_manager

Contains the IValueManager interface, which is implemented by devices to
describe how a control surface should manage showing its value on the
physical control.

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""
from abc import abstractmethod
from common.util.abstract_method_error import AbstractMethodError


class IValueManager:
    """
    An interface for classes used to describe how a control surface should
    show its value property on the physical control.
    """
    @abstractmethod
    def onValueChange(self, new_value: float) -> None:
        """
        Called when the value of a control surface changes, so the manager
        can send any required MIDI events to update the physical hardware.

        ### Args:
        * `new_value` (`float`): new value to set
        """
        raise AbstractMethodError(self)

    @abstractmethod
    def tick(self) -> None:
        """
        Called frequently to allow the value manager to update as required
        """
        raise AbstractMethodError(self)


class DummyValueManager(IValueManager):
    """
    A value manager that doesn't display values on the controller
    """
    def onValueChange(self, new_value: float) -> None:
        pass

    def tick(self) -> None:
        pass
