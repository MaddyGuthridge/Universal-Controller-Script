
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
        shadow.bindMatch(PlayButton, self.playButton, raise_on_failure=False)
        shadow.bindMatch(StopButton, self.stopButton, raise_on_failure=False)
        shadow.bindMatch(JogWheel, self.jogWheel, raise_on_failure=False)
        
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
