"""
plugs > mapping_strategies > drum_pad_strategy

Mapping strategy to simplify the handling of drum pads.

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""
from typing import Callable, Optional, Any
from . import IMappingStrategy
from common.plug_indexes import UnsafeIndex
from devices import DeviceShadow
from common.types import Color

from control_surfaces import (
    ControlShadow,
    DrumPad,
    ControlShadowEvent,
)

TriggerCallback = Callable[[int, ControlShadowEvent, UnsafeIndex], None]
ColorCallback = Callable[[int, ControlShadow, UnsafeIndex], Color]
AnnotationCallback = Callable[[int, ControlShadow, UnsafeIndex], str]


def defaultColorCallback(
    index: int,
    control: ControlShadow,
    plug_index: UnsafeIndex,
) -> Color:
    """
    Provides a default color for drum pads bound using the drum pad strategy.
    """
    return Color.fromGrayscale(0.3)


def defaultAnnotationCallback(
    index: int,
    control: ControlShadow,
    plug_index: UnsafeIndex,
) -> str:
    """
    Provides a default annotation for drum pads bound using the drum pad
    strategy.
    """
    return ""


class DrumPadStrategy(IMappingStrategy):
    """
    The drum pad strategy allows for mapping drum pad controls to drums or
    keyswitches. It handles various drum pad dimensions in order to ensure that
    content is fit to them as correctly as possible.
    """

    def __init__(
        self,
        width: int,
        height: int,
        do_property_update: bool,
        trigger_callback: TriggerCallback,
        color_callback: Optional[ColorCallback] = None,
        annotation_callback: Optional[AnnotationCallback] = None,
    ) -> None:
        """
        Create an instance of a drum pad strategy

        This will link all available drum pads, using the provided callback
        functions to manage the control surfaces.

        VS Code's markdown parsing is inherently broken for nested dot points,
        and as such I apologize in advance for the awfulness that you are about
        to witness. If you need to read this, you should hit F12 on the
        function definition and read it at the actual definition. Either that,
        or you can read the docs on the documentation website once I make it.

        ### Args:
        * `width` (`int`): the width of a single row of controls. This is used
          to determine how to arrange rows and columns for each control. After
          every `n` drum pads (where `n = width`), the index of the drum pad
          wraps around to start a new row. After running out of rows on the
          drum pad grid, another group of columns will be wrapped around to,
          although the `height` parameter is also respected. If the width of
          the controls is not important, this value and the `height` should be
          set to `-1`.

        * `height` (`int`): the height of a group of controls. This is used to
          determine how to arrange rows and columns for each control. After
          every `m` rows of drum pads (where `m = height`), drum pad indexes
          will wrap around to the next group of `n` columns (where
          `n = width`). If the height of the controls is not important, this
          value should be set to `-1`.

        * `do_property_update` (`bool`): whether the color and annotation
          properties of each drum pad should be updated after the initial
          binding.

        * `trigger_callback` (`TriggerCallback`): the callback
          function to call when a drum pad is triggered. It should be used to
          trigger any functionality required for when the drum pad is hit. A
          `TriggerCallback` should accept the following parameters:

              * `int`: the index of the drum pad, as determined by the width
                and height specified when creating the drum pad strategy.

              * `ControlShadowEvent`: the event that caused the trigger. The
                data from this event can be used to determine the value and
                coordinate of the drum pad.

              * `UnsafeIndex`: the index of the plugin or window associated
                with this strategy.

        * `color_callback` (`ColorCallback`, optional): the callback
          function to determine the color of a drum pad. Defaults to `None`,
          meaning that the color for each drum pad will be gray. The callback
          should return a `Color` object, and accept the following parameters:

              * `int`: the index of the drum pad, as determined by the width
                and height specified when creating the drum pad strategy.

              * `ControlShadow`: the control that is associated with this
                index. The data from this can be used to determine the value
                and coordinate of the drum pad if required.

              * `UnsafeIndex`: the index of the plugin or window associated
                with this strategy.

        * `annotation_callback` (`Callable[[int], str]`, optional): the
          callback function to determine the annotation for a drum pad. The
          parameter is the drum pad index. Defaults to `None`, meaning that the
          annotation for each drum pad will be unset.
        """
        self.__width = width
        self.__height = height
        self.__do_update = do_property_update
        self.__trigger = trigger_callback
        self.__color = color_callback
        self.__annotate = annotation_callback
        super().__init__()

    def apply(self, shadow: DeviceShadow) -> None:
        shadow.bindMatches(
            DrumPad,
            self.processTrigger,
            self.tick,
        )

    def processTrigger(
        self,
        control: ControlShadowEvent,
        index: UnsafeIndex,
        *args: Any
    ) -> bool:
        return False

    def tick(
        self,
        control: ControlShadow,
        index: UnsafeIndex,
        *args: Any
    ):
        ...
