"""
tests > device_shadow_test

Tests to ensure device shadows bind controls correctly

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""

import pytest
from common.plug_indexes import WindowIndex
from control_surfaces import (
    ControlEvent,
    PlayButton,
    Fader,
)
from devices import DeviceShadow
from tests.helpers.devices import DummyDeviceBasic


def test_binding():
    """Make sure we can bind to controls"""
    class DummyException(Exception):
        pass

    def _dummy(*args, **kwargs) -> bool:
        raise DummyException()

    s = DeviceShadow(DummyDeviceBasic())

    m = s.getControlMatches(PlayButton)[0]
    s.bindControl(m, _dummy)

    with pytest.raises(DummyException):
        s.processEvent(ControlEvent(
            ...,  # type: ignore
            m.getControl(),
            0.0,
            0,
            False,
        ), WindowIndex.MIXER)


def test_bind_same():
    """
    Make sure we can't bind the same control twice
    """
    def _dummy(*args, **kwargs) -> bool:
        return True

    s = DeviceShadow(DummyDeviceBasic())

    m = s.getControlMatches(PlayButton)
    s.bindControls(m, _dummy)
    # Use both methods for binding controls
    with pytest.raises(ValueError):
        s.bindControls(m, _dummy)
    with pytest.raises(ValueError):
        s.bindControl(m[0], _dummy)


def test_bind_matches_all():
    """Test we can bind all matches"""
    class DummyException(Exception):
        pass

    def _dummy(*args, **kwargs) -> bool:
        raise DummyException()

    s = DeviceShadow(DummyDeviceBasic())

    matches = s.bindMatches(Fader, _dummy)

    # Check each match is assigned
    for m in matches:
        with pytest.raises(DummyException):
            s.processEvent(ControlEvent(
                ...,  # type: ignore
                m.getControl(),
                0.0,
                0,
                False,
            ), WindowIndex.MIXER)
