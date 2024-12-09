"""
control_surfaces > event_patterns > forwarded_pattern

Contains the definition for the ForwardedPattern class

Authors:
* Maddy Guthridge [hello@maddyguthridge.com, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""

from common.util.forwarded_events import (
    receive_event_from_external,
    encode_forwarded_event,
)
from . import IEventPattern, UnionPattern

from fl_classes import FlMidiMsg


class ForwardedPattern(IEventPattern):
    """
    The forwarded pattern is used to parse data from events which were
    forwarded from the Universal Event Forwarded device script.

    This decodes the forwarded event, then checks it against another provided
    pattern.

    This allows events to all be processed on the same script, which massively
    simplifies things. Refer to docs/contributing/devices/event_forward.md
    """

    def __init__(self, device_num: int, pattern: IEventPattern) -> None:
        """
        Create a ForwardedPattern recognizer. This is used to pattern match
        with events that were forwarded from the Universal Event Forwarder.

        ### Args:
        * `device_num` (`int`): device number to accept events from
        * `pattern` (`IEventPattern`): pattern to detect from
        """
        super().__init__()
        self._device_num = device_num
        self._pattern = pattern

    def matchEvent(self, event: FlMidiMsg) -> bool:
        # Check if the event was forwarded here
        if (info := receive_event_from_external(event)) is not None:
            decoded, device_num = info
            return (
                device_num == self._device_num
                and self._pattern.matchEvent(decoded)
            )
        return False

    def fulfil(self) -> FlMidiMsg:
        num = self._device_num
        return FlMidiMsg(encode_forwarded_event(self._pattern.fulfil(), num))


class ForwardedUnionPattern(IEventPattern):
    """
    Represents an event that can either be forwarded or direct.
    """

    def __init__(self, device_num: int, pattern: IEventPattern) -> None:
        """
        Create a ForwardedUnionPattern recognizer

        ### Args:
        * `device_num` (`int`): device number to recognize
        * `pattern` (`IEventPattern`): pattern to match
        """
        self._pattern = UnionPattern(pattern, ForwardedPattern(
            device_num, pattern
        ))

    def matchEvent(self, event: FlMidiMsg) -> bool:
        return self._pattern.matchEvent(event)

    def fulfil(self) -> FlMidiMsg:
        return self._pattern.fulfil()
