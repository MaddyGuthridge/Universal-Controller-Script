
from controlsurfaces.valuestrategies import ForwardedStrategy, Data2Strategy
from common.types import EventData
from common.util.events import encodeForwardedEvent
from tests.helpers import floatApproxEq
from tests.helpers.devices import DummyDevice, DummyDeviceContext


def test_forward_value():
    s = ForwardedStrategy(Data2Strategy())
    with DummyDeviceContext(2, DummyDevice):
        e = EventData(encodeForwardedEvent(EventData(0, 0, 0)))
    with DummyDeviceContext(1, DummyDevice):
        assert s.getFloatFromValue(s.getValueFromEvent(e)) == 0.0


def test_float_conversion():
    s = ForwardedStrategy(Data2Strategy())
    assert floatApproxEq(0.5, s.getFloatFromValue(s.getValueFromFloat(0.5)))


def test_channel():
    s = ForwardedStrategy(Data2Strategy())
    with DummyDeviceContext(2, DummyDevice):
        e = EventData(encodeForwardedEvent(EventData(0x9F, 0, 0)))
    with DummyDeviceContext(1, DummyDevice):
        assert s.getChannelFromEvent(e) == 0xF

    with DummyDeviceContext(2, DummyDevice):
        e = EventData(encodeForwardedEvent(EventData(0x95, 0, 0)))
    with DummyDeviceContext(1, DummyDevice):
        assert s.getChannelFromEvent(e) == 0x5
