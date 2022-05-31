"""
tests > matchers > index_test

Tests for the IndexedMatcher

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
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


def test_no_match():
    """Test when there's no match"""
    matcher = IndexedMatcher(
        status=0,
        data1=0,
        controls=[SimpleControl(i) for i in range(10)],
    )
    assert matcher.matchEvent(EventData(0, 10, 0)) is None
