"""
controlsurfaces > controlshadow

Represents a "shadow" control surface, which can be modified as necessary
without affecting the original control, unless it is specifically applied

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]
"""

from typing import TYPE_CHECKING, Iterator, overload
from typing_extensions import TypeGuard
from common.types import Color
from .control_mapping import ControlMapping

if TYPE_CHECKING:
    from . import ControlSurface


class IControlShadow:
    """
    A class that acts as a "shadow" to a physical control surface. This allows
    plugins to control properties of a control surface, with those changes
    only being applied if required.

    This abstract base class provides the abstract properties used by the main
    class, but is separate so that a NullControlShadow can be defined, which
    simplifies performing quick assignments of control properties.
    """
    def isBound(self) -> TypeGuard['ControlShadow']:
        """
        Return whether this control shadow is bound to an actual control

        This should be used to check that a control is valid before performing
        complex operations on it.
        """
        return isinstance(self, ControlShadow)

    @property
    def value(self) -> float:
        """
        Represents the value that will be applied to the control after
        the event has been processed, as a float between 0-1
        """
    @value.setter
    def value(self, newVal: float) -> None:
        ...

    @property
    def color(self) -> Color:
        """
        Represents the color that will be applied to the control after the
        event has been processed.
        """
    @color.setter
    def color(self, newColor: Color) -> None:
        ...

    @property
    def annotation(self) -> str:
        """
        Represents the annotation that will be applied to the control after the
        event has been processed.
        """
    @annotation.setter
    def annotation(self, newAnnotation: str) -> None:
        ...


class ControlShadow(IControlShadow):
    """
    A class that acts as a "shadow" to a physical control surface. This allows
    plugins to control properties of a control surface, with those changes
    only being applied if required.

    This is the class representing a real control.
    """

    def __init__(self, control: 'ControlSurface') -> None:
        """
        Create an event object

        This should be called when recognizing an event

        ### Args:
        * `control` (`ControlSurface`): control associated with this event
        """
        self._control = control
        self._value = 0.0
        self._color = Color()
        self._annotation = ""
        self._changed = False

    def __repr__(self) -> str:
        return f"Shadow of {self._control}"

    def getControl(self):
        """
        Get a reference to the control surface associated with the event

        ### Returns:
        * `ControlSurface`: control surface
        """
        return self._control

    def getMapping(self) -> ControlMapping:
        """
        Returns a ControlMapping to the control that this object shadows
        """
        return self._control.getMapping()

    @property
    def value(self) -> float:
        """
        Represents the value that will be applied to the control after
        the event has been processed, as a float between 0-1
        """
        return self._value

    @value.setter
    def value(self, newVal: float) -> None:
        if self._value != newVal:
            if not (0 <= newVal <= 1):
                raise ValueError(
                    f"Value must be within range 0-1 ({newVal}) @ "
                    f"{self}"
                )
            self._value = newVal
            self._changed = True

    @property
    def color(self) -> Color:
        """
        Represents the color that will be applied to the control after the
        event has been processed.
        """
        return self._color

    @color.setter
    def color(self, newColor: Color) -> None:
        if self._color != newColor:
            self._color = newColor
            self._changed = True

    @property
    def annotation(self) -> str:
        """
        Represents the annotation that will be applied to the control after the
        event has been processed.
        """
        return self._annotation

    @annotation.setter
    def annotation(self, newAnnotation: str) -> None:
        if self._annotation != newAnnotation:
            self._annotation = newAnnotation
            self._changed = True

    @property
    def coordinate(self) -> tuple[int, int]:
        """
        The coordinate of the control
        """
        return self._control.coordinate

    def colorize(self, newColor: Color) -> 'ControlShadow':
        """
        Add a color to this control shadow

        This function differs from the color property, as it can be used in a
        "pipeline" fashion to apply multiple properties to a control quickly
        and easily.

        ### Args:
        * `newColor` (`Color`): new color to assign

        ### Returns:
        * `Self`: the same control, so that the pipeline can be continued

        ### Example usage

        This is best used when binding controls to quickly apply properties to
        the control.

        ```py
        # Bind to a play button, set its color to black, and label it "control"
        shadow.bindControl(PlayButton) \\
            .colorize(Color()) \\
            .annotate("Control")
        ```
        """
        self.color = newColor
        return self

    def annotate(self, newAnnotation: str) -> 'ControlShadow':
        """
        Add an annotation to this control shadow

        This function differs from the annotation property, as it can be used
        in a"pipeline" fashion to apply multiple properties to a control
        quickly and easily.

        ### Args:
        * `newAnnotation` (`str`): new annotation to assign

        ### Returns:
        * `Self`: the same control, so that the pipeline can be continued

        ### Example usage

        This is best used when binding controls to quickly apply properties to
        the control.

        ```py
        # Bind to a play button, set its color to pink, and label it "control"
        shadow.bindControl(PlayButton) \\
            .colorize(Color.fromRgb(255, 0, 255)) \\
            .annotate("Control")
        ```
        """
        self.annotation = newAnnotation
        return self

    def apply(self, thorough: bool, transparent: bool) -> None:
        """
        Apply the configuration of the control shadow to the control it
        representsApply the configuration of the control shadow to the control
        it represents

        ### Args:
        * `thorough` (`bool`): whether we should always apply the values,
          regardless of whether they changed or not
        * `transparent` (`bool`): whether we should only set colors, and treat
          black as transparent
        """
        # If our device shadow is transparent, we should only set the color
        if transparent:
            if self.color != Color():
                # IDEA: Superimpose the added color
                # Requires smarter updating of plugins and stuff
                self._control.color = self.color
                self._changed = False
            elif self._changed:
                if not self._control.got_update:
                    self._control.color = self.color
                self._changed = False
        # If we're being thorough, or the shadow has changed since last time,
        # or if the control needs an update
        elif thorough or self._changed or self._control.needs_update:
            self._control.color = self.color
            self._control.annotation = self.annotation
            self._control.value = self.value
            self._changed = False


