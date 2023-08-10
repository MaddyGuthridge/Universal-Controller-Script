# name=Universal Event Forwarder
# url=https://forum.image-line.com/viewtopic.php?f=1994&t=274277
# receiveFrom=Universal Controller
"""
device_event_forward

This script packages events into a format where they can be distinguished
and forwards the event on to the main controller. It can be used to link
multiple ports of a device together in a way such that overlapping event
IDs can be distinguished. The additional forwarding takes less than 1 ms, so
performance impact is negligible.

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""
# flake8: noqa

import version_check

# Add our additional includes to the Python environment
import fl_typing

import consts

# Add support for fl_param_checker
from fl_param_checker import idleCallback, pluginParamCheck

from common.context_manager import catchContextResetException
from common.extension_manager import ExtensionManager
from common.states import WaitingForDevice, ForwardState

from common import log, verbosity
from common import getContext

# Import console helpers
from common.util.console_helpers import *


class OverallDevice:
    @catchContextResetException
    def onInit(self) -> None:
        getContext().initialize(WaitingForDevice(ForwardState))

    @catchContextResetException
    def onMidiIn(self, event) -> None:
        getContext().processEvent(event)

    @catchContextResetException
    def onIdle(self) -> None:
        getContext().tick()

    @catchContextResetException
    def bootstrap(self):
        log("bootstrap.initialize", "Load success", verbosity.INFO)
        print(consts.getHeaderArt("Universal Event Forwarder"))
        print("Type `help` for help using the script\n")

dev = OverallDevice()

def OnInit():
    dev.onInit()

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
