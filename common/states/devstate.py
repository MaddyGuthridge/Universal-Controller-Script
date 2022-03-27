
import ui
from common import log, verbosity, consts
from common.types import EventData
from common.util.events import eventToString
from abc import abstractmethod
from . import IScriptState
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from devices import Device

class DeviceState(IScriptState):
    """
    Abstract state that requires a device to be detected
    """

    @classmethod
    @abstractmethod
    def create(cls, device: 'Device') -> 'DeviceState':
        """
        Create an instance of a DeviceState

        ### Args:
        * `device` (`Device`): device used by this state

        ### Returns:
        * `DeviceState`: new instance
        """
        raise NotImplementedError("This method should be implemented by "
                                  "child classes")