class NullControlShadow(IControlShadow):
    """
    A class that acts as a "shadow" to a physical control surface. This allows
    plugins to control properties of a control surface, with those changes
    only being applied if required.

    This class represents a control which failed to bind. It has dummy
    properties for the value, color and annotation, which means that those
    properties can be set easily in simple plugins, without the need for type
    checking.
    """
    @property
    def value(self) -> float:
        """
        Represents the value that will be applied to the control after
        the event has been processed, as a float between 0-1
        """
        return 0.0

    @value.setter
    def value(self, newVal: float) -> None:
        pass

    @property
    def color(self) -> Color:
        """
        Represents the color that will be applied to the control after the
        event has been processed.
        """
        return Color()

    @color.setter
    def color(self, newColor: Color) -> None:
        pass

    @property
    def annotation(self) -> str:
        """
        Represents the annotation that will be applied to the control after the
        event has been processed.
        """
        return ""

    @annotation.setter
    def annotation(self, newAnnotation: str) -> None:
        pass


class ControlShadowList:
    """
    A list of control shadows
    """
    def __init__(self, controls: list[ControlShadow]) -> None:
        """Create a list of controls"""
        self.controls = controls

    def __repr__(self) -> str:
        return f"ControlShadowList([{self.controls}])"

    def colorize(self, new: 'Color | list[Color]') -> 'ControlShadowList':
        """Set the colors of each control"""
        if isinstance(new, Color):
            for c in self.controls:
                c.color = new
        else:
            for control, color in zip(self.controls, new):
                control.color = color
        return self

    def annotate(self, new: 'str | list[str]') -> 'ControlShadowList':
        """Set the annotations of each control"""
        if isinstance(new, str):
            for c in self.controls:
                c.annotation = new
        else:
            for control, annotation in zip(self.controls, new):
                control.annotation = annotation
        return self

    def __iter__(self) -> Iterator:
        return iter(self.controls)

    def __len__(self) -> int:
        return len(self.controls)

    @overload
    def __getitem__(self, index: slice) -> 'ControlShadowList':
        ...

    @overload
    def __getitem__(self, index: int) -> 'ControlShadow':
        ...

    def __getitem__(self, index):
        if isinstance(index, slice):
            return ControlShadowList(self.controls[index])
        return self.controls[index]