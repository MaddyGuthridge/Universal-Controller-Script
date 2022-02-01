# name=Universal Controller
# url=https://github.com/MiguelGuthridge/Universal-Controller-Script
# receiveFrom=Universal Event Forwarder
"""device_universal.py

The entrypoint for the universal controller script.
It is responsible for event parsing, forwarding, script initialisation, and
contains a context object used throughout the script.

This entire script is licensed under GPL v3. Refer to the `LICENSE` file for a
full copy.

Refer to module `common.consts` for a list of authors for the project
"""

# Add our additional includes to the Python environment
import include

# Get context, and context reset wrapper
from common import getContext, catchContextResetException
# Function to allow user to reset context
from common.contextmanager import unsafeResetContext as reset
# Import constants and logger
from common import consts, log, verbosity, ExtensionManager

# Import console helpers
from common.util.consolehelpers import *

class OverallDevice:
    @catchContextResetException
    def onInit(self) -> None:
        getContext().initialise()

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
        print(ExtensionManager.getInfo())
        print("Type `help` for help using the script\n")

device = OverallDevice()

def OnInit():
    device.onInit()

def OnMidiIn(event):
    device.onMidiIn(event)

idle_uncalled = True
def OnIdle():
    global idle_uncalled
    if idle_uncalled:
        log("device.idle", "OnIdle() called", verbosity.INFO)
        idle_uncalled = False
    device.onIdle()

def OnRefresh(flags: int):
    device.onIdle()

def bootstrap():
    device.bootstrap()

if __name__ == "__main__":
    bootstrap()
