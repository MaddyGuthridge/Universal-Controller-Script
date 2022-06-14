"""
control_surfaces > value_strategies > forwarded_strategy

Contains the definition for the ForwardedStrategy strategy for getting values
from forwarded events

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""

from fl_classes import FlMidiMsg
from common.util.events import decodeForwardedEvent, isEventForwarded
from . import IValueStrategy


class ForwardedStrategy(IValueStrategy):
    """
    Value strategy used to get data out of
    forwarded events.
    """
    def __init__(self, strat: IValueStrategy) -> None:
        self._strat = strat

    def getValueFromEvent(self, event: FlMidiMsg, value: float) -> float:
        # The value is already matching, so we can cheat somewhat with getting
        # the data out
        return self._strat.getValueFromEvent(
            decodeForwardedEvent(event),
            value,
        )

    def getChannelFromEvent(self, event: FlMidiMsg):
        return self._strat.getChannelFromEvent(decodeForwardedEvent(event))


class ForwardedUnionStrategy(IValueStrategy):
    """
    Value strategy for getting values from events that could be either
    forwarded or not
    """
    def __init__(self, strat: IValueStrategy) -> None:
        self._strat = strat
        self._strat_forward = ForwardedStrategy(strat)

    def getValueFromEvent(self, event: FlMidiMsg, value: float) -> float:
        if isEventForwarded(event):
            return self._strat_forward.getValueFromEvent(event, value)
        else:
            return self._strat.getValueFromEvent(event, value)

    def getChannelFromEvent(self, event: FlMidiMsg):
        if isEventForwarded(event):
            return self._strat_forward.getChannelFromEvent(event)
        else:
            return self._strat.getChannelFromEvent(event)
