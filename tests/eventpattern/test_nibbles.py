"""
tests > eventpattern > test_nibbles

Tests generating event patterns from nibbles
"""

import pytest

from common.eventpattern import fromNibbles


def test_basic():
    assert fromNibbles(1, 2) == (0x12, )


def test_ellipsis():
    n = fromNibbles(5, ...)
    for i in range(16):
        assert 0x50 + i in n


@pytest.mark.parametrize(
    'r',
    [
        range(1, 10),
        range(2, 8, 2),
        range(5)
    ]
)
def test_range(r):
    n = fromNibbles(2, r)

    for i in r:
        assert 0x20 + i in n

    n = fromNibbles(r, 2)
    for i in r:
        assert (i << 4) + 2 in n
