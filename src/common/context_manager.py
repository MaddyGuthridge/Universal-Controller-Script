"""
common > context_manager

Contains the DeviceContextManager class, used to manage the state of the
script, allowing for soft resets of the script when required.

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
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
from fl_classes import FlMidiMsg

from .settings import Settings
from .activity_state import ActivityState
from .exceptions import UcsError
from .util.api_fixes import catchUnsafeOperation
from .util.misc import NoneNoPrintout
from .util.events import isEventForwarded, isEventForwardedHere
from .util.catch_exception_decorator import catchExceptionDecorator
from .profiler import ProfilerManager

from .states import (
    IScriptState,
    ErrorState,
    StateChangeException,
)

if TYPE_CHECKING:
    from devices import Device


def toErrorState(err: UcsError):
    getContext().setState(ErrorState(err))


class DeviceContextManager:
    """Defines the context for the entire script, which allows the modular
    components of script to be dynamically refreshed and reloaded, as well as
    be reset to the default start-up state if required.

    It is gettable from any location by using the getContext() method
    """

    def __init__(self) -> None:
        """Initialize the context manager, including reloading any required
        modules
        """
        self.settings = Settings()
        self.activity = ActivityState()
        # Set the state of the script to wait for the device to be recognized
        self.state: Optional[IScriptState] = None
        if self.settings.get("debug.profiling"):
            trace = self.settings.get("debug.exec_tracing")
            self.profiler: Optional[ProfilerManager] = ProfilerManager(trace)
        else:
            self.profiler = None
        # Time the script last ticked at
        self._last_tick = time_ns()
        self._ticks = 0
        self._dropped_ticks = 0
        self._slow_ticks = 0
        self._device: Optional['Device'] = None

    def enableProfiler(self, trace: bool = False) -> None:
        """
        Enable the performance profiler

        ### Args:
        * `trace` (`bool`, optional): Whether to print traces. Defaults to
          `False`.
        """
        self.profiler = ProfilerManager(trace)

    @catchExceptionDecorator(StateChangeException)
    @catchExceptionDecorator(UcsError, toErrorState)
    @profilerDecoration("initialize")
    def initialize(self, state: IScriptState) -> None:
        """Initialize the controller associated with this context manager.

        ### Args:
        * `state` (`IScriptState`): state to initialize with
        """
        # Ensure settings are valid
        self.settings.assert_loaded()
        self.state = state
        state.initialize()

    @catchExceptionDecorator(StateChangeException)
    @catchExceptionDecorator(UcsError, toErrorState)
    @profilerDecoration("deinitialize")
    def deinitialize(self) -> None:
        """Deinitialize the controller when FL Studio closes or begins a render
        """
        if self._device is not None:
            self._device.deinitialize()
            self._device = None
        if self.state is not None:
            self.state.deinitialize()
            self.state = None

    @catchUnsafeOperation
    @catchExceptionDecorator(StateChangeException)
    @catchExceptionDecorator(UcsError, toErrorState)
    @profilerDecoration("processEvent")
    def processEvent(self, event: FlMidiMsg) -> None:
        """Process a MIDI event

        ### Args:
        * `event` (`event`): event to process
        """
        # Filter out events that shouldn't be forwarded here
        if isEventForwarded(event):
            # If device is none, ignore all forwarded messages
            if self._device is None or not isEventForwardedHere(event):
                event.handled = True
                return
        if self.state is None:
            raise MissingContextException("State not set")
        self.state.processEvent(event)

    @catchUnsafeOperation
    @catchExceptionDecorator(StateChangeException)
    @catchExceptionDecorator(UcsError, toErrorState)
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
        drop_tick_time = self.settings.get("advanced.drop_tick_time")
        if (self._last_tick - last_tick) / 1_000_000 > drop_tick_time:
            self._dropped_ticks += 1
            return
        tick_start = time_ns()
        # Tick active plugin
        self.activity.tick()
        # Tick the current script state
        self.state.tick()
        tick_end = time_ns()
        slow_tick_time = self.settings.get("advanced.slow_tick_time")
        if (tick_end - tick_start) / 1_000_000 > slow_tick_time:
            self._slow_ticks += 1

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

        This is indicative of FL Studio performance

        ### Returns:
        * `str`: info on dropped ticks
        """
        percent = int(self._dropped_ticks / self._ticks * 100)
        return f"{self._dropped_ticks} dropped ticks ({percent}%)"

    def getSlowTicks(self) -> str:
        """
        Returns the number of ticks that ran slowly

        This is indicative of script performance

        ### Returns:
        * `str`: info on dropped ticks
        """
        percent = int(self._slow_ticks / self._ticks * 100)
        return f"{self._slow_ticks} slow ticks ({percent}%)"

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
        new_state.initialize()
        raise StateChangeException("State changed")

    def registerDevice(self, dev: 'Device'):
        """
        Register a recognized device

        ### Args:
        * `dev` (`Device`): device number
        """
        self._device = dev

    def getDevice(self) -> 'Device':
        """
        Return a reference to the recognized device

        This is used so that forwarded events can be encoded correctly

        ### Raises:
        * `ValueError`: device not set

        ### Returns:
        * `Device`: device
        """
        if self._device is None:
            raise ValueError("Device not set")
        return self._device

    def getDeviceId(self) -> str:
        """
        Return the type of device that's been recognized

        This can be used to ensure that devices are recognized correctly

        ### Returns:
        * `str`: device type
        """
        if self._device is not None:
            return self._device.getId()
        else:
            return 'Device not recognized'


class ContextResetException(Exception):
    """
    Raised when the context is reset, so as to prevent any other operations
    using the old context from succeeding
    """


class MissingContextException(Exception):
    """
    Raised when the context hasn't been initialized yet
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
      initialized

    ### Returns:
    * `DeviceContextManager`: context
    """
    if _context is None:
        raise Exception("Context isn't initialized")

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
    leading to undefined behavior. This should only ever be called by the user
    through the console.

    ### Args:
    * `reason` (`str`, optional): Reason for reset. Defaults to `"none"`.
    """
    resetContext(reason)


def _initContext() -> None:
    """
    Initializes the context manager for the script
    """
    global _context
    _context = DeviceContextManager()


_initContext()
