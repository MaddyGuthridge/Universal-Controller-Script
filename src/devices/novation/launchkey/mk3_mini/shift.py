"""
devices > novation > launchkey > mk3_mini > shift

Definition for shifted controls for Launchkey Mini Mk3

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""

from control_surfaces.event_patterns import BasicPattern, ForwardedPattern
from control_surfaces.value_strategies import (
    ButtonData2Strategy,
    ForwardedStrategy,
)
from control_surfaces import (
    NullControl,
    CaptureMidiButton,
)
from control_surfaces.matchers import ShiftMatcher, BasicControlMatcher
from devices.novation.launchkey.incontrol.controls import (
    LkMk3ControlSwitchButton,
    LkMk3RecordButton,
    Mk3DirectionLeft,
    Mk3DirectionRight,
    MiniMk3DirectionUp,
    MiniMk3DirectionDown,
    getMk3MiniMuteControls,
)


def getShiftControls() -> ShiftMatcher:
    shift = NullControl(
        ForwardedPattern(2, BasicPattern(0xB0, 0x6C, ...)),
        ForwardedStrategy(ButtonData2Strategy()),
    )

    # Non shifted events
    non_shift_matcher = BasicControlMatcher()
    non_shift_matcher.addControl(LkMk3RecordButton())
    non_shift_matcher.addControl(LkMk3ControlSwitchButton())
    non_shift_matcher.addSubMatcher(getMk3MiniMuteControls())

    # Shifted events
    shift_matcher = BasicControlMatcher()
    shift_matcher.addControl(CaptureMidiButton(
        ForwardedPattern(2, BasicPattern(0xBF, 0x75, ...)),
        ForwardedStrategy(ButtonData2Strategy()),
    ))
    shift_matcher.addControls([
        MiniMk3DirectionUp(),
        MiniMk3DirectionDown(),
        Mk3DirectionLeft(),
        Mk3DirectionRight(),
    ])

    return ShiftMatcher(
        shift,
        non_shift_matcher,
        shift_matcher,
    )
