# name=Universal Controller
# url=https://forum.image-line.com/viewtopic.php?f=1994&t=274277
# receiveFrom=Universal Event Forwarder
"""device_universal.py

The entrypoint for the universal controller script.
It is responsible for event parsing, forwarding, script initialisation, and
contains a context object used throughout the script.

This entire script is licensed under GPL v3. Refer to the `LICENSE` file for a
full copy.

Refer to module `common.consts` for a list of authors for the project
"""
# flake8: noqa

# Add our additional includes to the Python environment
import fl_typing

# Get context, and context reset wrapper
from common import getContext, catchContextResetException, getVersionString
# Function to allow user to reset context
from common.context_manager import unsafeResetContext as reset
# Import constants and logger
from common import consts, log, verbosity, ExtensionManager
# Import verbosities
from common.logger.verbosity import *
# Import some helper functions
from common.util.events import eventToString
# Import first state
from common.states import WaitingForDevice, MainState

# Import console helpers
from common.util.console_helpers import *


class OverallDevice:
    @catchContextResetException
    def onInit(self) -> None:
        getContext().initialize(WaitingForDevice(MainState))

    @catchContextResetException
    def onDeinit(self) -> None:
        getContext().deinitialize()

    @catchContextResetException
    def onMidiIn(self, event) -> None:
        getContext().processEvent(event)

    @catchContextResetException
    def onIdle(self) -> None:
        getContext().tick()

    @catchContextResetException
    def bootstrap(self):
        log("bootstrap.initialize", "Load success", verbosity.INFO)
        print(consts.ASCII_HEADER_ART)
        print(f"Universal Controller Script: v{getVersionString()}")
        print(ExtensionManager.getBasicInfo())
        print("Type `help` for help using the script\n")


dev = OverallDevice()


def OnInit():
    dev.onInit()


def OnDeInit():
    dev.onDeinit()


def OnMidiIn(event):
    dev.onMidiIn(event)


def OnIdle():
    dev.onIdle()


def OnRefresh(flags: int):
    dev.onIdle()


def bootstrap():
    dev.bootstrap()


if __name__ == "__main__":
    bootstrap()
