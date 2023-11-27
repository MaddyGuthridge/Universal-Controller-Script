"""
integrations > mapping_strategies > drum_pad_strategy

Mapping strategy to simplify the handling of drum pads.

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""
import itertools
from typing import Callable, Optional, Any

from common.plug_indexes import FlIndex, WindowIndex, PluginIndex
from devices import DeviceShadow
from common.types import Color
from common.util.grid_mapper import GridCell, grid_map

from control_surfaces import (
    ControlShadow,
    DrumPad,
    ControlShadowEvent,
)

TriggerCallback = Callable[[ControlShadowEvent, FlIndex, GridCell], bool]
ColorCallback = Callable[[ControlShadow, FlIndex, GridCell], Color]
AnnotationCallback = Callable[[ControlShadow, FlIndex, GridCell], str]


class color_callbacks:
    """
    A collection of simple callbacks for generating colors that can be used
    to color drum pads
    """
    @staticmethod
    def white(
        control: ControlShadow,
        plug_index: FlIndex,
        index: GridCell,
    ) -> Color:
        """
        Colors all drum pads white with brightness 0.3
        """
        return Color.fromGrayscale(0.3)

    @staticmethod
    def channelColor(
        control: ControlShadow,
        plug_index: FlIndex,
        index: GridCell,
    ) -> Color:
        """
        Colors all drum pads white with the channel or mixer track color

        Leaves FL Studio windows as white
        """

        # FL Studio windows should use white
        if isinstance(plug_index, WindowIndex):
            return Color.fromGrayscale(0.3)

        # It's a plugin
        assert isinstance(plug_index, PluginIndex)
        return plug_index.track.color


class annotation_callbacks:
    """
    A collection of simple callbacks for generating annotations that can be
    used to describe drum pads
    """
    @staticmethod
    def empty(
        control: ControlShadow,
        plug_index: FlIndex,
        index: GridCell,
    ) -> str:
        """
        Provides a default annotation for drum pads bound using the drum pad
        strategy.
        """
        return ""


class GridStrategy:
    """
    The grid strategy can be used for creating grid-like layouts that adapt to
    the drum pad layout of various MIDI controllers.
    """

    def __init__(
        self,
        shadow: DeviceShadow,
        group_width: Optional[int],
        group_height: Optional[int],
        trigger_callback: TriggerCallback,
        left_to_right: bool = True,
        top_to_bottom: bool = True,
        horizontal_before_vertical: bool = True,
        truncate_overflows: bool = False,
        wrap_overflows: bool = False,
        do_property_update: bool = True,
        color_callback: ColorCallback = color_callbacks.channelColor,
        annotation_callback: AnnotationCallback = annotation_callbacks.empty,
    ) -> None:
        """
        Create an instance of a grid strategy strategy

        This will link all available drum pads, using the provided callback
        functions to manage the control surfaces.

        VS Code's markdown parsing is inherently broken for nested dot points,
        and as such I apologize in advance for the awfulness that you are about
        to witness. If you need to read this, you should hit F12 on the
        function definition and read it at the actual definition. Either that,
        or you can read the docs on the documentation website once I make it.

        ### Args:
        * `shadow` (`DeviceShadow`): the device shadow to bind the mappings to

        * `group_width` (`Optional[int]`): the width of a single row of
          controls. This is used to determine how to arrange rows and columns
          for each control. After every `n` drum pads (where `n = width`), the
          index of the drum pad wraps around to start a new row. After running
          out of rows on the drum pad grid, another group of columns will be
          wrapped around to, although the `height` parameter is also respected.
          If the width of the controls is not important, this value and the
          `height` should be set to `None`.

        * `group_height` (`Optional[int]`): the height of a group of controls.
          This is used to determine how to arrange rows and columns for each
          control. After every `m` rows of drum pads (where `m = height`), drum
          pad indexes will wrap around to the next group of `n` columns (where
          `n = width`). If the height of the controls is not important, this
          value should be set to `None`.

        * `left_to_right` (`bool`, optional): whether to place groups
          left-to-right (`True`) or right-to-left (`False`). Defaults to
          `True`.

        * `top_to_bottom` (`bool`, optional): whether to place groups
          top-to-bottom (`True`) or bottom-to-top (`False`). Defaults to
          `True`.

        * `horizontal_before_vertical` (`bool`, optional): Whether to fill
          groups horizontally first or vertically first. If `True`, elements
          are filled across, then vertically once each row is filled. Defaults
          to `True`.

        * `truncate_overflows` (`bool`, optional): whether to truncate groups
          that are too big to fit into the group (`True`) or to not place them
          at all (`False`). Defaults to `False`.

        * `wrap_overflows` (`bool`, optional): whether to wrap groups that
          are too big to fit into the group (`True`) or to not place them at
          all (`False`). Defaults to `False`.

        * `do_property_update` (`bool`): whether the color and annotation
          properties of each drum pad should be updated after the initial
          binding.

        * `trigger_callback` (`TriggerCallback`): the callback
          function to call when a drum pad is triggered. It should be used to
          trigger any functionality required for when the drum pad is hit. A
          `TriggerCallback` should return a `bool` representing whether the
          event was handled, and should accept the following parameters:

              * `GridCell`: the index of the drum pad, as determined by the
                width and height specified when creating the drum pad strategy.

              * `ControlShadowEvent`: the event that caused the trigger. The
                data from this event can be used to determine the value and
                coordinate of the drum pad.

              * `FlIndex`: the index of the plugin or window associated
                with this strategy.

        * `color_callback` (`ColorCallback`, optional): the callback
          function to determine the color of a drum pad. Defaults to
          `color_callbacks.channelColor`, meaning that the color for each drum
          pad will be gray. The callback should return a `Color` object, and
          accept the following parameters:

              * `GridCell`: the index of the drum pad, as determined by the
                width and height specified when creating the drum pad strategy.

              * `ControlShadow`: the control that is associated with this
                index. The data from this can be used to determine the value
                and coordinate of the drum pad if required.

              * `FlIndex`: the index of the plugin or window associated
                with this strategy.

        * `annotation_callback` (`Callable[[int], str]`, optional): the
          callback function to determine the annotation for a drum pad. The
          parameter is the drum pad index. Defaults to
          `annotation_callbacks.empty`, meaning that the annotation for each
          drum pad will be unset.
        """
        # Width and height of each group
        self.__group_width = group_width
        self.__group_height = group_height

        # Whether to update properties
        self.__do_update = do_property_update

        # Directions
        self.__left_to_right = left_to_right
        self.__top_to_bottom = top_to_bottom
        self.__horizontal_before_vertical = horizontal_before_vertical

        # Truncation and wrapping
        self.__truncate_overflows = truncate_overflows
        self.__wrap_overflows = wrap_overflows

        # Callbacks
        self.__trigger = trigger_callback
        self.__color = color_callback
        self.__annotate: AnnotationCallback = annotation_callback

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

        self.__mappings = grid_map(
            cols,
            rows,
            self.__group_width,
            self.__group_height,
            self.__left_to_right,
            self.__top_to_bottom,
            self.__horizontal_before_vertical,
            self.__truncate_overflows,
            self.__wrap_overflows,
        )
        # list of drums we've initialized
        self.__initialized_drums = [
            [False for _ in range(cols)]
            for _ in range(rows)
        ]

    def get_num_groups_mapped(self) -> int:
        """
        Returns the number of groups that have been mapped using the strategy.

        ### Raises
        * `ValueError`: the mapping strategy hasn't been applied yet

        ### Returns:
        * `int`: the number of groups that were mapped by the strategy.
        """
        return max(map(
            lambda cell: 0 if cell is None else cell.group_number,
            itertools.chain.from_iterable(self.__mappings),
        )) + 1

    def get_group_size(self) -> int:
        """
        Returns the size of all the groups that have been mapped using the
        strategy.

        ### Raises
        * `ValueError`: the mapping strategy hasn't been applied yet

        ### Returns:
        * `int`: the size of each group mapped by the strategy
        """
        return max(map(
            lambda cell: 0 if cell is None else cell.group_size,
            itertools.chain.from_iterable(self.__mappings),
        ))

    def processTrigger(
        self,
        control: ControlShadowEvent,
        plug: FlIndex,
        *args: Any
    ) -> bool:
        assert self.__mappings is not None

        row, col = control.coordinate
        index = self.__mappings[row][col]
        if index is None:
            # Not mapped to anything
            return True

        # Use the callback
        return self.__trigger(control, plug, index)

    def tick(
        self,
        control: ControlShadow,
        plug: FlIndex,
        *args: Any
    ):
        row, col = control.coordinate

        # If we're not updating the drums and they're already initialized, skip
        # it
        if not self.__do_update and self.__initialized_drums[row][col]:
            return

        index = self.__mappings[row][col]
        if index is None:
            # Not mapped to anything
            return

        # Use the callbacks
        control.color = self.__color(control, plug, index)
        control.annotation = self.__annotate(control, plug, index)

        self.__initialized_drums[row][col] = True
