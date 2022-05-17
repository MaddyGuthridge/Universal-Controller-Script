from typing import Any
import channels
from common.types.color import Color
from common.util.apifixes import UnsafeIndex
from controlsurfaces import ControlShadowEvent
from controlsurfaces import (
    DrumPad,
)
from devices import DeviceShadow
from plugs import WindowPlugin
from .helpers import coordToIndex, INDEX


class OmniPreview(WindowPlugin):
    """
    used to process omni preview mode
    """

    def __init__(self, shadow: DeviceShadow) -> None:
        self._drums = \
            shadow.bindMatches(DrumPad, self.drumPads)
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

    def tick(self):
        """Set colours and annotations for omni preview"""
        for drum in self._drums:
            index = coordToIndex(drum)
            if index == -1:
                continue
            drum.color = Color.fromInteger(channels.getChannelColor(index))
            drum.annotation = channels.getChannelName(index)
