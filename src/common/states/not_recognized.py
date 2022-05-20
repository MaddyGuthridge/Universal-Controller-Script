"""
common > states > not_recognized

The state for when the script failed to recognize the connected device.
"""
import ui
from common import log, verbosity, consts
from common.types import EventData
from common.util.events import eventToString
from . import IScriptState


class DeviceNotRecognized(IScriptState):
    """
    State for when device isn't recognized
    """

    def initialize(self) -> None:
        log(
            "bootstrap.device.type_detect",
            "Failed to recognize device",
            verbosity.ERROR,
            "The device was unable to be recognized. This usually means that "
            "there is no definition available for your device. You could "
            "help by contributing a device definition. Visit the GitHub page "
            "for details: " + consts.WEBSITE)
        ui.setHintMsg("Failed to recognize device")

    def deinitialize(self) -> None:
        pass

    def tick(self) -> None:
        ui.setHintMsg("Failed to recognize device")

    def processEvent(self, event: EventData) -> None:
        log(
            "bootstrap.device.type_detect",
            f"Received event: {eventToString(event)}"
        )
