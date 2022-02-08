
import plugins
import channels
from typing import Any
from common.extensionmanager import ExtensionManager
from common.util.apifixes import GeneratorIndex
from controlsurfaces import DrumPad
from controlsurfaces.controlshadow import ControlShadow
from devices import DeviceShadow
from plugs import StandardPlugin
from plugs.eventfilters import filterToGeneratorIndex

class FPC(StandardPlugin):
    """
    Used to interact with the FPC plugin, mapping drum pads to the required
    notes
    """
    def __init__(self, shadow: DeviceShadow) -> None:
        
        # Bind a different callback depending on drum pad size
        size = shadow.getDevice().getDrumPadSize()
        if size[0] >= 4 and size[1] >= 4:
            shadow.bindMatches(DrumPad, self.drumPad4x4)
        elif size[0] >= 2 and size[1] >= 8:
            shadow.bindMatches(DrumPad, self.drumPad2x8)
        
        super().__init__(shadow, [])
    
    @classmethod
    def create(cls, shadow: DeviceShadow) -> 'StandardPlugin':
        return cls(shadow)
    
    @staticmethod
    def getPlugId() -> str:
        return "FPC"
    
    @staticmethod
    def triggerPad(pad_idx: int, control: ControlShadow, ch_idx: int) -> None:
        note = plugins.getPadInfo(ch_idx, -1, 1, pad_idx)
        channels.midiNoteOn(ch_idx, note, int(control.getCurrentValue()*127))
    
    @filterToGeneratorIndex
    def drumPad4x4(self, control: ControlShadow, index: GeneratorIndex, *args: Any) -> bool:
        row, col = control.getControl().coordinate
        # Handle pads out of bounds as well
        if row >= 4 or col >= 4:
            return True
        coordToIndex = lambda r, c : 16 - (c + 1) * 4 + r
        self.triggerPad(coordToIndex(row, col), control, *index)
        return True
    
    @filterToGeneratorIndex
    def drumPad2x8(self, control: ControlShadow, index: GeneratorIndex, *args: Any) -> bool:
        row, col = control.getControl().coordinate
        # Handle pads out of bounds
        if row >= 2 or col >= 8:
            return True
        coordToIndex = lambda r, c : 4 * (1-r) + c + 4 * (c >= 4)
        self.triggerPad(coordToIndex(row, col), control, *index)
        return True

ExtensionManager.registerPlugin(FPC)
