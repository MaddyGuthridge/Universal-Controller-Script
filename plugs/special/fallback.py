
from typing import Any
import ui
from common.extensionmanager import ExtensionManager
from common.util.apifixes import UnsafeIndex, UnsafePluginIndex
from controlsurfaces import consts
from controlsurfaces import ControlShadowEvent
from controlsurfaces import MoveJogWheel, ShiftedJogWheel, StandardJogWheel, JogWheel
from devices import DeviceShadow
from plugs import SpecialPlugin
from plugs.mappingstrategies import PedalStrategy, WheelStrategy, NoteStrategy

class Fallback(SpecialPlugin):
    """
    Used to process events as a fallback if there isn't a plugin registered for
    the active FL plugin.
    
    Handles:
    * Pedals
    * Mod and pitch wheels
    * Notes
    """
    def __init__(self, shadow: DeviceShadow) -> None:
        shadow.bindMatches(JogWheel, self.jogWheel, raise_on_failure=False)
        super().__init__(shadow, [
            PedalStrategy(raise_on_error=False),
            WheelStrategy(raise_on_error=False),
            NoteStrategy()
        ])
    
    @staticmethod
    def shouldBeActive() -> bool:
        return True
    
    @classmethod
    def create(cls, shadow: DeviceShadow) -> 'SpecialPlugin':
        return cls(shadow)

    def jogWheel(self, control: ControlShadowEvent, index: UnsafeIndex, *args: Any) -> bool:
        if control.value == consts.ENCODER_NEXT:
            increment = 1
        elif control.value == consts.ENCODER_PREV:
            increment = -1
        elif control.value == consts.ENCODER_SELECT:
            ui.enter()
            return True
        else:
            return True
        
        if isinstance(control.getControl(), StandardJogWheel):
            ui.jog(increment)
        elif isinstance(control.getControl(), ShiftedJogWheel):
            ui.jog(increment)
        elif isinstance(control.getControl(), MoveJogWheel):
            ui.moveJog(increment)
        return True

ExtensionManager.registerSpecialPlugin(Fallback)
