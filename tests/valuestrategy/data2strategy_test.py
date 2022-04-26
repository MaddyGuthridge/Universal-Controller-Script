from tests.helpers import floatApproxEq
from common.types import EventData
from controlsurfaces.valuestrategies import Data2Strategy


def test_min_value_event():
    s = Data2Strategy()
    val = s.getValueFromEvent(EventData(0, 0, 0))
    assert s.getFloatFromValue(val) == 0.0


def test_float_conversion():
    s = Data2Strategy()
    assert floatApproxEq(0.5, s.getFloatFromValue(s.getValueFromFloat(0.5)))


def test_channel():
    s = Data2Strategy()
    assert s.getChannelFromEvent(EventData(0x9F, 0, 0)) == 0xF
    assert s.getChannelFromEvent(EventData(0x95, 0, 0)) == 0x5
