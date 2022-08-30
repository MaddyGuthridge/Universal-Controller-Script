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

TriggerCallback = Callable[[ControlShadowEvent, UnsafeIndex, int], bool]
ColorCallback = Callable[[ControlShadow, UnsafeIndex, int], Color]
AnnotationCallback = Callable[[ControlShadow, UnsafeIndex, int], str]


def defaultColorCallback(
    control: ControlShadow,
    plug_index: UnsafeIndex,
    index: int,
) -> Color:
    """
    Provides a default color for drum pads bound using the drum pad strategy.
    """
    return Color.fromGrayscale(0.3)


def defaultAnnotationCallback(
    control: ControlShadow,
    plug_index: UnsafeIndex,
    index: int,
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
        invert_rows: bool = False,
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
          `TriggerCallback` should return a `bool` representing whether the
          event was handled, and should accept the following parameters:

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

        * `invert_rows` (`bool`, optional): whether to have the rows invert, so
          that the first row is at the bottom and the last is at the top. It
          does not respect the groupings made by the `height` parameter.
          Defaults to `False`
        """
        self.__width = width
        self.__height = height
        self.__do_update = do_property_update
        self.__trigger = trigger_callback
        self.__color: ColorCallback = (
            color_callback
            if color_callback is not None
            else defaultColorCallback
        )
        self.__annotate: AnnotationCallback = (
            annotation_callback
            if annotation_callback is not None
            else defaultAnnotationCallback
        )
        self.__invert_rows = invert_rows
        self.__mappings: Optional[list[list[int]]] = None
        self.__initialized_drums: Optional[list[list[bool]]] = None

        # Error checking
        if width == -1 and height != -1:
            raise ValueError(f"height ({height}) must be -1 if width is -1")
        super().__init__()

    def generateLayoutMapping(self, shadow: DeviceShadow) -> list[list[int]]:
        """
        Generate a mapping to use for the layout of the drum pads

        ### Args:
        * `shadow` (`DeviceShadow`): device to create the mapping for

        ### Returns:
        * `list[list[int]]`: mapping matrix
        """
        # Get the number of rows and columns
        rows, cols = shadow.getDevice().getDrumPadSize()

        # Determine the actual width and height of each chunk
        full_width = self.__width if self.__width != -1 else cols
        full_height = self.__height if self.__height != -1 else rows

        # Calculate the number of rows and columns we'll actually be able to
        # use
        reduced_rows = rows // full_height * full_height
        reduced_cols = cols // full_width * full_width

        # If we can't use any rows or columns, just use the maximum available
        if reduced_rows == 0:
            reduced_rows = rows
            full_height = rows
        if reduced_cols == 0:
            reduced_cols = cols
            full_width = cols

        # Determine the size of each subdivided chunk
        chunk_size = full_width * full_height

        def calcIndex(r: int, c: int) -> int:
            """
            Calculate the index used for any particular cell
            """
            # Return early for out-of-range values
            if (
                r >= reduced_rows
                or c >= reduced_cols
                or r < 0  # handles reversed indexes
            ):
                return -1
            # Outer values represent the coordinates of the chunk that the
            # index lies in
            outer_row = (
                r // self.__height
                if self.__height != -1
                else 0
            )
            outer_col = (
                c // self.__width
                if self.__width != -1
                else 0
            )

            # Inner values represent the coordinates within that chunk
            inner_row = r - full_height * outer_row
            inner_col = c - full_width * outer_col

            # Indexes are the index of the chunk and the value within the
            # chunk
            outer_idx = outer_col + rows // self.__width * outer_row
            inner_idx = inner_row * full_width + inner_col

            # We can add those together to get the overall index
            return outer_idx * chunk_size + inner_idx

        def row_mapper(r: int):
            """
            Function to account for the invert_rows property
            """
            return (reduced_rows - r - 1) if self.__invert_rows else r

        # Now fill in the matrix
        return [
            [
                calcIndex(row_mapper(r), c)
                for c in range(cols)
            ]
            for r in range(rows)
        ]

    def apply(self, shadow: DeviceShadow) -> None:
        rows, cols = shadow.getDevice().getDrumPadSize()

        drums = shadow.bindMatches(
            DrumPad,
            self.processTrigger,
            self.tick,
        )
        if (
            len(drums) != rows * cols
            and shadow.getDevice().getDrumPadSize() != (0, 0)
        ):
            raise ValueError("Unable to bind drum pads. Perhaps they were "
                             "already bound by another component of this "
                             "plugin?")

        self.__mappings = self.generateLayoutMapping(shadow)
        self.__initialized_drums = [
            [False for _ in range(cols)]
            for _ in range(rows)
        ]

    def processTrigger(
        self,
        control: ControlShadowEvent,
        plug: UnsafeIndex,
        *args: Any
    ) -> bool:
        assert self.__mappings is not None

        row, col = control.coordinate
        index = self.__mappings[row][col]
        if index == -1:
            # Not mapped to anything
            return True

        # Use the callback
        return self.__trigger(control, plug, index)

    def tick(
        self,
        control: ControlShadow,
        plug: UnsafeIndex,
        *args: Any
    ):
        assert self.__mappings is not None
        assert self.__initialized_drums is not None

        row, col = control.coordinate

        # If we're not updating the drums and they're already initialized, skip
        # it
        if not self.__do_update and self.__initialized_drums[row][col]:
            return

        index = self.__mappings[row][col]
        if index == -1:
            # Not mapped to anything
            return True

        # Use the callbacks
        control.color = self.__color(control, plug, index)
        control.annotation = self.__annotate(control, plug, index)

        self.__initialized_drums[row][col] = True
