"""
tests > value_strategy > data_strategy_test

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""
from fl_classes import FlMidiMsg
from control_surfaces.value_strategies import Data1Strategy, Data2Strategy


def test_data1_min_value_event():
    s = Data1Strategy()
    assert s.getValueFromEvent(FlMidiMsg(0, 0, 0), 1.0) == 0.0
    assert s.getValueFromEvent(FlMidiMsg(0, 64, 0), 1.0) == 64/127


def test_data1_channel():
    s = Data1Strategy()
    assert s.getChannelFromEvent(FlMidiMsg(0x9F, 0, 0)) == 0xF
    assert s.getChannelFromEvent(FlMidiMsg(0x95, 0, 0)) == 0x5


def test_data2_min_value_event():
    s = Data2Strategy()
    assert s.getValueFromEvent(FlMidiMsg(0, 0, 0), 1.0) == 0.0
    assert s.getValueFromEvent(FlMidiMsg(0, 0, 64), 1.0) == 64/127


def test_data2_channel():
    s = Data2Strategy()
    assert s.getChannelFromEvent(FlMidiMsg(0x9F, 0, 0)) == 0xF
    assert s.getChannelFromEvent(FlMidiMsg(0x95, 0, 0)) == 0x5
