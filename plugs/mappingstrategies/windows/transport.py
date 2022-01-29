
import transport
import ui

from typing import Any
from common.util.apifixes import PluginIndex
from controlsurfaces import (
    ControlShadow,
    PlayButton,
    StopButton,
    JogForwards,
    JogBackards,
    JogWheel
)
from devices import DeviceShadow
from plugs import Plugin

class Transport(Plugin):
    
    def __init__(self, shadow: DeviceShadow) -> None:
        super().__init__(shadow, [])
        shadow.bindFirstMatchSafe(PlayButton, self.playButton)
        shadow.bindFirstMatchSafe(StopButton, self.stopButton)
        shadow.bindFirstMatchSafe(JogWheel, self.jogWheel)
        
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
