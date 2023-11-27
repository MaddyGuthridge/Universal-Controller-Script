"""
integrations > window > channel_rack > sequence

Step sequencer integration for channel rack

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""
import channels
import ui
from common.types.color import Color
from common.plug_indexes import FlIndex, WindowIndex
from common.util.grid_mapper import GridCell
from control_surfaces import ControlShadowEvent
from control_surfaces import (
    DirectionLeft,
    DirectionRight,
    DirectionNext,
    DirectionPrevious,
    DirectionUp,
    DirectionDown,
)
from control_surfaces.control_shadow import ControlShadow
from devices import DeviceShadow
from integrations import WindowIntegration
from integrations.event_filters import filterButtonLift
from integrations.mapping_strategies.grid_strategy import GridStrategy
from .helpers import INDEX, getChannelRows

# How many steps should be scrolled each time
SCROLL_MULTIPLIER = 8

DISABLED_COLOR = Color()


class StepSequencer(WindowIntegration):
    """
    used to process omni preview mode
    """

    def __init__(self, shadow: DeviceShadow) -> None:
        self._drums = GridStrategy(
            shadow,
            16,
            1,
            self.triggerDrumPad,
            color_callback=self.colorDrumPad,
            # FIXME: Looks like horizontal_before_vertical is having,,, issues
            # when set, indexes for wrapped rows are utterly incorrect
            # horizontal_before_vertical=False,
            wrap_overflows=True,
        )
        # How far they scrolled
        self._scroll = 0

        self._left = shadow.bindMatch(DirectionLeft, self.left)
        self._right = shadow.bindMatch(DirectionRight, self.right)
        self._up = shadow.bindMatch(DirectionUp, self.up)
        self._down = shadow.bindMatch(DirectionDown, self.down)
        self._prev = shadow.bindMatch(DirectionPrevious, self.left)
        self._next = shadow.bindMatch(DirectionNext, self.right)
        super().__init__(shadow)

    @classmethod
    def getWindowId(cls) -> WindowIndex:
        return INDEX

    @classmethod
    def create(cls, shadow: DeviceShadow) -> 'WindowIntegration':
        return cls(shadow)

    def triggerDrumPad(
        self,
        control: ControlShadowEvent,
        idx: FlIndex,
        cell: GridCell,
    ) -> bool:
        """
        Handle drum pad events
        """
        # For now, just ignore release events
        # TODO: Later use them to implement graph editor features
        if not control.value:
            return False
        channel = cell.group_number + getChannelRows()[0].index
        index = cell.group_index + self._scroll * SCROLL_MULTIPLIER

        val = channels.getGridBit(channel, index)
        channels.setGridBit(channel, index, not val)
        return True

    def colorDrumPad(
        self,
        control: ControlShadow,
        idx: FlIndex,
        cell: GridCell,
    ) -> Color:
        """
        Determine color for drum pads
        """
        channel = cell.group_number + getChannelRows()[0].index
        index = cell.group_index + self._scroll * SCROLL_MULTIPLIER

        on_color = Color.fromGrayscale(1)

        off_color = Color.fromInteger(
            channels.getChannelColor(channel),
            enabled=False
        )
        if channels.getGridBit(channel, index):
            return on_color
        else:
            return off_color

    def showGrid(self) -> None:
        """Show the channel rack grid"""
        col = self._scroll * SCROLL_MULTIPLIER

        # FIXME: This might get an index error on controllers with no drum pads
        row = getChannelRows()[0].index

        width = self._drums.get_group_size()
        height = self._drums.get_num_groups_mapped()

        ui.crDisplayRect(
            col,
            row,
            width,
            height,
            1000,
        )

    @filterButtonLift()
    def left(self, *args) -> bool:
        """Scroll left"""
        self._scroll = max(self._scroll - 1, 0)
        self.showGrid()
        return True

    @filterButtonLift()
    def right(self, *args) -> bool:
        """Scroll right"""
        self._scroll += 1
        self.showGrid()
        return True

    @filterButtonLift()
    def up(self, *args) -> bool:
        """Scroll up"""
        new = channels.selectedChannel() - 1
        if new < 0:
            new = channels.channelCount(True) - 1
        channels.selectOneChannel(new)
        self.showGrid()
        return True

    @filterButtonLift()
    def down(self, *args) -> bool:
        """Scroll down"""
        new = channels.selectedChannel() + 1
        if new >= channels.channelCount(True):
            new = 0
        channels.selectOneChannel(new)
        self.showGrid()
        return True
