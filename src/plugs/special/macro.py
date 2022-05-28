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

from common.extension_manager import ExtensionManager
from common import getContext
from common.util.api_fixes import UnsafeIndex
from control_surfaces import (
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
    CaptureMidiButton,
)
from devices import DeviceShadow
from plugs import SpecialPlugin
from plugs.event_filters import filterButtonLift


class Macro(SpecialPlugin):
    """
    The macro plugin handles macro commands.
    """

    def __init__(self, shadow: DeviceShadow) -> None:
        shadow.setMinimal(True)
        super().__init__(shadow, [])
        # Macro buttons
        shadow.bindMatch(UndoButton, self.undo)
        shadow.bindMatch(RedoButton, self.redo)
        shadow.bindMatch(UndoRedoButton, self.undoRedo)
        shadow.bindMatch(SaveButton, self.save)
        shadow.bindMatch(QuantizeButton, self.quantize)
        shadow.bindMatch(CaptureMidiButton, self.captureMidi)
        shadow.bindMatches(
            SwitchActiveButton,
            self.switchActive,
            one_type=False,
        )
        shadow.bindMatches(
            PauseActiveButton,
            self.pauseActive,
            one_type=False,
        )

    @classmethod
    def create(cls, shadow: DeviceShadow) -> 'SpecialPlugin':
        return cls(shadow)

    @classmethod
    def shouldBeActive(cls) -> bool:
        return True

    @filterButtonLift()
    def undo(
        self,
        control: ControlShadowEvent,
        index: UnsafeIndex,
        *args: Any
    ) -> bool:
        general.undoUp()
        return True

    @filterButtonLift()
    def redo(
        self,
        control: ControlShadowEvent,
        index: UnsafeIndex,
        *args: Any
    ) -> bool:
        general.undoDown()
        return True

    @filterButtonLift()
    def undoRedo(
        self,
        control: ControlShadowEvent,
        index: UnsafeIndex,
        *args: Any
    ) -> bool:
        general.undo()
        return True

    @filterButtonLift()
    def save(
        self,
        control: ControlShadowEvent,
        index: UnsafeIndex,
        *args: Any
    ) -> bool:
        transport.globalTransport(92, 1)
        return True

    @filterButtonLift()
    def quantize(
        self,
        control: ControlShadowEvent,
        index: UnsafeIndex,
        *args: Any
    ) -> bool:
        channels.quickQuantize(channels.selectedChannel())
        return True

    @filterButtonLift()
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

    @filterButtonLift()
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

    @filterButtonLift()
    def captureMidi(
        self,
        control: ControlShadowEvent,
        index: UnsafeIndex,
        *args: Any
    ) -> bool:
        # Find out how much length to write
        time = \
            getContext().settings.get("plugins.general.score_log_dump_length")
        general.dumpScoreLog(time, 0)
        return True


ExtensionManager.special.register(Macro)
