"""
devices > novation > launchkey > mk3_mini > shift

Definition for shifted controls for Launchkey Mini Mk3
"""

from controlsurfaces.eventpattern import BasicPattern, ForwardedPattern
from controlsurfaces.valuestrategies import (
    ButtonData2Strategy,
    ForwardedStrategy,
)
from controlsurfaces import (
    NullEvent,
    CaptureMidiButton,
)
from devices.matchers import ShiftMatcher, BasicControlMatcher
from devices.novation.launchkey.incontrol.controls import (
    LkMk3RecordButton,
)


def getShiftControls() -> ShiftMatcher:
    shift = NullEvent(
        ForwardedPattern(2, BasicPattern(0xB0, 0x6C, ...)),
        ForwardedStrategy(ButtonData2Strategy()),
    )

    # Non shifted events
    non_shift_matcher = BasicControlMatcher()
    non_shift_matcher.addControl(LkMk3RecordButton())

    # Shifted events
    shift_matcher = BasicControlMatcher()
    shift_matcher.addControl(CaptureMidiButton(
        ForwardedPattern(2, BasicPattern(0xBF, 0x75, ...)),
        ForwardedStrategy(ButtonData2Strategy()),
    ))

    return ShiftMatcher(
        shift,
        non_shift_matcher,
        shift_matcher,
    )
