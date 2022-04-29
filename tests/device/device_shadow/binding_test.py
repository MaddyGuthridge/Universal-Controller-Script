"""
tests > device_shadow_test

Tests to ensure device shadows bind controls correctly
"""

import pytest
from controlsurfaces import (
    ControlEvent,
    PlayButton,
    Fader,
)
from devices import DeviceShadow
from tests.helpers.devices import DummyDevice


def test_binding():
    """Make sure we can bind to controls"""
    class DummyException(Exception):
        pass

    def _dummy(*args, **kwargs) -> bool:
        raise DummyException()

    s = DeviceShadow(DummyDevice())

    m = s.getControlMatches(PlayButton)[0]
    s.bindControl(m, _dummy)

    with pytest.raises(DummyException):
        s.processEvent(ControlEvent(m.getControl(), 0.0, 0, False), None)


def test_bind_same():
    """
    Make sure we can't bind the same control twice
    """
    def _dummy(*args, **kwargs) -> bool:
        pass

    s = DeviceShadow(DummyDevice())

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

    s = DeviceShadow(DummyDevice())

    matches = s.bindMatches(Fader, _dummy)

    # Check each match is assigned
    for m in matches:
        with pytest.raises(DummyException):
            s.processEvent(ControlEvent(m.getControl(), 0.0, 0, False), None)
