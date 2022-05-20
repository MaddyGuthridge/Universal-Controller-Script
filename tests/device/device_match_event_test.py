"""
tests > device_shadow_test

Tests to ensure device shadows bind controls correctly
"""

from common.types import EventData
from control_surfaces import Note, PlayButton, Fader
from tests.helpers.devices import DummyDevice


def test_match_note():
    """Can we match note events for our device"""
    d = DummyDevice()

    assert isinstance(d.matchEvent(EventData(0x9F, 0, 127)).getControl(), Note)


def test_match_button():
    """Can we match the play button"""
    d = DummyDevice()

    assert isinstance(
        d.matchEvent(EventData(0, 0, 0)).getControl(),
        PlayButton
    )


def test_match_faders():
    """Can we match the faders"""
    d = DummyDevice()
    for i in range(4):
        match = d.matchEvent(EventData(1, i, 0))
        assert isinstance(match.getControl(), Fader)
        assert match.getControl() == d.faders[i]
