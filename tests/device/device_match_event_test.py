"""
tests > device_match_event_test

Tests to ensure device shadows bind controls correctly

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""

from fl_classes import FlMidiMsg
from control_surfaces import Note, PlayButton, Fader
from tests.helpers.devices import DummyDeviceBasic


def test_match_note():
    """Can we match note events for our device"""
    d = DummyDeviceBasic()

    assert isinstance(
        d.matchEvent(FlMidiMsg(0x9F, 0, 127)).getControl(),  # type: ignore
        Note,
    )


def test_match_button():
    """Can we match the play button"""
    d = DummyDeviceBasic()

    assert isinstance(
        d.matchEvent(FlMidiMsg(0, 0, 0)).getControl(),  # type: ignore
        PlayButton
    )


def test_match_faders():
    """Can we match the faders"""
    d = DummyDeviceBasic()
    for i in range(4):
        match = d.matchEvent(FlMidiMsg(1, i, 0))
        assert match is not None
        assert isinstance(match.getControl(), Fader)
        assert match.getControl() == d.faders[i]
