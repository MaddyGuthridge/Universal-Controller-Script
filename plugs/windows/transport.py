
from abc import abstractmethod
import transport
import ui

from typing import Any

from common import ExtensionManager
from common.util.apifixes import PluginIndex
from controlsurfaces import (
    ControlShadow,
    PlayButton,
    StopButton,
    JogForwards,
    JogBackards,
    JogWheel,
    NextPrevButtons,
    DirectionNext,
    DirectionPrevious,
    DirectionButtons,
    DirectionUp,
    DirectionDown,
    DirectionRight,
    DirectionLeft,
    DirectionSelect
)
from devices import DeviceShadow
from plugs import SpecialPlugin

class Transport(SpecialPlugin):
    
    def __init__(self, shadow: DeviceShadow) -> None:
        super().__init__(shadow, [])
        shadow.bindMatch(PlayButton, self.playButton, raise_on_failure=False)
        shadow.bindMatch(StopButton, self.stopButton, raise_on_failure=False)
        shadow.bindMatch(JogWheel, self.jogWheel, raise_on_failure=False)
        # TODO: Bind navigation controls
    
    @classmethod
    def create(cls, shadow: DeviceShadow) -> 'SpecialPlugin':
        return cls(shadow)
    
    @staticmethod
    def shouldBeActive() -> bool:
        return True
    
    def playButton(self, control: ControlShadow, index: PluginIndex, *args: Any) -> bool:
        transport.start()
        return True

    def stopButton(self, control: ControlShadow, index: PluginIndex, *args: Any) -> bool:
        transport.stop()
        return True

    def jogWheel(self, control: ControlShadow, index: PluginIndex, *args: Any) -> bool:
        
        increment = 1 if isinstance(control.getControl(), JogForwards) else -1
        
        ui.jog(increment)
        return True
    
    def navigation(self, control: ControlShadow, index: PluginIndex, *args: Any) -> bool:
        c_type = type(control.getControl())
        if c_type == DirectionUp:
            ui.up()
        elif c_type == DirectionDown:
            ui.down()
        elif c_type == DirectionLeft:
            ui.left()
        elif c_type == DirectionRight:
            ui.right()
        elif c_type == DirectionSelect:
            ui.enter()
        elif c_type == DirectionNext:
            ui.next()
        elif c_type == DirectionPrevious:
            ui.previous()
        else:
            return False
        return True

ExtensionManager.registerSpecialPlugin(Transport)
