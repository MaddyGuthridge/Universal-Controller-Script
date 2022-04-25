"""
tests > helpers > devices

Helper code for testing with devices
"""
from typing import Optional
from common.contextmanager import getContext, unsafeResetContext
from common.eventpattern.ieventpattern import IEventPattern
from common.types.eventdata import EventData
from devices import Device, BasicControlMatcher

__all__ = [
    'DummyDevice',
    'DummyDevice2',
    'DummyDeviceContext',
]


class DummyDevice(Device):
    """A dummy device so that the script doesn't have a hissy fit during testing
    """

    def __init__(self, device_nam: int = 1) -> None:
        matcher = BasicControlMatcher()
        self._num = device_nam
        super().__init__(matcher)

    @classmethod
    def create(cls, event: Optional[EventData]) -> 'Device':
        return cls()

    @staticmethod
    def getId() -> str:
        return "Dummy.Device"

    @staticmethod
    def getUniversalEnquiryResponsePattern() -> Optional[IEventPattern]:
        return None

    def getDeviceNumber(self) -> int:
        return self._num

    @staticmethod
    def matchDeviceName(name: str) -> bool:
        return False

    @staticmethod
    def getDrumPadSize() -> tuple[int, int]:
        return 0, 0


class DummyDevice2(DummyDevice):
    """Another dummy device"""
    @staticmethod
    def getId() -> str:
        return "Dummy.Device.2"


class DummyDeviceContext:
    """A context manager for working with dummy devices"""

    def __init__(
        self,
        num: int = 1,
        dev: type[DummyDevice] = DummyDevice
    ) -> None:
        self._dev = dev
        self._num = num

    def __enter__(self):
        getContext().registerDevice(self._dev(self._num))

    def __exit__(self, exc_type, exc_value, exc_traceback):
        unsafeResetContext()
