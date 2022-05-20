"""
control_surfaces > event_patterns > fulfil

Helper code for generating EventData objects that match event patterns
"""

import random
from common.types import EventData
from common.util.events import encodeForwardedEvent
from control_surfaces.event_patterns import (
    IEventPattern,
    BasicPattern,
    UnionPattern,
    ForwardedPattern,
    ForwardedUnionPattern,
    ByteMatch,
)


def fulfil(pattern: IEventPattern) -> EventData:
    """
    Fulfil an event pattern by creating an EventData object that will match
    that pattern.

    ### Args:
    * `pattern` (`IEventPattern`): pattern to fulfil

    ### Returns:
    * `EventData`: event that matches pattern
    """
    if isinstance(pattern, BasicPattern):
        return fulfilBasic(pattern)
    elif isinstance(pattern, ForwardedPattern):
        return fulfilForwarded(pattern)
    elif isinstance(pattern, ForwardedUnionPattern):
        return fulfilForwardedUnion(pattern)
    elif isinstance(pattern, UnionPattern):
        return fulfilUnion(pattern)
    else:
        raise TypeError(f"No definition to fulfil {type(pattern)}")


def fulfilBasic(pattern: BasicPattern) -> EventData:
    if pattern.sysex_event:
        return EventData(bytes([fulfilByte(b) for b in pattern.sysex]))
    else:
        return EventData(
            fulfilByte(pattern.status),
            fulfilByte(pattern.data1),
            fulfilByte(pattern.data2),
        )


def fulfilForwarded(pattern: ForwardedPattern) -> EventData:
    num = pattern._device_num
    return EventData(encodeForwardedEvent(fulfil(pattern._pattern), num))


def fulfilForwardedUnion(pattern: ForwardedUnionPattern) -> EventData:
    return fulfilUnion(pattern._pattern)


def fulfilUnion(pattern: UnionPattern) -> EventData:
    return fulfil(random.choice(pattern._patterns))


def fulfilByte(b: ByteMatch) -> int:
    if isinstance(b, int):
        return b
    elif isinstance(b, range):
        return random.randrange(b.start, b.stop, b.step)
    elif isinstance(b, tuple):
        return random.choice(b)
    elif b is Ellipsis:
        return random.randrange(0, 128)
    else:
        raise TypeError()
