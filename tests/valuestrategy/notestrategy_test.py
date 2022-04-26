from tests.helpers import floatApproxEq
from common.types import EventData
from controlsurfaces.valuestrategies import NoteStrategy


def test_value_note_on():
    s = NoteStrategy()
    val = s.getValueFromEvent(EventData(0x9F, 0, 0x7F))
    assert s.getFloatFromValue(val) == 1.0


def test_value_note_off():
    s = NoteStrategy()
    val = s.getValueFromEvent(EventData(0x9F, 0, 0))
    assert s.getFloatFromValue(val) == 0.0

    val = s.getValueFromEvent(EventData(0x8F, 0, 0x7F))
    assert s.getFloatFromValue(val) == 0.0


def test_float_conversion():
    s = NoteStrategy()
    assert floatApproxEq(0.5, s.getFloatFromValue(s.getValueFromFloat(0.5)))


def test_channel():
    s = NoteStrategy()
    assert s.getChannelFromEvent(EventData(0x9F, 0, 0)) == 0xF
    assert s.getChannelFromEvent(EventData(0x95, 0, 0)) == 0x5
