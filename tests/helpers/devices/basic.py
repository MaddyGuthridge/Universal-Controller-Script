"""
tests > helpers > devices > basic

Device definitions for use when testing.

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""
from typing import Optional
from control_surfaces.event_patterns import IEventPattern, BasicPattern
from fl_classes import FlMidiMsg
from devices import Device
from control_surfaces.matchers import BasicControlMatcher, NoteMatcher
from control_surfaces import Fader, PlayButton, LoopButton, ControlSurface
from control_surfaces.value_strategies import (
    Data2Strategy,
    ButtonData2Strategy,
)

__all__ = [
    'DummyDeviceBasic',
    'DummyDeviceBasic2',
]


class DummyLoopButton1(LoopButton):
    """One type of loop button on our controller. This is used to test the
    one_type flag when matching events.
    """


class DummyLoopButton2(LoopButton):
    """Another type of loop button on our controller"""


class DummyDeviceAbstract(Device):
    """A device that is only used during testing. It is extended by devices
    with specific properties for testing.
    """
    def getId(self) -> str:
        return "Dummy.Device"

    @classmethod
    def getSupportedIds(cls) -> tuple[str, ...]:
        return ("Dummy.Device",)

    @staticmethod
    def getUniversalEnquiryResponsePattern() -> Optional[IEventPattern]:
        return None

    def getDeviceNumber(self) -> int:
        return 1

    @staticmethod
    def matchDeviceName(name: str) -> bool:
        return False

    @staticmethod
    def getDrumPadSize() -> tuple[int, int]:
        return 0, 0


class DummyDeviceBasic(DummyDeviceAbstract):
    """A dummy device so that the script doesn't have a hissy fit during
    testing.

    Contains some basic control surfaces:

    * Notes

    * Play button, matching `FlMidiMsg(0, 0, ...)`

    * 4 faders, matching `FlMidiMsg(1, i, ...)`, where `i` is the index

    * 2 loop buttons, matching `FlMidiMsg(2, i, ...)`, where `i` is the index
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
    def create(
        cls,
        event: Optional[FlMidiMsg] = None,
        id: Optional[str] = None,
    ) -> 'Device':
        return cls()

    def getDeviceNumber(self) -> int:
        return self._num


class DummyDeviceBasic2(DummyDeviceBasic):
    """Another dummy device, to test that different devices don't interact"""
    @staticmethod
    def getId() -> str:
        return "Dummy.Device.2"
