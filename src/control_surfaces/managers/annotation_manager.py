"""
control_surfaces > managers > annotation_manager

Contains the IAnnotationManager interface, which is implemented by devices to
describe how a control surface should manage displaying its annotation on the
physical control.

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""
from abc import abstractmethod
from common.util.abstract_method_error import AbstractMethodError


class IAnnotationManager:
    """
    An interface for classes used to describe how a control surface should
    display its annotation property on the physical control.
    """
    @abstractmethod
    def onAnnotationChange(self, new_annotation: str) -> None:
        """
        Called when the annotation of a control surface changes, so the manager
        can send any required MIDI events to update the physical hardware.

        ### Args:
        * `new_annotation` (`str`): new annotation to set
        """
        raise AbstractMethodError(self)

    @abstractmethod
    def tick(self) -> None:
        """
        Called frequently to allow the annotation manager to update as required
        """
        raise AbstractMethodError(self)


class DummyAnnotationManager(IAnnotationManager):
    """
    An annotation manager that doesn't display annotations on the controller
    """
    def onAnnotationChange(self, new_annotation: str) -> None:
        pass

    def tick(self) -> None:
        pass
