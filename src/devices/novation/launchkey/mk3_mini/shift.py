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
from control_surfaces.matchers import (
    ShiftMatcher,
    ShiftView,
    BasicControlMatcher,
)
from devices.novation.launchkey.incontrol.controls import (
    LkMk3ControlSwitchButton,
    LkMk3RecordButton,
    Mk3DirectionLeft,
    Mk3DirectionRight,
    MiniMk3DirectionUp,
    MiniMk3DirectionDown,
    StopSoloMuteButton,
    LkDrumPadMatcher,
    LkMk3DrumPad,
    LkMk3DrumPadSolo,
    LkMk3DrumPadMute,
    LkMk3MiniDrumPadActivity,
    LkMk3PlayButton,
)


def getShiftControls() -> ShiftMatcher:
    shift_button = NullControl(
        ForwardedPattern(2, BasicPattern(0xB0, 0x6C, ...)),
        ForwardedStrategy(ButtonData2Strategy()),
    )

    # Non shifted events
    main_view = BasicControlMatcher()
    main_view.addControl(LkMk3RecordButton())
    main_view.addControl(LkMk3ControlSwitchButton())
    main_view.addSubMatcher(LkDrumPadMatcher(LkMk3DrumPad))

    # Shifted events
    shift_view = BasicControlMatcher()
    shift_view.addControl(CaptureMidiButton(
        ForwardedPattern(2, BasicPattern(0xBF, 0x75, ...)),
        ForwardedStrategy(ButtonData2Strategy()),
    ))
    shift_view.addControls([
        MiniMk3DirectionUp(),
        MiniMk3DirectionDown(),
        Mk3DirectionLeft(),
        Mk3DirectionRight(),
    ])

    shift = ShiftView(shift_button, shift_view, allow_fallback_match=False)

    mutes = ShiftView(
        StopSoloMuteButton(),
        LkDrumPadMatcher(LkMk3DrumPadSolo, LkMk3DrumPadMute),
        disable_in_other_views=True,
        latch=True,
    )
    activity_switchers = ShiftView(
        LkMk3PlayButton(),
        LkDrumPadMatcher(LkMk3MiniDrumPadActivity),
        ignore_single_press=True,
    )

    return ShiftMatcher(
        main_view,
        [shift, mutes, activity_switchers],
    )
