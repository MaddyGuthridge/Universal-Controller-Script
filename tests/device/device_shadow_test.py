"""
tests > device_shadow_test

Tests to ensure device shadows bind controls correctly
"""

import pytest
# from common.types import EventData
from controlsurfaces import (
    ControlSurface,
    ControlEvent,
    Note,
    PlayButton,
    Fader,
    Knob
)
from devices import DeviceShadow
from tests.helpers.devices import DummyDevice


@pytest.mark.parametrize(
    ['control', 'amount'],
    [
        (Note, 128),        # Device has 128 notes
        (PlayButton, 1),    # Device has a play button
        (Fader, 4),         # Device has 4 faders
        (Knob, 0),          # Device has no knobs
    ],
)
def test_get_num_matches(control: type[ControlSurface], amount: int):
    """Make sure we find all the matches for different control types"""
    s = DeviceShadow(DummyDevice())

    assert s.getNumControlMatches(control) == amount


@pytest.mark.parametrize(
    ['control', 'amount'],
    [
        (Note, 128),        # Device has 128 notes
        (PlayButton, 1),    # Device has a play button
        (Fader, 4),         # Device has 4 faders
        (Knob, 4),          # No knobs, but there are 4 faders as a backup
    ],
)
def test_get_num_matches_subs(control: type[ControlSurface], amount: int):
    """
    Make sure we find all the matches for different control types, but with
    substitution enabled
    """
    s = DeviceShadow(DummyDevice())

    assert s.getNumControlMatches(control, allow_substitution=True) == amount


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
    with pytest.raises(ValueError):
        s.bindControls(m, _dummy)
