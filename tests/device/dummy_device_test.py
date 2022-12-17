"""
tests > device > dummy_device_test

Tests for dummy devices

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""
from tests.helpers.devices import DummyDeviceDrumPads
from tests.helpers import floatApproxEqRatio


def test_drum_pad_dummy_device_generate_event():
    """Do events generated using getEventForDrumPad actually match up?"""
    d = DummyDeviceDrumPads(8, 8)
    assert d.matchEvent(  # type: ignore
        d.getEventForDrumPad(5, 5, 0)  # type: ignore
    ).coordinate == (5, 5)
    assert d.matchEvent(  # type: ignore
        d.getEventForDrumPad(5, 4, 0)  # type: ignore
    ).coordinate == (5, 4)
    assert d.matchEvent(
        d.getEventForDrumPad(8, 0, 0)  # type: ignore
    ) is None


def test_drum_pad_dummy_device_generate_event_value():
    """Do events generated using getEventForDrumPad have the right velocity?"""
    d = DummyDeviceDrumPads(8, 8)
    assert floatApproxEqRatio(
        0.5,
        d.matchEvent(d.getEventForDrumPad(5, 5, 0.5)).value  # type: ignore
    )
