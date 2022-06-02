"""
tests > helpers > devices

Helper code for testing with devices

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""
from typing import Optional
from common.context_manager import getContext, unsafeResetContext
from control_surfaces.event_patterns import IEventPattern, BasicPattern
from common.types.event_data import EventData
from devices import Device
from control_surfaces.matchers import BasicControlMatcher, NoteMatcher
from control_surfaces import Fader, PlayButton, LoopButton, ControlSurface
from control_surfaces.value_strategies import (
    Data2Strategy,
    ButtonData2Strategy,
)

__all__ = [
    'DummyDevice',
    'DummyDevice2',
    'DummyDeviceContext',
]


class DummyLoopButton1(LoopButton):
    """One type of loop button on our controller. This is used to test the
    one_type flag when matching events.
    """


class DummyLoopButton2(LoopButton):
    """Another type of loop button on our controller"""


class DummyDevice(Device):
    """A dummy device so that the script doesn't have a hissy fit during
    testing.

    Contains some control surfaces:

    * Notes

    * Play button (0, 0, ...)

    * 4 faders (1, i, ...)

    * 2 loop buttons (2, i, ...)
    """

    def __init__(self, device_num: int = 1) -> None:
        matcher = BasicControlMatcher()
        self._num = device_num
        # Match notes
        matcher.addSubMatcher(NoteMatcher())
        # Match play button
        self.play_button = PlayButton(
            BasicPattern(0, 0, ...),
            ButtonData2Strategy()
        )
        matcher.addControl(self.play_button)
        # Add 4 faders
        self.faders: list[ControlSurface] = [
            Fader(
                BasicPattern(1, i, ...),
                Data2Strategy(),
                (0, i),
            ) for i in range(4)
        ]
        matcher.addControls(self.faders)
        # Add both our loop buttons
        self.loop_buttons: list[ControlSurface] = [
            DummyLoopButton1(
                BasicPattern(2, 0, ...),
                ButtonData2Strategy()
            ),
            DummyLoopButton2(
                BasicPattern(2, 1, ...),
                ButtonData2Strategy()
            )
        ]
        matcher.addControls(self.loop_buttons)
        super().__init__(matcher)

    @classmethod
    def create(cls, event: EventData = None, id: str = None) -> 'Device':
        return cls()

    def getId(self) -> str:
        return "Dummy.Device"

    @classmethod
    def getSupportedIds(cls) -> tuple[str, ...]:
        return ("Dummy.Device",)

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
    """Another dummy device, to test that different devices don't interact"""
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
