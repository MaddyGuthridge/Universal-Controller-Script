"""
common > contextmanager

Contains the DeviceContextManager class, used to manage the state of the
script, allowing for soft resets of the script when required.

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]
"""

__all__ = [
    'catchContextResetException',
    'getContext',
    'resetContext',
    'unsafeResetContext'
]

from .profiler import profilerDecoration
from . import logger
from typing import NoReturn, Optional, Callable, TYPE_CHECKING
from time import time_ns

from .settings import Settings
from .activitystate import ActivityState

from .util.apifixes import catchUnsafeOperation
from .util.misc import NoneNoPrintout
from .util.events import isEventForwarded, isEventForwardedHere
from .types import EventData
from .profiler import ProfilerManager

from .states import (
    IScriptState,
    StateChangeException,
    catchStateChangeException,
)

if TYPE_CHECKING:
    from devices import Device


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
        self.state: Optional[IScriptState] = None
        if self.settings.get("debug.profiling"):
            trace = self.settings.get("debug.exec_tracing")
            self.profiler: Optional[ProfilerManager] = ProfilerManager(trace)
        else:
            self.profiler = None
        # Time the device last ticked at
        self._last_tick = time_ns()
        self._ticks = 0
        self._dropped_ticks = 0
        self._device: Optional['Device'] = None

    @catchStateChangeException
    @profilerDecoration("initialise")
    def initialise(self, state: IScriptState) -> None:
        """Initialise the controller associated with this context manager.

        ### Args:
        * `state` (`IScriptState`): state to initialise with
        """
        self.state = state
        state.initialise()

    @catchStateChangeException
    @profilerDecoration("deinitialise")
    def deinitialise(self) -> None:
        """Deinitialise the controller when FL Studio closes or begins a render
        """
        if self._device is not None:
            self._device.deinitialise()
            self._device = None
        if self.state is not None:
            self.state.deinitialise()
            self.state = None

    @catchUnsafeOperation
    @catchStateChangeException
    @profilerDecoration("processEvent")
    def processEvent(self, event: EventData) -> None:
        """Process a MIDI event

        ### Args:
        * `event` (`event`): event to process
        """
        # Filter out events that shouldn't be forwarded here
        if isEventForwarded(event) and not isEventForwardedHere(event):
            event.handled = True
            return
        if self.state is None:
            raise MissingContextException("State not set")
        self.state.processEvent(event)

    @catchUnsafeOperation
    @catchStateChangeException
    @profilerDecoration("tick")
    def tick(self) -> None:
        """
        Called frequently to allow any required updates to the controller
        """
        if self.state is None:
            raise MissingContextException("State not set")
        # Update number of ticks
        self._ticks += 1
        # If the last tick was over 60 ms ago, then our script is getting laggy
        # Skip this tick to compensate
        last_tick = self._last_tick
        self._last_tick = time_ns()
        if (self._last_tick - last_tick) / 1_000_000 > 60:
            self._dropped_ticks += 1
            return
        # Tick active plugin
        self.active.tick()
        # The tick the current script state
        self.state.tick()

    def getTickNumber(self) -> int:
        """
        Returns the tick number of the script

        This is the number of times the script has been ticked

        ### Returns:
        * `int`: tick number
        """
        return self._ticks

    def getDroppedTicks(self) -> str:
        """
        Returns the number of ticks dropped by the controller

        This is a good indicator of script performance

        ### Returns:
        * `str`: info on dropped ticks
        """
        percent = int(self._dropped_ticks / self._ticks * 100)
        return f"{self._dropped_ticks} dropped ticks ({percent}%)"

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

    def registerDevice(self, dev: 'Device'):
        """
        Register a recognised device

        ### Args:
        * `dev` (`Device`): device number
        """
        self._device = dev

    def getDevice(self) -> 'Device':
        """
        Return a reference to the recognised device

        This is used so that forwarded events can be encoded correctly

        ### Raises:
        * `ValueError`: device not set

        ### Returns:
        * `Device`: device
        """
        if self._device is None:
            raise ValueError("Device not set")
        return self._device


class ContextResetException(Exception):
    """
    Raised when the context is reset, so as to prevent any other operations
    using the old context from succeeding
    """


class MissingContextException(Exception):
    """
    Raised when the context hasn't been initialised yet
    """


def catchContextResetException(func: Callable) -> Callable:
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


def resetContext(reason: str = "none") -> NoReturn:
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
def unsafeResetContext(reason: str = "none") -> None:
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


_initContext()
