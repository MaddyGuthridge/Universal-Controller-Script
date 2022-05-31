"""
plugs > special > macro

Contains the definition for the macro plugin

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""

import channels
import general
import transport
from typing import Any

from common.extension_manager import ExtensionManager
from common import getContext
from common.types import Color
from common.util.api_fixes import getUndoPosition
from control_surfaces import (
    ControlShadowEvent,
    ControlShadow,
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


ENABLED = Color.fromGrayscale(0.7)
DISABLED = Color.fromGrayscale(0.3, False)


class Macro(SpecialPlugin):
    """
    The macro plugin handles macro commands.
    """

    def __init__(self, shadow: DeviceShadow) -> None:
        shadow.setMinimal(True)
        super().__init__(shadow, [])
        # Macro buttons
        shadow.bindMatch(UndoButton, self.eUndo, self.tUndo)
        shadow.bindMatch(RedoButton, self.eRedo, self.tRedo)
        shadow.bindMatch(UndoRedoButton, self.eUndoRedo).colorize(ENABLED)
        shadow.bindMatch(SaveButton, self.eSave, self.tSave)
        shadow.bindMatch(QuantizeButton, self.eQuantize).colorize(ENABLED)
        shadow.bindMatch(CaptureMidiButton, self.eCaptureMidi)\
            .colorize(ENABLED)
        shadow.bindMatches(
            SwitchActiveButton,
            self.eSwitchActive,
            self.tSwitchActive,
            one_type=False,
        )
        shadow.bindMatch(
            PauseActiveButton,
            self.ePauseActive,
            self.tPauseActive,
        )

    @classmethod
    def create(cls, shadow: DeviceShadow) -> 'SpecialPlugin':
        return cls(shadow)

    @classmethod
    def shouldBeActive(cls) -> bool:
        return True

    @filterButtonLift()
    def eUndo(
        self,
        control: ControlShadowEvent,
        *args: Any
    ) -> bool:
        general.undoUp()
        return True

    def tUndo(self, control: ControlShadow, *args: Any):
        pos, num = getUndoPosition()
        if pos == num - 1:
            # Nothing to undo
            control.color = DISABLED
        else:
            control.color = ENABLED

    @filterButtonLift()
    def eRedo(
        self,
        control: ControlShadowEvent,
        *args: Any
    ) -> bool:
        general.undoDown()
        return True

    def tRedo(self, control: ControlShadow, *args: Any):
        pos = general.getUndoHistoryLast()
        if pos == 0:
            # Nothing to redo
            control.color = DISABLED
        else:
            control.color = ENABLED

    @filterButtonLift()
    def eUndoRedo(
        self,
        control: ControlShadowEvent,
        *args: Any
    ) -> bool:
        general.undo()
        return True

    @filterButtonLift()
    def eSave(
        self,
        control: ControlShadowEvent,
        *args: Any
    ) -> bool:
        transport.globalTransport(92, 1)
        return True

    def tSave(
        self,
        control: ControlShadow,
        *args,
    ):
        if general.getChangedFlag():
            control.color = ENABLED
        else:
            control.color = DISABLED

    @filterButtonLift()
    def eQuantize(
        self,
        control: ControlShadowEvent,
        *args: Any
    ) -> bool:
        channels.quickQuantize(channels.selectedChannel())
        return True

    @filterButtonLift()
    def eSwitchActive(
        self,
        control: ControlShadowEvent,
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

    def tSwitchActive(
        self,
        control: ControlShadow,
        *args: Any
    ) -> bool:
        c = control.getControl()
        if isinstance(c, SwitchActivePluginButton):
            if getContext().active.isPlugActive():
                control.color = ENABLED
            else:
                control.color = DISABLED
        elif isinstance(c, SwitchActiveWindowButton):
            if not getContext().active.isPlugActive():
                control.color = ENABLED
            else:
                control.color = DISABLED
        elif isinstance(c, SwitchActiveToggleButton):
            control.color = ENABLED
        return True

    @filterButtonLift()
    def ePauseActive(
        self,
        control: ControlShadowEvent,
        *args: Any
    ) -> bool:
        # TODO: If there's enough demand, potentially add support for a direct
        # controls as well as just a toggle
        getContext().active.playPause()
        return True

    def tPauseActive(
        self,
        control: ControlShadow,
        *args,
    ):
        if getContext().active.isUpdating():
            control.color = DISABLED
        else:
            control.color = ENABLED

    @filterButtonLift()
    def eCaptureMidi(
        self,
        control: ControlShadowEvent,
        *args: Any
    ) -> bool:
        # Find out how much length to write
        time = \
            getContext().settings.get("plugins.general.score_log_dump_length")
        general.dumpScoreLog(time, 0)
        return True


ExtensionManager.special.register(Macro)
