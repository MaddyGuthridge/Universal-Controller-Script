
from common.types import EventData
from controlsurfaces.valuestrategies import Data2Strategy


def test_min_value_event():
    s = Data2Strategy()
    assert s.getValueFromEvent(EventData(0, 0, 0), 1.0) == 0.0
    assert s.getValueFromEvent(EventData(0, 0, 64), 1.0) == 64/127


def test_channel():
    s = Data2Strategy()
    assert s.getChannelFromEvent(EventData(0x9F, 0, 0)) == 0xF
    assert s.getChannelFromEvent(EventData(0x95, 0, 0)) == 0x5
