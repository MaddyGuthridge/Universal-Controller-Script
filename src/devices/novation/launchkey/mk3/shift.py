"""
devices > novation > launchkey > mk3 > shift

Shift menu for activity switching on LkMk3

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""
from control_surfaces.matchers import (
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


def getActivitySwitcherLarge():
    """
    Get shift menu for activity switcher
    """
    main_view = LkDrumPadMatcher(LkMk3DrumPad)

    activity_switchers = ShiftView(
        LkDeviceSelect(),
        LkDrumPadMatcher(LkMk3DrumPadActivity),
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
    )

    mutes = ShiftView(
        StopSoloMuteButton(),
        LkDrumPadMatcher(LkMk3DrumPadSolo, LkMk3DrumPadMute),
    )

    return ShiftMatcher(
        main_view,
        [activity_switchers, mutes],
    )
