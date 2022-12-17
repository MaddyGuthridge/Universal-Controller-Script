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
from plugs.mapping_strategies import DrumPadStrategy
from devices import DeviceShadow
from plugs import WindowPlugin
from plugs.event_filters import filterButtonLift
from .helpers import INDEX, getChannelRows

# How many steps should be scrolled each time
SCROLL_MULTIPLIER = 4

DISABLED_COLOR = Color()


class StepSequencer(WindowPlugin):
    """
    used to process omni preview mode
    """

    def __init__(self, shadow: DeviceShadow) -> None:
        drum_pads = DrumPadStrategy(
            width=16,
            height=-1,
            do_property_update=True,
            
        )
        super().__init__(shadow, [])

    @classmethod
    def getWindowId(cls) -> int:
        return INDEX

    @classmethod
    def create(cls, shadow: DeviceShadow) -> 'StepSequencer':
        return cls(shadow)

    def getDrumLayout(self) -> list[list[tuple[int, int]]]:
        """
        Returns the layout of drum pad mappings for the step sequencer

        ### Returns:
        * `list[list[tuple[int, int]]]`: 2D matrix, where each cell contains:
                * Channel offset
                * Step number for that channel
        """
        return [
            [
                (0, 0) for _ in range(self._width)
            ] for _ in range(self._height)
        ]

    def drumPads(
        self,
        control: ControlShadowEvent,
        idx: UnsafeIndex,
        *args: Any
    ) -> bool:
        """Bind drum pads to step sequencer"""

        return True

    def showGrid(self) -> None:
        """Show the channel rack grid"""

    @filterButtonLift()
    def left(self, *args) -> bool:
        """Scroll left"""
        return True

    @filterButtonLift()
    def right(self, *args) -> bool:
        """Scroll right"""
        return True

    @filterButtonLift()
    def up(self, *args) -> bool:
        """Scroll up"""
        return True

    @filterButtonLift()
    def down(self, *args) -> bool:
        """Scroll down"""
        return True

    def tick(self, *args):
        """Set colors and annotations for omni-preview"""
