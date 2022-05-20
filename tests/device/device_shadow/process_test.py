"""
tests > device_shadow_test

Tests to ensure device shadows bind controls correctly
"""

# import pytest
# from common.types import EventData
from control_surfaces import (
    ControlEvent,
    PlayButton,
)
from devices import DeviceShadow
from tests.helpers.devices import DummyDevice


def test_process_unbound():
    """Check that attempting to process events that aren't assigned doesn't
    give an error
    """
    s = DeviceShadow(DummyDevice())

    m = s.getControlMatches(PlayButton)[0]

    s.processEvent(ControlEvent(m.getControl(), 0.0, 0, False), None)
