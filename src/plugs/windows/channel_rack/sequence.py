from typing import Any
import channels
from common.types.color import Color
from common.util.apifixes import UnsafeIndex, getSelectedChannels
from controlsurfaces import ControlShadowEvent
from controlsurfaces import (
    DrumPad,
)
from devices import DeviceShadow
from plugs import WindowPlugin
from .helpers import coordToIndex, INDEX


class StepSequencer(WindowPlugin):
    """
    used to process omni preview mode
    """

    def __init__(self, shadow: DeviceShadow) -> None:
        self._drums = \
            shadow.bindMatches(DrumPad, self.drumPads, raise_on_failure=False)
        super().__init__(shadow, [])

    @staticmethod
    def getWindowId() -> int:
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
        selections = getSelectedChannels(global_mode=False)

        row, col = control.getControl().coordinate

        # If there aren't enough selections
        if len(selections) <= row:
            # Get the last selected channel
            # There can't be more selections than the number of channels
            ch_idx = channels.selectedChannel(
                False,
                channels.channelCount(True)
            ) + (row - len(selections) + 1)
        else:
            ch_idx = selections[row]

        val = not channels.getGridBit(ch_idx, col)
        channels.setGridBit(ch_idx, col, val)
        return True

    def tick(self):
        """Set colours and annotations for omni preview"""
        # Row should apply to the offset of the selected channel
        # or if there aren't enough selections, the next selections along
        selections = getSelectedChannels(global_mode=False)

        for control in self._drums:
            row, col = control.getControl().coordinate

            # If there aren't enough selections
            if len(selections) <= row:
                # Get the last selected channel
                # There can't be more selections than the number of channels
                ch_idx = channels.selectedChannel(
                    False,
                    channels.channelCount(True)
                ) + (row - len(selections) + 1)
            else:
                ch_idx = selections[row]

            c = Color.fromInteger(channels.getChannelColor(ch_idx))
            if channels.getGridBit(ch_idx, col):
                control.color = c
            else:
                control.color = c.fadeGray()
