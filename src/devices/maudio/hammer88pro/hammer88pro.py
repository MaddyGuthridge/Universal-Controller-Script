"""
devices > maudio > hammer88pro > hammer88pro

Device definitions for M-Audio Hammer 88 Pro

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""

from typing import Optional
import device

from common import getContext
from control_surfaces.event_patterns import (
    BasicPattern,
    ForwardedPattern,
    ForwardedUnionPattern,
    NotePattern,
)
from common.extension_manager import ExtensionManager
from fl_classes import FlMidiMsg
from devices import Device
from control_surfaces.matchers import (
    BasicControlMatcher,
    NoteMatcher,
    PedalMatcher,
)
from control_surfaces import (
    NullControl,
    Fader,
    MasterFader,
    Knob,
    DrumPad,
    PlayButton,
    StopButton,
    RecordButton,
    FastForwardButton,
    RewindButton,
    LoopButton,
    MetronomeButton,
    StandardModWheel,
    ChannelAfterTouch,
    SwitchActivePluginButton,
    SwitchActiveWindowButton,
    GenericFaderButton,
    MuteButton,
    SoloButton,
    ArmButton,
    SelectButton,
    ControlSwitchButton,
)
from control_surfaces.value_strategies import (
    ForwardedStrategy,
    ForwardedUnionStrategy,
    ButtonData2Strategy,
    Data2Strategy,
    NoteStrategy,
)

from .hammer_pitch import HammerPitchWheel
from .jog_matcher import JogMatcher


class Hammer88Pro(Device):
    """
    Device definition for Hammer 88 Pro

    Note: this requires the presets for both DAW and User modes to be loaded
    on the device.
    """

    def __init__(self) -> None:
        matcher = BasicControlMatcher()
        # Null events
        matcher.addControl(NullControl(
            BasicPattern(0xFA, 0x0, 0x0)
        ))
        matcher.addControl(NullControl(
            BasicPattern(0xFC, 0x0, 0x0)
        ))
        # Switch fader button types
        # TODO: When adding lighting, map this to a refresh command?
        matcher.addControl(NullControl(
            BasicPattern(0xBF, range(0x39, 0x3D+1), ...)
        ))

        # Active switches
        getContext().activity.setSplitWindowsPlugins(True)
        matcher.addControl(SwitchActiveWindowButton(
            ForwardedPattern(3, BasicPattern(0xBF, 0x6E, ...)),
            ForwardedStrategy(ButtonData2Strategy())
        ))
        matcher.addControl(SwitchActivePluginButton(
            ForwardedPattern(3, BasicPattern(0xBF, 0x6F, ...)),
            ForwardedStrategy(ButtonData2Strategy())
        ))

        # Jog wheel stuff
        matcher.addSubMatcher(JogMatcher())

        # Notes and pedals
        matcher.addSubMatcher(NoteMatcher())
        matcher.addSubMatcher(PedalMatcher())
        matcher.addControl(ChannelAfterTouch.fromChannel(...))

        # Drum pads (high priority because they just use note on events)
        matcher.addControls([
            DrumPad(NotePattern(i, 9), NoteStrategy(), (i // 8, i % 8))
            for i in range(16)
        ], 10)

        # Knobs
        matcher.addControls([
            Knob(
                ForwardedUnionPattern(3, BasicPattern(0xB0, i+80, ...)),
                ForwardedUnionStrategy(Data2Strategy()),
                (0, i)
            ) for i in range(8)
        ])

        # Faders
        matcher.addControls([
            Fader(
                ForwardedUnionPattern(3, BasicPattern(0xB0, i+48, ...)),
                ForwardedUnionStrategy(Data2Strategy()),
                (0, i)
            ) for i in range(9)
        ])
        matcher.addControl(
            MasterFader(
                ForwardedUnionPattern(3, BasicPattern(0xB0, 56, ...)),
                ForwardedStrategy(Data2Strategy())
            )
        )

        matcher.addControls([
            GenericFaderButton(
                BasicPattern(0xB5, 0x30 + i, ...),
                ButtonData2Strategy(),
                (0, i)
            ) for i in range(8)
        ])

        fader_button_types = [
            ArmButton,
            SelectButton,
            MuteButton,
            SoloButton
        ]

        for i, t in zip(range(1, 5), fader_button_types):
            matcher.addControls([
                t(
                    ForwardedPattern(3, BasicPattern(0xB0 + i, 0x30 + j, ...)),
                    ForwardedStrategy(ButtonData2Strategy()),
                    (0, j)
                ) for j in range(8)
            ])

        # Transport buttons
        matcher.addControl(StopButton(
            ForwardedPattern(3, BasicPattern(0xBF, 102, ...)),
            ForwardedStrategy(ButtonData2Strategy())
        ))
        matcher.addControl(PlayButton(
            ForwardedPattern(3, BasicPattern(0xBF, 103, ...)),
            ForwardedStrategy(ButtonData2Strategy())
        ))
        matcher.addControl(RecordButton(
            ForwardedPattern(3, BasicPattern(0xBF, 104, ...)),
            ForwardedStrategy(ButtonData2Strategy())
        ))
        matcher.addControl(RewindButton(
            ForwardedPattern(3, BasicPattern(0xBF, 105, ...)),
            ForwardedStrategy(ButtonData2Strategy())
        ))
        matcher.addControl(FastForwardButton(
            ForwardedPattern(3, BasicPattern(0xBF, 106, ...)),
            ForwardedStrategy(ButtonData2Strategy())
        ))
        matcher.addControl(LoopButton(
            ForwardedPattern(3, BasicPattern(0xBF, 107, ...)),
            ForwardedStrategy(ButtonData2Strategy())
        ))
        matcher.addControl(MetronomeButton(
            ForwardedPattern(3, BasicPattern(0xB9, 0x74, ...)),
            ForwardedStrategy(ButtonData2Strategy())
        ))
        matcher.addControl(StandardModWheel())
        matcher.addControl(HammerPitchWheel())

        matcher.addControl(ControlSwitchButton(
            ForwardedPattern(3, BasicPattern(0xB9, 0x44, ...)),
            ForwardedStrategy(ButtonData2Strategy()),
        ))

        super().__init__(matcher)

    @classmethod
    def getDrumPadSize(cls) -> tuple[int, int]:
        return 2, 8

    @classmethod
    def create(
        cls,
        event: Optional[FlMidiMsg] = None,
        id: Optional[str] = None,
    ) -> 'Device':
        return cls()

    def getId(self) -> str:
        return "Maudio.Hammer88Pro"

    @classmethod
    def getSupportedIds(cls) -> tuple[str, ...]:
        return ("Maudio.Hammer88Pro",)

    @classmethod
    def getUniversalEnquiryResponsePattern(cls):
        return BasicPattern(
            [
                0xF0,  # Sysex start
                0x7E,  # Device response
                ...,  # OS Device ID
                0x06,  # Separator
                0x02,  # Separator
                0x00,  # Manufacturer
                0x01,  # Manufacturer
                0x05,  # Manufacturer
                0x00,  # Family code
                0x3C,  # Family code
                # Extra details omitted
            ]
        )

    def getDeviceNumber(self) -> int:
        name = device.getName()

        try:
            return {
                "Hammer 88 Pro": 1,
                "Hammer 88 Pro USB MIDI": 1,
                "MIDIIN3 (Hammer 88 Pro)": 3,
                "Hammer 88 Pro Mackie/HUI": 3,
            }[name]
        except KeyError as e:
            raise TypeError("Couldn't find a mapping for device name") from e


ExtensionManager.devices.register(Hammer88Pro)
