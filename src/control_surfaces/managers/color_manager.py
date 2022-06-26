"""
control_surfaces > managers > color_manager

Contains the IColorManager interface, which is implemented by devices to
describe how a control surface should manage displaying its color on the
physical control.

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""
from abc import abstractmethod
from common.types import Color
from common.util.abstract_method_error import AbstractMethodError


class IColorManager:
    """
    An interface for classes used to describe how a control surface should
    display its color property on the physical control.
    """
    @abstractmethod
    def onColorChange(self, new_color: Color) -> None:
        """
        Called when the color of a control surface changes, so the manager can
        send any required MIDI events to update the physical hardware.

        ### Args:
        * `new_color` (`Color`): new color to set
        """
        raise AbstractMethodError(self)

    @abstractmethod
    def tick(self) -> None:
        """
        Called frequently to allow the color manager to update as required
        """
        raise AbstractMethodError(self)


class DummyColorManager(IColorManager):
    """
    A color manager that doesn't display colors on the controller
    """
    def onColorChange(self, new_color: Color) -> None:
        pass

    def tick(self) -> None:
        pass
