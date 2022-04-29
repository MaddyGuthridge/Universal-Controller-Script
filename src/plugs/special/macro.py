"""
plugs > special > macro

Contains the definition for the macro plugin

Authors:
* Miguel Guthridge [hdsq@outlook.com.au]
"""

import channels
import general
import transport
from typing import Any

from common.extensionmanager import ExtensionManager
from common import getContext
from common.util.apifixes import UnsafeIndex
from controlsurfaces import (
    ControlShadowEvent,
    UndoButton,
    RedoButton,
    UndoRedoButton,
    SaveButton,
    QuantizeButton,
    SwitchActiveButton,
    SwitchActivePluginButton,
    SwitchActiveWindowButton,
    SwitchActiveToggleButton,
    PauseActiveButton,
)
from devices import DeviceShadow
from plugs import SpecialPlugin
from plugs.eventfilters import filterButtonLift


class Macro(SpecialPlugin):
    """
    The macro plugin handles macro commands.
    """

    def __init__(self, shadow: DeviceShadow) -> None:
        shadow.setMinimal(True)
        super().__init__(shadow, [])
        # Macro buttons
        shadow.bindMatch(UndoButton, self.undo, raise_on_failure=False)
        shadow.bindMatch(RedoButton, self.redo, raise_on_failure=False)
        shadow.bindMatch(UndoRedoButton, self.undoRedo, raise_on_failure=False)
        shadow.bindMatch(SaveButton, self.save, raise_on_failure=False)
        shadow.bindMatch(QuantizeButton, self.quantize,
                         raise_on_failure=False)
        shadow.bindMatches(
            SwitchActiveButton,
            self.switchActive,
            raise_on_failure=False,
            one_type=False,
        )
        shadow.bindMatches(
            PauseActiveButton,
            self.pauseActive,
            raise_on_failure=False,
            one_type=False,
        )

    @classmethod
    def create(cls, shadow: DeviceShadow) -> 'SpecialPlugin':
        return cls(shadow)

    @staticmethod
    def shouldBeActive() -> bool:
        return True

    def tick(self):
        pass

    @filterButtonLift
    def undo(
        self,
        control: ControlShadowEvent,
        index: UnsafeIndex,
        *args: Any
    ) -> bool:
        general.undoUp()
        return True

    @filterButtonLift
    def redo(
        self,
        control: ControlShadowEvent,
        index: UnsafeIndex,
        *args: Any
    ) -> bool:
        general.undoDown()
        return True

    @filterButtonLift
    def undoRedo(
        self,
        control: ControlShadowEvent,
        index: UnsafeIndex,
        *args: Any
    ) -> bool:
        general.undo()
        return True

    @filterButtonLift
    def save(
        self,
        control: ControlShadowEvent,
        index: UnsafeIndex,
        *args: Any
    ) -> bool:
        transport.globalTransport(92, 1)
        return True

    @filterButtonLift
    def quantize(
        self,
        control: ControlShadowEvent,
        index: UnsafeIndex,
        *args: Any
    ) -> bool:
        channels.quickQuantize(channels.selectedChannel())
        return True

    @filterButtonLift
    def switchActive(
        self,
        control: ControlShadowEvent,
        index: UnsafeIndex,
        *args: Any
    ) -> bool:
        c = control.getControl()
        if isinstance(c, SwitchActivePluginButton):
            getContext().active.toggleWindowsPlugins(True)
        elif isinstance(c, SwitchActiveWindowButton):
            getContext().active.toggleWindowsPlugins(False)
        elif isinstance(c, SwitchActiveToggleButton):
            # Toggle between windows and plugins
            getContext().active.toggleWindowsPlugins()
        return True

    @filterButtonLift
    def pauseActive(
        self,
        control: ControlShadowEvent,
        index: UnsafeIndex,
        *args: Any
    ) -> bool:
        # TODO: If there's enough demand, potentially add support for a direct
        # controls as well as just a toggle
        getContext().active.playPause()
        return True


ExtensionManager.registerSpecialPlugin(Macro)
