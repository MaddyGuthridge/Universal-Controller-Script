"""
tests > value_strategy > forwarded_strategy_test

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""
from control_surfaces.value_strategies import ForwardedStrategy, Data2Strategy
from fl_classes import FlMidiMsg
from common.util.events import encodeForwardedEvent
from tests.helpers.devices import DummyDeviceBasic, DummyDeviceContext


def test_forward_value():
    s = ForwardedStrategy(Data2Strategy())
    with DummyDeviceContext(2, DummyDeviceBasic):
        e1 = FlMidiMsg(encodeForwardedEvent(FlMidiMsg(0, 0, 0)))
        e2 = FlMidiMsg(encodeForwardedEvent(FlMidiMsg(0, 0, 64)))
    with DummyDeviceContext(1, DummyDeviceBasic):
        assert s.getValueFromEvent(e1, 1.0) == 0.0
        assert s.getValueFromEvent(e2, 1.0) == 64/127


def test_channel():
    s = ForwardedStrategy(Data2Strategy())
    with DummyDeviceContext(2, DummyDeviceBasic):
        e = FlMidiMsg(encodeForwardedEvent(FlMidiMsg(0x9F, 0, 0)))
    with DummyDeviceContext(1, DummyDeviceBasic):
        assert s.getChannelFromEvent(e) == 0xF

    with DummyDeviceContext(2, DummyDeviceBasic):
        e = FlMidiMsg(encodeForwardedEvent(FlMidiMsg(0x95, 0, 0)))
    with DummyDeviceContext(1, DummyDeviceBasic):
        assert s.getChannelFromEvent(e) == 0x5
