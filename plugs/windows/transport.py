
from abc import abstractmethod
import transport
import ui

from typing import Any

from common.extensionmanager import ExtensionManager
from common.util.apifixes import PluginIndex
from controlsurfaces import (
    ControlShadow,
    NullEvent,
    PlayButton,
    StopButton,
    JogForwards,
    JogWheel,
    DirectionNext,
    DirectionPrevious,
    NavigationButtons,
    DirectionUp,
    DirectionDown,
    DirectionRight,
    DirectionLeft,
    DirectionSelect,
    RecordButton,
    LoopButton,
    MetronomeButton
)
from devices import DeviceShadow
from plugs import SpecialPlugin

from plugs.eventfilters import filterButtonLift

class Transport(SpecialPlugin):
    """
    The transport plugin manages basic transport commands, such as play/pause
    commands and navigation commands.
    """
    def __init__(self, shadow: DeviceShadow) -> None:
        super().__init__(shadow, [])
        shadow.bindMatches(NullEvent, self.nullEvent, raise_on_failure=False)
        shadow.bindMatch(PlayButton, self.playButton, raise_on_failure=False)
        shadow.bindMatch(StopButton, self.stopButton, raise_on_failure=False)
        shadow.bindMatch(JogWheel, self.jogWheel, raise_on_failure=False)
        shadow.bindMatch(RecordButton, self.recButton, raise_on_failure=False)
        shadow.bindMatch(LoopButton, self.loopButton, raise_on_failure=False)
        shadow.bindMatch(MetronomeButton, self.metroButton, raise_on_failure=False)
        shadow.bindMatches(NavigationButtons, self.navigationButtons, raise_on_failure=False)
    
    @classmethod
    def create(cls, shadow: DeviceShadow) -> 'SpecialPlugin':
        return cls(shadow)
    
    @staticmethod
    def shouldBeActive() -> bool:
        return True
    
    @filterButtonLift
    def playButton(self, control: ControlShadow, index: PluginIndex, *args: Any) -> bool:
        transport.start()
        return True

    @filterButtonLift
    def stopButton(self, control: ControlShadow, index: PluginIndex, *args: Any) -> bool:
        transport.stop()
        return True

    @filterButtonLift
    def recButton(self, control: ControlShadow, index: PluginIndex, *args: Any) -> bool:
        transport.record()
        return True
    
    @filterButtonLift
    def loopButton(self, control: ControlShadow, index: PluginIndex, *args: Any) -> bool:
        transport.setLoopMode()
        return True
    
    @filterButtonLift
    def metroButton(self, control: ControlShadow, index: PluginIndex, *args: Any) -> bool:
        transport.globalTransport(110, 1)
        return True

    def jogWheel(self, control: ControlShadow, index: PluginIndex, *args: Any) -> bool:
        
        increment = 1 if isinstance(control.getControl(), JogForwards) else -1
        
        ui.jog(increment)
        return True
    
    def nullEvent(self, control: ControlShadow, index: PluginIndex, *args: Any) -> bool:
        """Handle NullEvents for which no action should be taken
        """
        return True
    
    @filterButtonLift
    def navigationButtons(self, control: ControlShadow, index: PluginIndex, *args: Any) -> bool:
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
