"""
devices > mvave > smk25_ii > smk25_ii

Definition for the M-VAVE SMK25-II controller.

There are labels for transport controls, but I haven't gotten to adding them.
They share the same keys as the drum pad.

Authors:
* Xinayder

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""

from typing import Optional

from fl_classes import FlMidiMsg

from common.extension_manager import ExtensionManager
from control_surfaces import (
    ChannelAfterTouch,
    ControlSwitchButton,
    Fader,
    FastForwardButton,
    Knob,
    MuteButton,
    PlayButton,
    RecordButton,
    RewindButton,
    SoloButton,
    StopButton,
    DirectionLeft,
    DirectionRight,
    UndoButton,
    DrumPad,
    StandardModWheel,
    StandardPitchWheel,
)
from control_surfaces.event_patterns import BasicPattern, IEventPattern, NotePattern
from control_surfaces.matchers import BasicControlMatcher, NoteMatcher
from control_surfaces.value_strategies import (
    ButtonData2Strategy,
    Data2Strategy,
    NoteStrategy,
)
from devices.device import Device

class SMK25II(Device):
    """M-VAVE SMK25-II
    """

    def __init__(self) -> None:
        matcher = BasicControlMatcher()

        matcher.addSubMatcher(NoteMatcher())
        matcher.addControl(StandardPitchWheel.create())
        matcher.addControl(StandardModWheel.create())
        matcher.addControl(ChannelAfterTouch.fromChannel(...))

        matcher.addControls([
            DrumPad(NotePattern(i, 9), NoteStrategy(), (i // 8, i % 8))
            for i in range(16)
        ], 10)


        for i in range(8):
            # Knobs
            matcher.addControl(Knob(
                BasicPattern(0xB0, 0x1E + i, ...),
                Data2Strategy(),
                (0, i)
            ))

        super().__init__(matcher)

    @classmethod
    def getDrumPadSize(cls) -> tuple[int, int]:
        return 2, 8

    @classmethod
    def matchDeviceName(cls, name: str) -> bool:
        return name.startswith("SINCO - SINCO SMK25II")

    @classmethod
    def create(
        cls,
        event: Optional[FlMidiMsg] = None,
        id: Optional[str] = None,
    ) -> 'Device':
        return cls()

    def getId(self) -> str:
        return "MVAVE.SMK25.II"

    @classmethod
    def getSupportedIds(cls) -> tuple[str, ...]:
        return ("MVAVE.SMK25.II",)


ExtensionManager.devices.register(SMK25II)
