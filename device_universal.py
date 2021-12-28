"""device_universal.py

The entrypoint for the universal controller script.
It is responsible for event parsing, forwarding, script initialisation, and
contains a context object used throughout the script.

This entire script is licensed under GPL v3. Refer to the `LICENSE` file for a
full copy.

Refer to module `common.consts` for a list of authors for the project
"""

# Get context, and context reset wrapper
from common import getContext, catchContextResetException
# Function to allow user to reset context
from common.contextmanager import unsafeResetContext as reset

# Import console helpers
from common.util.consolehelpers import *

from logger import verbosity

@catchContextResetException
def onInit() -> None:
    getContext().initialise()
    
@catchContextResetException
def onMidiIn(event) -> None:
    # TODO: Parse event and stuff
    getContext().processEvent(event)

@catchContextResetException
def onIdle() -> None:
    getContext().tick()

@catchContextResetException
def bootstrap():
    # resetContext("Initial context")
    pass

if __name__ == "__main__":
    bootstrap()
