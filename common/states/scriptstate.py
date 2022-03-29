"""
common > scriptstate

Contains the IScriptState interface, which contains a state used by the
script's context manager.

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]
"""

from typing import Any, Callable
from typing_extensions import ParamSpec
from abc import abstractmethod
from common.types import EventData


class IScriptState:
    """
    Represents a state the script can be in.

    This interface is implemented by various classes to allow the script to
    switch between states. For example:
    * Waiting to recognise device
    * Main state (processing events and stuff)
    * Error state (something went horribly wrong)
    """

    @abstractmethod
    def initialise(self) -> None:
        """
        Initialise this context
        """
        raise NotImplementedError(
            "This method must be overridden by child classes"
        )

    @abstractmethod
    def processEvent(self, event: EventData) -> None:
        """Process a MIDI event

        ### Args:
        * `event` (`event`): event to process
        """
        raise NotImplementedError(
            "This method must be overridden by child classes"
        )

    @abstractmethod
    def tick(self) -> None:
        """
        Called frequently to allow any required updates to the controller
        """
        raise NotImplementedError(
            "This method must be overridden by child classes"
        )


class StateChangeException(Exception):
    """
    Raised when the the state of the controller has been reset
    """

P = ParamSpec("P")

def catchStateChangeException(func: Callable[P, Any])-> Callable[P, None]:
    """A decorator for catching StateChangeExceptions so that the program
    continues normally

    ### Args:
    * `func` (`Callable`): function to decorate

    ### Returns:
    * `Callable`: decorated function
    """
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except StateChangeException:
            pass
    return wrapper
