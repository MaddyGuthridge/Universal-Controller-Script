"""
tests > matchers > index_test

Tests for the IndexedMatcher

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""
# import pytest
from fl_classes import FlMidiMsg
from common.util.events import encodeForwardedEvent
from control_surfaces.matchers import IndexedMatcher
from tests.helpers.controls import SimpleControl, SimpleForwardedControl
from tests.helpers.devices import DummyDeviceContext


def test_index():
    """Test matching things with IndexedMatcher"""
    controls = [SimpleControl(i) for i in range(10)]
    matcher = IndexedMatcher(
        status=0,
        data1_start=0,
        controls=controls,
    )
    for i in range(10):
        assert matcher.matchEvent(  # type: ignore
            FlMidiMsg(0, i, 0)).getControl() is controls[i]


def test_no_match():
    """Test when there's no match"""
    matcher = IndexedMatcher(
        status=0,
        data1_start=0,
        controls=[SimpleControl(i) for i in range(10)],
    )
    assert matcher.matchEvent(FlMidiMsg(0, 10, 0)) is None


def test_forwarded():
    """Test that we can still match forwarded events"""
    with DummyDeviceContext(2):
        event = FlMidiMsg(encodeForwardedEvent(FlMidiMsg(0, 10, 0), 2))
    with DummyDeviceContext(1):
        matcher = IndexedMatcher(
            status=0,
            data1_start=0,
            controls=[SimpleForwardedControl(i) for i in range(10)],
            device=2
        )
        assert matcher.matchEvent(event) is None


# Removed until I can find a proper way to implement this functionality
# def test_invalid_controls():
#     """
#     Test we get an error when we try to bind controls where they don't match
#     the overall pattern generated.
#     """
#     # Invalid status
#     with pytest.raises(ValueError):
#         IndexedMatcher(
#             status=1,
#             data1_start=0,
#             controls=[SimpleControl(i) for i in range(10)],
#         )
#     # Bad data1 start
#     with pytest.raises(ValueError):
#         IndexedMatcher(
#             status=0,
#             data1_start=1,
#             controls=[SimpleControl(i) for i in range(10)],
#         )
