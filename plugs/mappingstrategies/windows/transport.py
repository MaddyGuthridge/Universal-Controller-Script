
import transport
import ui

from typing import Any
from common.util.apifixes import PluginIndex
from controlsurfaces import ControlShadow, JogForwards, JogBackards, JogWheel
from devices import DeviceShadow
from plugs import Plugin

class Transport(Plugin):
    
    def __init__(self, shadow: DeviceShadow) -> None:
        super().__init__(shadow, [])
        
    def playButton(self, control: ControlShadow, index: PluginIndex, *args: Any):
        transport.start()

    def stopButton(self, control: ControlShadow, index: PluginIndex, *args: Any):
        transport.stop()

    def jogWheel(self, control: ControlShadow, index: PluginIndex, *args: Any):
        
        increment = 1 if isinstance(control.getControl(), JogForwards) else -1
        
        ui.jog(increment)
