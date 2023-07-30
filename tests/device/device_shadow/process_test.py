"""
tests > device_shadow_test

Tests to ensure device shadows bind controls correctly

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""

# import pytest
# from common.types import FlMidiMsg
from common.plug_indexes import WindowIndex
from control_surfaces import (
    ControlEvent,
    PlayButton,
)
from devices import DeviceShadow
from tests.helpers.devices import DummyDeviceBasic


def test_process_unbound():
    """Check that attempting to process events that aren't assigned doesn't
    give an error
    """
    s = DeviceShadow(DummyDeviceBasic())

    m = s.getControlMatches(PlayButton)[0]

    s.processEvent(ControlEvent(
        ...,  # type: ignore
        m.getControl(),
        0.0,
        0,
        False,
    ), WindowIndex.MIXER)
