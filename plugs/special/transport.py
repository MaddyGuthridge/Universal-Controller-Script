
from abc import abstractmethod
import channels
import general
import transport
import ui

from typing import Any

from common.extensionmanager import ExtensionManager
from common import getContext
from common.util.apifixes import UnsafeIndex
from controlsurfaces import (
    ControlShadowEvent,
    NullEvent,
    PlayButton,
    StopButton,
    DirectionNext,
    DirectionPrevious,
    NavigationButton,
    DirectionUp,
    DirectionDown,
    DirectionRight,
    DirectionLeft,
    DirectionSelect,
    RecordButton,
    LoopButton,
    MetronomeButton,
    UndoButton,
    RedoButton,
    UndoRedoButton,
    SaveButton,
    QuantizeButton,
    SwitchActiveButton,
    SwitchActivePluginButton,
    SwitchActiveWindowButton,
    SwitchActiveToggleButton,
)
from controlsurfaces import consts
from devices import DeviceShadow
from plugs import SpecialPlugin

from plugs.eventfilters import filterButtonLift

class Transport(SpecialPlugin):
    """
    The transport plugin manages basic transport commands, such as play/pause
    commands and navigation commands.
    """
    def __init__(self, shadow: DeviceShadow) -> None:
        shadow.setTransparent(True)
        super().__init__(shadow, [])
        shadow.bindMatches(NullEvent, self.nullEvent, raise_on_failure=False)
        shadow.bindMatch(PlayButton, self.playButton, raise_on_failure=False)
        shadow.bindMatch(StopButton, self.stopButton, raise_on_failure=False)
        shadow.bindMatch(RecordButton, self.recButton, raise_on_failure=False)
        shadow.bindMatch(LoopButton, self.loopButton, raise_on_failure=False)
        shadow.bindMatch(MetronomeButton, self.metroButton, raise_on_failure=False)
        shadow.bindMatches(NavigationButton, self.navigationButtons, raise_on_failure=False)

        # Macro buttons
        shadow.bindMatch(UndoButton, self.undo, raise_on_failure=False)
        shadow.bindMatch(RedoButton, self.redo, raise_on_failure=False)
        shadow.bindMatch(UndoRedoButton, self.undoRedo, raise_on_failure=False)
        shadow.bindMatch(SaveButton, self.save, raise_on_failure=False)
        shadow.bindMatch(QuantizeButton, self.metroButton, raise_on_failure=False)
        shadow.bindMatch(SwitchActiveButton, self.metroButton, raise_on_failure=False)

    @classmethod
    def create(cls, shadow: DeviceShadow) -> 'SpecialPlugin':
        return cls(shadow)

    @staticmethod
    def shouldBeActive() -> bool:
        return True

    def tick(self):
        pass

    @filterButtonLift
    def playButton(self, control: ControlShadowEvent, index: UnsafeIndex, *args: Any) -> bool:
        transport.start()
        return True

    @filterButtonLift
    def stopButton(self, control: ControlShadowEvent, index: UnsafeIndex, *args: Any) -> bool:
        transport.stop()
        return True

    @filterButtonLift
    def recButton(self, control: ControlShadowEvent, index: UnsafeIndex, *args: Any) -> bool:
        transport.record()
        return True

    @filterButtonLift
    def loopButton(self, control: ControlShadowEvent, index: UnsafeIndex, *args: Any) -> bool:
        transport.setLoopMode()
        return True

    @filterButtonLift
    def metroButton(self, control: ControlShadowEvent, index: UnsafeIndex, *args: Any) -> bool:
        transport.globalTransport(110, 1)
        return True

    def nullEvent(self, control: ControlShadowEvent, index: UnsafeIndex, *args: Any) -> bool:
        """Handle NullEvents for which no action should be taken
        """
        return True

    @filterButtonLift
    def navigationButtons(self, control: ControlShadowEvent, index: UnsafeIndex, *args: Any) -> bool:
        c_type = type(control.getControl())
        if c_type == DirectionUp:
            ui.up()
        elif c_type == DirectionDown:
            ui.down()
        elif c_type == DirectionLeft:
            ui.left()
        elif c_type == DirectionRight:
            ui.right()
        elif c_type == DirectionNext:
            ui.next()
        elif c_type == DirectionPrevious:
            ui.previous()
        elif c_type == DirectionSelect:
            ui.enter()
        else:
            return False
        return True

    @filterButtonLift
    def undo(self, control: ControlShadowEvent, index: UnsafeIndex, *args: Any) -> bool:
        general.undoUp()
        return True
    @filterButtonLift
    def redo(self, control: ControlShadowEvent, index: UnsafeIndex, *args: Any) -> bool:
        general.undoDown()
        return True
    @filterButtonLift
    def undoRedo(self, control: ControlShadowEvent, index: UnsafeIndex, *args: Any) -> bool:
        general.undo()
        return True
    @filterButtonLift
    def save(self, control: ControlShadowEvent, index: UnsafeIndex, *args: Any) -> bool:
        transport.globalTransport(92, 1)
        return True
    @filterButtonLift
    def quantize(self, control: ControlShadowEvent, index: UnsafeIndex, *args: Any) -> bool:
        channels.quickQuantize(channels.selectedChannel())
        return True
    @filterButtonLift
    def switchActive(self, control: ControlShadowEvent, index: UnsafeIndex, *args: Any) -> bool:
        c = control.getControl()
        if isinstance(c, SwitchActivePluginButton):
            getContext().active.toggleWindowsPlugins(True)
        elif isinstance(c, SwitchActiveWindowButton):
            getContext().active.toggleWindowsPlugins(False)
        else:
            # Toggle between windows and plugins
            getContext().active.toggleWindowsPlugins()
        return True

ExtensionManager.registerSpecialPlugin(Transport)
