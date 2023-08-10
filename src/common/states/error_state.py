"""
common > states > not_recognized

The state for when the script failed to recognize the connected device.

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""
import ui
import consts
from common import log, verbosity
from fl_classes import FlMidiMsg
from common.exceptions import (
    UcsError,
    DeviceRecognizeError,
    DeviceInitializeError,
    EventInspectError,
    EventEncodeError,
    EventDecodeError,
    EventDispatchError,
    InvalidConfigError,
)
from common.util.events import eventToString
from . import IScriptState


ERROR_MAPPINGS: dict[type[Exception], dict] = {
    DeviceRecognizeError: {
        "category": "bootstrap.device.type_detect",
        "msg": "Failed to recognize device",
        "verbosity": verbosity.CRITICAL,
        "detailed_msg": (
            f"The device was unable to be recognized. This usually means that "
            f"there is no definition available for your device, if you're "
            f"sure there is one, make sure you contact the maintainer for "
            f"device on the Discord server, or open an issue on the GitHub. "
            f"If there is no definition available, you could help by "
            f"contributing one. Visit the GitHub page for details: "
            f"{consts.WEBSITE}"
        )
    },
    DeviceInitializeError: {
        "category": "bootstrap.device.initialize",
        "msg": "Failed to initialize device",
        "verbosity": verbosity.CRITICAL,
        "detailed_msg": (
            f"The device was unable to be initialized. This is likely a bug "
            f"with the script. Please create an issue on GitHub by visiting "
            f"{consts.ISSUES_PAGE}, or join the Discord server and ask for "
            f"help at {consts.DISCORD}"
        )
    },
    EventDispatchError: {
        "category": "device.forward.out",
        "msg": "Failed to dispatch event",
        "verbosity": verbosity.CRITICAL,
        "detailed_msg": (
            f"The script was unable to dispatch an event to the second port "
            f"of this device. This usually means that you haven't assigned "
            f"the second port of your device to the Universal Event Forwarder "
            f"script. For more details, see the troubleshooting section in "
            f"project's documentation ({consts.DOCUMENTATION})."
        )
    },
    EventEncodeError: {
        "category": "device.forward.out",
        "msg": "Failed to encode event",
        "verbosity": verbosity.CRITICAL,
        "detailed_msg": (
            f"An error occurred while forwarding an event. Please open an "
            f"issue on the project's GitHub page ({consts.ISSUES_PAGE})."
        )
    },
    EventDecodeError: {
        "category": "device.forward.in",
        "msg": "Failed to decode event",
        "verbosity": verbosity.CRITICAL,
        "detailed_msg": (
            f"An error occurred while decoding a forwarded event. Please open "
            f"an issue on the project's GitHub page ({consts.ISSUES_PAGE})."
        )
    },
    EventInspectError: {
        "category": "device.forward",
        "msg": "Failed to inspect event",
        "verbosity": verbosity.CRITICAL,
        "detailed_msg": (
            f"An error occurred while inspecting a forwarded an event. Please "
            f"open an issue on the project's GitHub page "
            f"({consts.ISSUES_PAGE})."
        )
    },
    InvalidConfigError: {
        "category": "bootstrap.initialize",
        "msg": "Failed to load custom settings",
        "verbosity": verbosity.CRITICAL,
        "detailed_msg": (
            "An error occurred when loading the script's configuration file. "
            "This usually means that you've entered invalid options, or have "
            "a syntax error in your configuration file."
        )
    },
}

DEFAULT_ERROR = {
    "category": "general",
    "msg": "An unknown error occurred",
    "verbosity": verbosity.CRITICAL,
    "detailed_msg": (
        f"Something went wrong and the script crashed. Please create a "
        f"bug report by notifying a developer on the Discord server, or "
        f"opening an issue on the project's GitHub page at "
        f"{consts.ISSUES_PAGE}."
    )
}


class ErrorState(IScriptState):
    """
    State for when a critical error occurred
    """
    def __init__(self, error: UcsError) -> None:
        self.__exception = error

    def initialize(self) -> None:
        error_info = ERROR_MAPPINGS.get(type(self.__exception), DEFAULT_ERROR)
        log(**error_info)
        log(
            "general",
            f"Error details: {repr(self.__exception)}",
            verbosity.CRITICAL,
        )
        if self.__exception.__cause__ is not None:
            log(
                "general",
                f"Error caused by: {repr(self.__exception.__cause__)}",
                verbosity.CRITICAL,
            )
        ui.setHintMsg("[UCS] error: see script output")
        # raise self.__exception

    def deinitialize(self) -> None:
        pass

    def tick(self) -> None:
        # ui.setHintMsg("[UCS] error: see script output")
        pass

    def processEvent(self, event: FlMidiMsg) -> None:
        log(
            "bootstrap.device.type_detect",
            f"Received event: {eventToString(event)}"
        )
