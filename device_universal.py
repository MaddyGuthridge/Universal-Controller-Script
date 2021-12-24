"""device_universal.py

The entrypoint for the universal controller script.
It is responsible for event parsing, forwarding, script initialisation, and
contains a context object used throughout the script.

This entire script is licensed under GPL v3. Refer to the `LICENSE` file for a
full copy.

Author: Miguel Guthridge [hdsq@outlook.com.au]
"""

from bootstrap import getContext, resetContext, catchContextResetException

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
    resetContext("Initial context")

if __name__ == "__main__":
    bootstrap()
    bootstrap()
    bootstrap()
