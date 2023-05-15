"""
Tests for the grid mapper utility
"""


from common.util.grid_mapper import grid_map


def test_basic_mapping():
    assert grid_map(2, 2, 2, 2) == [
        [(0, 0, 0), (0, 0, 1)],
        [(0, 1, 0), (0, 1, 1)],
    ]


def test_leaves_empty_space():
    assert grid_map(3, 3, 2, 2) == [
        [(0, 0, 0), (0, 0, 1), None],
        [(0, 1, 0), (0, 1, 1), None],
        [None, None, None],
    ]


def test_fills_multiple():
    assert grid_map(4, 2, 2, 2) == [
        [(0, 0, 0), (0, 0, 1), (1, 0, 0), (1, 0, 1)],
        [(0, 1, 0), (0, 1, 1), (1, 1, 0), (1, 1, 1)],
    ]


def test_fills_in_expected_order():
    assert grid_map(4, 4, 2, 2) == [
        [(0, 0, 0), (0, 0, 1), (1, 0, 0), (1, 0, 1)],
        [(0, 1, 0), (0, 1, 1), (1, 1, 0), (1, 1, 1)],
        [(2, 0, 0), (2, 0, 1), (3, 0, 0), (3, 0, 1)],
        [(2, 1, 0), (2, 1, 1), (3, 1, 0), (3, 1, 1)],
    ]


def test_truncates():
    assert grid_map(3, 2, 4, 1, truncate_overflows=True) == [
        [(0, 0, 0), (0, 0, 1), (0, 0, 2)],
        [(1, 0, 0), (1, 0, 1), (1, 0, 2)],
    ]


def test_no_truncate_secondary_axis():
    assert grid_map(2, 2, 1, 3, truncate_overflows=True) == [
        [None, None],
        [None, None],
    ]


def test_truncates_tall():
    assert grid_map(2, 2, 3, 2, truncate_overflows=True) == [
        [(0, 0, 0), (0, 0, 1)],
        [(0, 1, 0), (0, 1, 1)],
    ]


def test_wraps():
    assert grid_map(3, 2, 4, 1, wrap_overflows=True) == [
        [(0, 0, 0), (0, 0, 1), (0, 0, 2)],
        [(0, 0, 3), None, None],
    ]


def test_wraps_multiple_groups():
    assert grid_map(3, 4, 4, 1, wrap_overflows=True) == [
        [(0, 0, 0), (0, 0, 1), (0, 0, 2)],
        [(0, 0, 3), None, None],
        [(1, 0, 0), (1, 0, 1), (1, 0, 2)],
        [(1, 0, 3), None, None],
    ]


def test_wraps_tall():
    assert grid_map(3, 4, 4, 2, wrap_overflows=True) == [
        [(0, 0, 0), (0, 0, 1), (0, 0, 2)],
        [(0, 1, 0), (0, 1, 1), (0, 1, 2)],
        [(0, 0, 3), None, None],
        [(0, 1, 3), None, None],
    ]
