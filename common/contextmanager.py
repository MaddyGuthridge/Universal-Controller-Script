"""
common > contextmanager

Contains the DeviceContextManager class, used to manage the state of the script,
allowing for soft resets of the script when required.

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]
"""

__all__ = [
    'catchContextResetException',
    'getContext',
    'resetContext'
]

from typing import NoReturn, Optional, Callable

from .settings import Settings
from .activitystate import ActivityState

from .util.misc import NoneNoPrintout
from .util.events import isEventForwarded, isEventForwardedHere
from .types import EventData

from .states import (
    IScriptState,
    StateChangeException,
    catchStateChangeException,
)

class DeviceContextManager:
    """Defines the context for the entire script, which allows the modular
    components of script to be dynamically refreshed and reloaded, as well as
    be reset to the default start-up state if required.
    
    It is gettable from any location by using the getContext() method
    """
    
    def __init__(self) -> None:
        """Initialise the context manager, including reloading any required
        modules
        """
        self.settings = Settings()
        self.active = ActivityState()
        # Set the state of the script to wait for the device to be recognised
        self.state: IScriptState = WaitingForDevice()
    
    @catchStateChangeException
    def initialise(self) -> None:
        """Initialise the controller associated with this context manager.
        """
        self.state.initialise()

    @catchStateChangeException
    def processEvent(self, event: EventData) -> None:
        """Process a MIDI event

        ### Args:
        * `event` (`event`): event to process
        """
        # Filter out events that shouldn't be forwarded here
        if isEventForwarded(event) and not isEventForwardedHere(event):
            event.handled = True
            return
        self.state.processEvent(event)
    
    @catchStateChangeException
    def tick(self) -> None:
        """
        Called frequently to allow any required updates to the controller
        """
        self.state.tick()
        self.active.tick()
    
    def setState(self, new_state: IScriptState) -> NoReturn:
        """
        Set the state of the script to a new state

        This is used to transfer between different states

        ### Args:
        * `new_state` (`IScriptState`): state to switch to
        
        ### Raises:
        * `StateChangeException`: state changed successfully
        """
        self.state = new_state
        new_state.initialise()
        raise StateChangeException("State changed")

class ContextResetException(Exception):
    """
    Raised when the context is reset, so as to prevent any other operations
    using the old context from succeeding
    """

class MissingContextException(Exception):
    """
    Raised when the context hasn't been initialised yet
    """

def catchContextResetException(func: Callable)-> Callable:
    """A decorator for catching ContextResetExceptions so that the program
    continues normally

    ### Args:
    * `func` (`Callable`): function to decorate

    ### Returns:
    * `Callable`: decorated function
    """
    def wrapper(*args, **kwargs):
        try:
            ret = func(*args, **kwargs)
            if ret is None:
                return NoneNoPrintout
        except ContextResetException:
            return NoneNoPrintout
    return wrapper

# The context manager's instance
# This should be the only non-constant global variable in the entire program,
# except for the log
_context: Optional[DeviceContextManager] = None

def getContext() -> DeviceContextManager:
    """Returns a reference to the device context

    ### Raises:
    * `Exception`: when the context is `None`, indicating that it wasn't
      initialised

    ### Returns:
    * `DeviceContextManager`: context
    """
    if _context is None:
        raise Exception("Context isn't initialised")
    
    return _context

def resetContext(reason:str="none") -> NoReturn:
    """Resets the context of the script to the default, before raising a
    ContextResetException to halt the current event

    ### Args:
    * `reason` (`str`, optional): reason for resetting. Defaults to "none".

    ### Raises:
    * `ContextResetException`: halt the event's processing
    """
    global _context
    logger.log(
        "bootstrap.context.reset",
        f"Device context reset with reason: {reason}",
        logger.verbosity.WARNING)
    _context = DeviceContextManager()
    raise ContextResetException(reason)

@catchContextResetException
def unsafeResetContext(reason:str="none") -> None:
    """
    Reset the context of the script to the default, without raising a
    ContextResetException to halt the current event.

    WARNING: Calling this inside the main components of the script is a very
    bad idea, as your code will interact with a context it isn't prepared for,
    leading to undefined behaviour. This should only ever be called by the user
    through the console.

    ### Args:
    * `reason` (`str`, optional): Reason for reset. Defaults to `"none"`.
    """
    resetContext(reason)

def _initContext() -> None:
    """
    Initialises the context manager for the script
    """
    global _context
    _context = DeviceContextManager()

from . import logger
from .states import WaitingForDevice

_initContext()
