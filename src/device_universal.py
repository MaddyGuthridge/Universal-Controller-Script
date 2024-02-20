# name=Universal Controller
# url=https://forum.image-line.com/viewtopic.php?f=1994&t=274277
# receiveFrom=Universal Event Forwarder
"""
device_universal

The entrypoint for the universal controller script.
It is responsible for event parsing, forwarding, script initialization, and
contains a context object used throughout the script.

Refer to module `common.consts` for a list of authors for the project

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""
# Disable flake8 on this file: it gets too mad at us
# flake8: noqa

import version_check

# Add our additional includes to the Python environment
import fl_typing

import consts

# Add support for fl_param_checker
from fl_param_checker import idleCallback, pluginParamCheck

# Get context, and context reset wrapper
from common import getContext, catchContextResetException
# Function to allow user to reset context
from common.context_manager import unsafeResetContext as reset
# Import constants and logger
from common import log, verbosity, ExtensionManager
# Import verbosity constants
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
        idleCallback()
        getContext().tick()

    @catchContextResetException
    def bootstrap(self):
        log("bootstrap.initialize", "Load success", verbosity.INFO)
        print(consts.getHeaderArt("Universal Controller Script"))
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
