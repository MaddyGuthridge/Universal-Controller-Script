"""
tests > value_strategy > twos_compliment_delta_test

tests for the two's compliment delta value strategy

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""
import pytest
from fl_classes import FlMidiMsg
from control_surfaces.value_strategies import TwosComplimentDeltaStrategy


def test_zero():
    s = TwosComplimentDeltaStrategy()
    e = FlMidiMsg(0, 0, 0)
    assert s.getValueFromEvent(e, 0.5) == 0.5


def test_positive():
    s = TwosComplimentDeltaStrategy()
    e = FlMidiMsg(0, 0, 1)
    assert s.getValueFromEvent(e, 0.5) == 0.5 + 1/64
    e = FlMidiMsg(0, 0, 5)
    assert s.getValueFromEvent(e, 0.5) == 0.5 + 5/64


def test_negative():
    s = TwosComplimentDeltaStrategy()
    e = FlMidiMsg(0, 0, 127)
    assert s.getValueFromEvent(e, 0.5) == 0.5 - 1/64
    e = FlMidiMsg(0, 0, 123)
    assert s.getValueFromEvent(e, 0.5) == 0.5 - 5/64


@pytest.mark.parametrize(
    'e', [
        FlMidiMsg(0, 0, 1),
        FlMidiMsg(0, 0, 127),
        FlMidiMsg(0, 0, 0),
        FlMidiMsg(0, 0, 5),
    ]
)
def test_scaling(e):
    s1 = TwosComplimentDeltaStrategy()
    s2 = TwosComplimentDeltaStrategy(2.0)
    delta = s1.getValueFromEvent(e, 0.5) - 0.5
    assert s2.getValueFromEvent(e, 0.5) - 0.5 == delta * 2


def test_clamp():
    s = TwosComplimentDeltaStrategy()
    e = FlMidiMsg(0, 0, 127)
    assert s.getValueFromEvent(e, 0.0) == 0.0
    e = FlMidiMsg(0, 0, 1)
    assert s.getValueFromEvent(e, 1.0) == 1.0
