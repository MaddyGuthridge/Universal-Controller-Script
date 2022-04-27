
import ui
from common import log, verbosity, consts
from common.types import EventData
from common.util.events import eventToString
from . import IScriptState


class DeviceNotRecognised(IScriptState):
    """
    State for when device isn't recognised
    """

    def initialise(self) -> None:
        log(
            "bootstrap.device.type_detect",
            "Failed to recognise device",
            verbosity.ERROR,
            "The device was unable to be recognised. This usually means that "
            "there is no definition available for your device. You could "
            "help by contributing a device definition. Visit the GitHub page "
            "for details: " + consts.WEBSITE)
        ui.setHintMsg("Failed to recognise device")

    def deinitialise(self) -> None:
        pass

    def tick(self) -> None:
        ui.setHintMsg("Failed to recognise device")

    def processEvent(self, event: EventData) -> None:
        log(
            "bootstrap.device.type_detect",
            f"Received event: {eventToString(event)}"
        )
