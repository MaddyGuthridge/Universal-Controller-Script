# name=Universal Event Forwarder
# url=https://github.com/MiguelGuthridge/Universal-Controller-Script
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

import include
import time
from typing import TYPE_CHECKING
from common import log, verbosity
from common.consts import getVersionString, ASCII_HEADER_ART
from common.util.events import bytesToString, eventToString
from common.util.misc import formatLongTime
from common.types import eventData
import device

EVENT_HEADER: bytes = bytes()

def raiseIncompatibleDevice():
    raise TypeError("This script should be used to forward extra device "
                        "port events to the primary device port. This isn't a "
                        "device port.")

def OnMidiIn(event: eventData):
    
    if event.sysex is None:
        if TYPE_CHECKING:
            assert event.data2 is not None
            assert event.data1 is not None
            assert event.status is not None
        output = EVENT_HEADER + bytes([0]) + bytes([
            event.data2,
            event.data1,
            event.status,
            0xF7
        ])
    else:
        output = EVENT_HEADER + bytes([1]) + bytes(event.sysex)
    
    # print("Output sysex event:")
    # print(bytesToString(output))

    # Dispatch to all available devices
    for i in range(device.dispatchReceiverCount()):
        device.dispatch(i, 0xF0, output)
    
    log(
        "device.forward.out",
        "Dispatched event to main script: " + eventToString(event)
    )
    event.handled = True

def OnInit():
    global EVENT_HEADER
    # Determine device name and number
    name = device.getName()
    
    if not name.startswith("MIDIIN"):
        raiseIncompatibleDevice()
    name = name.lstrip("MIDIIN")
    bracket_start = name.find("(")
    if bracket_start == 0:
        raiseIncompatibleDevice()
    try:
        dev_num = int(name[0:bracket_start])
    except ValueError:
        raiseIncompatibleDevice()
    
    name = name[bracket_start+1:-1]
    
    EVENT_HEADER = bytes([
        0xF0, # Start sysex
        0x7D  # Non-commercial sysex ID
    ]) + name.encode() \
       + bytes([0]) \
       + bytes([dev_num])
    
    log(
        "device.forward.bootstrap",
        "Generated event header",
        detailed_msg=f"{bytesToString(EVENT_HEADER)}\n"
                     f"{dev_num=}"
    )

log(
    "device.forward.bootstrap",
    "Loaded script successfully"
)

print(ASCII_HEADER_ART)
print(f"Universal Event Forwarder: v{getVersionString()}")
