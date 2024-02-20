"""
integrations > window > piano_roll

Integration for FL Studio's piano roll

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""
import transport
import ui
from common.extension_manager import ExtensionManager
from common.plug_indexes import WindowIndex
from common.types import Color
from devices import DeviceShadow
from integrations import WindowIntegration
from integrations.event_filters import filterButtonLift
from control_surfaces import ToolSelector, ControlShadowEvent


# TODO: Annotate tool names, like in playlist
TOOL_COLORS = [
    Color.fromInteger(0xffc43f),  # Pencil
    Color.fromInteger(0x7bcefd),  # Paint
    Color.fromInteger(0xad90fe),  # Paint drums
    Color.fromInteger(0xfe5750),  # Delete
    Color.fromInteger(0xff54b0),  # Mute
    Color.fromInteger(0x85b3f2),  # Slice
    Color.fromInteger(0xff9354),  # Select
    Color.fromInteger(0x80acff),  # Zoom
    # Color.fromInteger(0xffa64a),  # Preview
]


class PianoRoll(WindowIntegration):
    """
    Used to process events directed at the piano-roll

    Currently empty: will expand in the future
    """

    def __init__(self, shadow: DeviceShadow) -> None:
        shadow.bindMatches(
            ToolSelector,
            self.eSelectTool,
            args_generator=...,
            target_num=len(TOOL_COLORS),
        )\
            .colorize(TOOL_COLORS)
        super().__init__(shadow)

    @classmethod
    def getWindowId(cls) -> WindowIndex:
        return WindowIndex.PIANO_ROLL

    @classmethod
    def create(cls, shadow: DeviceShadow) -> 'WindowIntegration':
        return cls(shadow)

    @filterButtonLift()
    def eSelectTool(
        self,
        control: ControlShadowEvent,
        window,
        idx: int,
    ) -> bool:
        # FIXME: This uses keyboard shortcuts which are extremely unreliable
        if idx < len(TOOL_COLORS):
            # If we're already in a menu, close it
            if ui.isInPopupMenu():
                ui.closeActivePopupMenu()
            # Open menu
            transport.globalTransport(90, 1)
            # Navigate to tool selection
            ui.left()
            ui.left()
            # Move down until we reach the required tool
            for _ in range(idx):
                ui.down()
            # Select it
            ui.enter()
        return True


ExtensionManager.windows.register(PianoRoll)
