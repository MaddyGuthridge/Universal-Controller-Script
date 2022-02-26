
import plugins
import channels
from typing import Any
from common.types import Color
from common.extensionmanager import ExtensionManager
from common.util.apifixes import GeneratorIndex
from controlsurfaces import DrumPad
from controlsurfaces import ControlShadowEvent
from devices import DeviceShadow
from plugs import StandardPlugin
from plugs import eventfilters, tickfilters

class FPC(StandardPlugin):
    """
    Used to interact with the FPC plugin, mapping drum pads to the required
    notes
    """
    def __init__(self, shadow: DeviceShadow) -> None:
        
        # Bind a different callback depending on drum pad size
        size = shadow.getDevice().getDrumPadSize()
        if size[0] >= 4 and size[1] >= 4:
            self._pads = shadow.bindMatches(DrumPad, self.drumPad4x4)
            self._coordToIndex = lambda r, c : 16 - (c + 1) * 4 + r
        elif size[0] >= 2 and size[1] >= 8:
            self._pads = shadow.bindMatches(DrumPad, self.drumPad2x8)
            self._coordToIndex = lambda r, c : 4 * (1-r) + c + 4 * (c >= 4)
        
        super().__init__(shadow, [])
    
    @classmethod
    def create(cls, shadow: DeviceShadow) -> 'StandardPlugin':
        return cls(shadow)
    
    @staticmethod
    def getPlugIds() -> tuple[str, ...]:
        return ("FPC",)

    @tickfilters.toGeneratorIndex
    def tick(self, index: GeneratorIndex):
        for p in self._pads:
            p.color = Color.fromInteger(
                plugins.getPadInfo(index[0], -1, 2, self._coordToIndex(*p.coordinate))
            )
    
    @staticmethod
    def triggerPad(pad_idx: int, control: ControlShadowEvent, ch_idx: int) -> None:
        note = plugins.getPadInfo(ch_idx, -1, 1, pad_idx)
        # Work-around for horrible bug where wrong note numbers are given
        if note > 127:
            note = note >> 16
        channels.midiNoteOn(ch_idx, note, int(control.value*127))
    
    @eventfilters.toGeneratorIndex
    def drumPad4x4(self, control: ControlShadowEvent, index: GeneratorIndex, *args: Any) -> bool:
        row, col = control.getShadow().coordinate
        # Handle pads out of bounds as well
        if row >= 4 or col >= 4:
            return True
        self.triggerPad(self._coordToIndex(row, col), control, *index)
        return True
    
    @eventfilters.toGeneratorIndex
    def drumPad2x8(self, control: ControlShadowEvent, index: GeneratorIndex, *args: Any) -> bool:
        row, col = control.getShadow().coordinate
        # Handle pads out of bounds
        if row >= 2 or col >= 8:
            return True
        self.triggerPad(self._coordToIndex(row, col), control, *index)
        return True

ExtensionManager.registerPlugin(FPC)
