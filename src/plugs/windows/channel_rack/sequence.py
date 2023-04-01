"""
plugs > windows channel_rack > sequence

Step sequencer for channel rack

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""

from typing import Any
import channels
import ui
from common.types.color import Color
from common.plug_indexes import UnsafeIndex
from control_surfaces import ControlShadowEvent
from control_surfaces import (
    DrumPad,
    DirectionLeft,
    DirectionRight,
    DirectionNext,
    DirectionPrevious,
    DirectionUp,
    DirectionDown,
)
from devices import DeviceShadow
from plugs import WindowPlugin
from plugs.event_filters import filterButtonLift
from .helpers import INDEX, getChannelRows

# How many steps should be scrolled each time
SCROLL_MULTIPLIER = 8

DISABLED_COLOR = Color()


class StepSequencer(WindowPlugin):
    """
    used to process omni preview mode
    """

    def __init__(self, shadow: DeviceShadow) -> None:
        self._drums = \
            shadow.bindMatches(DrumPad, self.drumPads)
        # Number of rows and cols
        self._height, self._width = shadow.getDevice().getDrumPadSize()
        # How far they scrolled
        self._scroll = 0
        self._left = shadow.bindMatch(DirectionLeft, self.left)
        self._right = shadow.bindMatch(DirectionRight, self.right)
        self._up = shadow.bindMatch(DirectionUp, self.up)
        self._down = shadow.bindMatch(DirectionDown, self.down)
        self._prev = shadow.bindMatch(DirectionPrevious, self.left)
        self._next = shadow.bindMatch(DirectionNext, self.right)
        super().__init__(shadow, [])

    @classmethod
    def getWindowId(cls) -> int:
        return INDEX

    @classmethod
    def create(cls, shadow: DeviceShadow) -> 'WindowPlugin':
        return cls(shadow)

    def drumPads(
        self,
        control: ControlShadowEvent,
        idx: UnsafeIndex,
        *args: Any
    ) -> bool:
        """Bind drum pads to step sequencer"""
        # Ignore button lifts
        if not control.value:
            return True
        # Row should apply to the offset of the selected channel
        # or if there aren't enough selections, the next selections along
        selections = getChannelRows()

        row, col = control.getControl().coordinate

        # Implement scrolling
        col += SCROLL_MULTIPLIER * self._scroll

        # Check for index out of range
        if row >= len(selections):
            return True
        # Get selected row
        ch_idx = selections[row]

        val = not channels.getGridBit(ch_idx, col)
        channels.setGridBit(ch_idx, col, val)
        return True

    def showGrid(self) -> None:
        """Show the channel rack grid"""
        col = self._scroll * SCROLL_MULTIPLIER

        # FIXME: This might get an index error on controllers with no drum pads
        row = getChannelRows()[0]

        ui.crDisplayRect(
            col,
            row,
            self._width,
            self._height,
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

    def tick(self, *args):
        """Set colors and annotations for omni-preview"""
        # Row should apply to the offset of the selected channel
        # or if there aren't enough selections, the next selections along
        selections = getChannelRows()

        for control in self._drums:
            row, col = control.getControl().coordinate

            if row >= len(selections):
                control.color = DISABLED_COLOR
                continue

            ch_idx = selections[row]

            # Implement scrolling
            col += SCROLL_MULTIPLIER * self._scroll

            # Determine color to use for when the grid bit isn't set
            # if (col // SCROLL_MULTIPLIER) % 2:
            #     false_color = BACK_BEAT_COLOR
            # else:
            #     false_color = LEAD_BEAT_COLOR
            on_color = Color.fromGrayscale(1)

            off_color = Color.fromInteger(
                channels.getChannelColor(ch_idx),
                enabled=False
            )
            if channels.getGridBit(ch_idx, col):
                control.color = on_color
            else:
                control.color = off_color
