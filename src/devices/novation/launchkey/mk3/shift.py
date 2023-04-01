"""
devices > novation > launchkey > mk3 > shift

Shift menu for activity switching on LkMk3

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""
from typing import Callable
from control_surfaces.matchers import (
    BasicControlMatcher,
    ShiftMatcher,
    ShiftView,
)
from devices.novation.launchkey.incontrol.controls import (
    LkDrumPadMatcher,
    StopSoloMuteButton,
    LkDeviceSelect,
    LkMk3DrumPad,
    LkMk3DrumPadActivity,
    LkMk3DrumPadSolo,
    LkMk3DrumPadMute,
)
from devices.novation.launchkey.incontrol.controls.activity import (
    LkDeviceSelectExtras,
)


def addNullControl(
    func: Callable[[], ShiftMatcher],
) -> Callable[[], BasicControlMatcher]:
    """
    Add an extra NullControl to fix some weirdness with the controllers

    Doing this as a decorator, since it may need to be used for the smaller
    variants too
    """
    def wrapper() -> BasicControlMatcher:
        matcher = BasicControlMatcher()
        matcher.addSubMatcher(func())
        matcher.addControl(LkDeviceSelectExtras())
        return matcher

    return wrapper


@addNullControl
def getActivitySwitcherLarge():
    """
    Get shift menu for activity switcher
    """
    main_view = LkDrumPadMatcher(LkMk3DrumPad)

    activity_switchers = ShiftView(
        LkDeviceSelect(),
        LkDrumPadMatcher(LkMk3DrumPadActivity),
        latch=True,
    )

    return ShiftMatcher(
        main_view,
        [activity_switchers],
    )


def getActivitySwitcherSmall():
    """
    Get shift menu for activity switcher
    """
    main_view = LkDrumPadMatcher(LkMk3DrumPad)

    activity_switchers = ShiftView(
        LkDeviceSelect(),
        LkDrumPadMatcher(LkMk3DrumPadActivity),
        latch=True,
    )

    mutes = ShiftView(
        StopSoloMuteButton(),
        LkDrumPadMatcher(LkMk3DrumPadSolo, LkMk3DrumPadMute),
        latch=True,
    )

    return ShiftMatcher(
        main_view,
        [activity_switchers, mutes],
    )
