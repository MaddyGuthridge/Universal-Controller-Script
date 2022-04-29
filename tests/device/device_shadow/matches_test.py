"""
tests > device_shadow_test

Tests to ensure device shadows bind controls correctly
"""

import pytest
# from common.types import EventData
from controlsurfaces import (
    ControlSurface,
    Note,
    PlayButton,
    StopButton,
    LoopButton,
    Fader,
    Knob,
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


def test_get_matches_target():
    """Make sure we get enough matches when we give a target number
    """
    s = DeviceShadow(DummyDevice())

    assert len(s.getControlMatches(Fader, target_num=2)) == 2


def test_get_matches_target_no_trim():
    """Make sure we get all matches when we give a target number, but choose
    not to trim
    """
    s = DeviceShadow(DummyDevice())

    assert len(s.getControlMatches(
        Fader,
        target_num=2,
        exact=False,
        trim=False
    )) == 4


def test_get_matches_target_no_trim_exact():
    """Make sure we get an error when we choose not to trim results then get
    too many (exact defaults to True)
    """
    s = DeviceShadow(DummyDevice())

    with pytest.raises(ValueError):
        s.getControlMatches(
            Fader,
            target_num=2,
            trim=False
        )


def test_get_matches_target_no_trim_exact_correct():
    """Make sure we don't get an error when we ask for an exact number, get
    that number then choose not to trim
    """
    s = DeviceShadow(DummyDevice())

    assert len(s.getControlMatches(
        Fader,
        target_num=4,
        trim=False
    )) == 4


def test_get_matches_target_exact():
    """Make sure we get the right number of matches when we give a target
    number, and choose to trim
    """
    s = DeviceShadow(DummyDevice())

    assert len(s.getControlMatches(
            Fader,
            target_num=2,
            exact=True,
        )) == 2


def test_get_matches_target_not_enough():
    """Make sure we get an error when there aren't enough matches for our
    target number
    """
    s = DeviceShadow(DummyDevice())

    with pytest.raises(ValueError):
        s.getControlMatches(
            Fader,
            target_num=8,
        )


def test_get_matches_target_not_enough_non_exact():
    """Make sure we get some matches when was ask for a certain amount
    """
    s = DeviceShadow(DummyDevice())

    assert len(s.getControlMatches(
        Fader,
        target_num=8,
        exact=False,
    )) == 4


def test_get_matches_none():
    """Make sure we don't get an error when there's no matches if we don't use
    the raise_on_zero flag
    """
    s = DeviceShadow(DummyDevice())

    assert len(s.getControlMatches(
        StopButton,
    )) == 0


def test_get_matches_none_raise():
    """Make sure we get an error when there's no matches if we use the
    raise_on_zero flag
    """
    s = DeviceShadow(DummyDevice())

    with pytest.raises(ValueError):
        s.getControlMatches(
            StopButton,
            raise_on_zero=True,
        )


def test_get_matches_subtypes():
    """Make sure that we get only one subtype when we don't disable the
    one_type flag
    """
    s = DeviceShadow(DummyDevice())

    assert len(s.getControlMatches(
        LoopButton,
    )) == 1


def test_get_matches_subtypes_one_type():
    """Make sure that we get all subtypes when we disable the one_type flag
    """
    s = DeviceShadow(DummyDevice())

    assert len(s.getControlMatches(
        LoopButton,
        one_type=False,
    )) == 2
