"""
tests > matchers > basic_test

Tests for the BasicControlMatcher
"""
from common.types import EventData
from devices.matchers import IndexedMatcher
from tests.helpers.controls import SimpleControl


def test_index():
    """Test matching things with IndexedMatcher"""
    controls = [SimpleControl(i) for i in range(10)]
    matcher = IndexedMatcher(
        status=0,
        data1=0,
        controls=controls,
    )
    for i in range(10):
        assert matcher.matchEvent(EventData(0, i, 0)).getControl()\
            is controls[i]


def test_get_controls_groups():
    """Test getting controls"""
    controls = [SimpleControl(i) for i in range(10)]
    matcher = IndexedMatcher(
        status=0,
        data1=0,
        controls=controls,
    )
    assert matcher.getControls() == controls
    assert matcher.getGroups() == {"group"}


def test_no_match():
    """Test when there's no match"""
    matcher = IndexedMatcher(
        status=0,
        data1=0,
        controls=[SimpleControl(i) for i in range(10)],
    )
    assert matcher.matchEvent(EventData(0, 10, 0)) is None
