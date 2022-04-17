"""
tests > helpers

Contains helper functions to use with tests
"""

from typing import Optional, TypeVar, Generator
from common.contextmanager import getContext, unsafeResetContext
from common.eventpattern.ieventpattern import IEventPattern
from common.types.eventdata import EventData

from devices import Device, BasicControlMatcher

T = TypeVar("T")


def floatApproxEq(expected: float, actual: float) -> bool:
    """
    Return whether there is less than a 5% error between the expected
    and actual values, or if the expected value is zero, whether the actual
    value is within 0.001 of it.
    """
    if expected == 0:
        return abs(actual) < 0.001
    return abs(expected - actual) / abs(expected) < 0.05


def combinations(
    p: list[T],
    number: int
) -> Generator[tuple[T, ...], None, None]:
    """
    Generates a set of combinations

    ### Args:
    * `p` (`list[T]`): list to get combinations from
    * `number` (`int`): number of combinations to return on each iteration

    ### Raises:
    * `ValueError`: number must be >= 1

    ### Yields:
    * `Iterator[tuple[T, ...]]`: combinations
    """
    if number <= 0:
        raise ValueError("Expecting more combinations")
    if number == 1:
        for item in p:
            yield (item,)
    else:
        for item in p:
            for others in combinations(p, number-1):
                yield item, *others


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
