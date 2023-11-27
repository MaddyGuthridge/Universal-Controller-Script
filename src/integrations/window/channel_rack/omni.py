"""
integrations > window > channel_rack > omni

Omni preview integration for channel rack

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""

from typing import Any
import channels
from common.plug_indexes import WindowIndex
from common.types.color import Color
from common.plug_indexes import FlIndex
from control_surfaces import ControlShadowEvent
from control_surfaces import DrumPad
from devices import DeviceShadow
from integrations import WindowIntegration
from .helpers import coordToIndex, INDEX


class OmniPreview(WindowIntegration):
    """
    Used to process omni preview mode on the channel rack
    """

    def __init__(self, shadow: DeviceShadow) -> None:
        self._drums = \
            shadow.bindMatches(DrumPad, self.drumPads)
        super().__init__(shadow)

    @classmethod
    def getWindowId(cls) -> WindowIndex:
        return INDEX

    @classmethod
    def create(cls, shadow: DeviceShadow) -> 'WindowIntegration':
        return cls(shadow)

    def drumPads(
        self,
        control: ControlShadowEvent,
        window_index: FlIndex,
        *args: Any
    ) -> bool:
        """Bind drum pads to omni preview"""
        try:
            idx = channels.getChannelIndex(
                coordToIndex(control.getShadow())
            )
        except TypeError:  # Index out of range
            return True
        channels.midiNoteOn(
            idx,
            60,
            int(control.value * 127),
            control.channel
        )
        return True

    def tick(self, *args):
        """Set colors and annotations for omni preview"""
        for drum in self._drums:
            index = coordToIndex(drum)
            if index == -1:
                drum.color = Color()
                drum.annotation = ""
            else:
                drum.color = Color.fromInteger(channels.getChannelColor(index))
                drum.annotation = channels.getChannelName(index)
