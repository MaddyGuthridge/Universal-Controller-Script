
from typing import Any
import channels
from common import getContext
from common.extensionmanager import ExtensionManager
from common.types.color import Color
from common.util.apifixes import UnsafeIndex
from controlsurfaces import ControlShadowEvent, ControlShadow
from controlsurfaces import (
    DrumPad,
)
from devices import DeviceShadow
from plugs import WindowPlugin

INDEX = 1


class ChannelRack(WindowPlugin):
    """
    Used to process events directed at the channel rack
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

    @staticmethod
    def coordToIndex(control: ControlShadow) -> int:
        """Return the global index of a channel given a drum pad coordinate

        If the drum pad maps to nothing, -1 is returned.
        """
        assert isinstance(control.getControl(), DrumPad)
        drums_width = getContext().getDevice().getDrumPadSize()[1]
        row, col = control.getControl().coordinate
        index = drums_width * row + col
        if index >= channels.channelCount(1):
            return -1
        return index

    def tick(self):
        self.tickOmniPreview()

    def drumPads(
        self,
        control: ControlShadowEvent,
        idx: UnsafeIndex,
        *args: Any
    ) -> bool:
        """Bind drum pads to omni preview"""
        try:
            idx = channels.getChannelIndex(
                self.coordToIndex(control.getShadow())
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

    def tickOmniPreview(self):
        """Set colours and annotations for omni preview"""
        for drum in self._drums:
            index = self.coordToIndex(drum)
            if index == -1:
                continue
            drum.color = Color.fromInteger(channels.getChannelColor(index))
            drum.annotation = channels.getChannelName(index)


ExtensionManager.registerWindowPlugin(ChannelRack)
