"""
devices > matchers > indexed_matcher

Matches controls that use sequential MIDI control change indexes.

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""

from typing import Optional, Sequence
from control_surfaces.event_patterns import (
    IEventPattern,
    BasicPattern,
    ForwardedPattern
)
from fl_classes import FlMidiMsg, isMidiMsgStandard
from common.util.events import decodeForwardedEvent
from control_surfaces import ControlEvent, ControlSurface
from . import IControlMatcher


class IndexedMatcher(IControlMatcher):
    """
    Indexed matchers are used to match control surfaces that are differentiated
    by their data1 value.

    It expects each control in the provided controls list to match based on the
    `data1` value of `data1_start + i` where `i` is the index of that control
    in the control list.
    """
    def __init__(
        self,
        status: int,
        data1_start: int,
        controls: Sequence[ControlSurface],
        device: int = 1,
    ) -> None:
        """
        Create an indexed matcher.

        ### Args:
        * `status` (`int`): status byte used by each control surface

        * `data1_start` (`int`): data1 value for first control surface in list

        * `controls` (`list[ControlSurface]`): list of controls to bind

        * `device` (`int`, optional): device number, to allow for forwarded
          events. Defaults to `1`.
        """
        self.__pattern: IEventPattern = BasicPattern(
            status,
            range(data1_start, data1_start + len(controls)),
            ...
        )

        self.__start = data1_start
        self.__controls = controls

        if device != 1:
            self.__forwarded = True
            self.__pattern = ForwardedPattern(device, self.__pattern)
        else:
            self.__forwarded = False

        # Validation: each control surface we assigned should match our overall
        # pattern if we fulfil the event
        # FIXME: In order for this validation to work, we need the device ID
        # to be assigned already, but that's impossible since the device is
        # still being instantiated
        # for c in controls:
        #     if not self.__pattern.matchEvent(c.getPattern().fulfil()):
        #         raise ValueError(
        #             f"All control surfaces must match the pattern from the "
        #             f"given status and data1 bytes. Failed for control {c}, "
        #             f"pattern to match: {self.__pattern}"
        #         )

    def matchEvent(self, event: FlMidiMsg) -> Optional[ControlEvent]:
        if not self.__pattern.matchEvent(event):
            return None
        if self.__forwarded:
            decoded = decodeForwardedEvent(event)
        else:
            decoded = event
        assert isMidiMsgStandard(decoded)
        idx = decoded.data1 - self.__start
        match = self.__controls[idx].match(event)
        assert match is not None
        return match

    def getControls(self) -> Sequence[ControlSurface]:
        return self.__controls

    def tick(self, thorough: bool) -> None:
        for c in self.__controls:
            c.doTick(thorough)
