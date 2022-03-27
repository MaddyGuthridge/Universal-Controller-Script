# name=Universal Event Forwarder
# url=https://forum.image-line.com/viewtopic.php?f=1994&t=274277
# receiveFrom=Universal Controller
"""
device_eventforward

This script packages events into a format where they can be distinguished
and forwards the event on to the main controller. It can be used to link
multiple ports of a device together in a way such that overlapping event
IDs can be distinguished. The additional forwarding takes less than 1 ms, so
performance impact is negligible.

Authors:
* Miguel Guthridge

# Specification:

Each event is wrapped by a sysex event that contains the details for the event
as required

* 0xF0 sysex start

* 0x7D non-commercial system exclusive ID (should prevent overlap with any other
  hardware which would be using a registered system exclusive ID)

* [device name] a null-terminated string containing the device name (sans the
  MIDIIN# parts), to allow for the events to be filtered if the universal
  controller is being used for multiple devices

* 0x00 null terminator

* [device number] determined by the device name in FL Studio, which has
  something like MIDIIN# where # is the device number. This allows the script
  to determine what sub-device the message came from, and separate the events
  properly.

* [event category] type of event:
    * standard (0), or
    * sysex (1)

* [event data] data from the event:
    * data2, data1, status if standard event
    * sysex data if sysex event

* 0xF7 event terminator (if standard event)

# Limitations:

* This system may not work correctly on MacOS, as device names could be managed
  differently to Windows (they are determined by OS-specific APIs)
* Current algorithm assumes less than 10 extra MIDIIN# devices
* Doesn't support devices with parentheses in device name
"""

# Add our additional includes to the Python environment
import fl_typing

from typing import TYPE_CHECKING

from common import consts
from common.contextmanager import catchContextResetException
from common.extensionmanager import ExtensionManager
from common.states import WaitingForDevice, ForwardState

from common import log, verbosity
from common import getContext
from common.consts import getVersionString, ASCII_HEADER_ART
from common.util.events import eventToString, isEventForwarded, isEventForwardedHereFrom, forwardEvent, decodeForwardedEvent
from common.util.misc import formatLongTime
from common.types.eventdata import EventData, isEventStandard, isEventSysex
import device


class OverallDevice:
    @catchContextResetException
    def onInit(self) -> None:
        getContext().initialise(WaitingForDevice(ForwardState))

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
        print(f"Universal Event Forwarder: v{getVersionString()}")
        print(ExtensionManager.getInfo())

dev = OverallDevice()

def OnInit():
    dev.onInit()

def OnMidiIn(event):
    print(eventToString(event))
    dev.onMidiIn(event)

def OnIdle():
    dev.onIdle()

def OnRefresh(flags: int):
    dev.onIdle()

def bootstrap():
    dev.bootstrap()

if __name__ == "__main__":
    bootstrap()
