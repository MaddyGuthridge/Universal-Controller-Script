"""
Tests for the grid mapper utility
"""
from jestspectation import ObjectContainingItems, Any
from common.util.grid_mapper import grid_map, GridCell


def cell_in(group_number: int):
    return ObjectContainingItems({'group_number': group_number})


def cell_at(row: int, col: int):
    return ObjectContainingItems({'row': row, 'col': col})


def cell_at_index(group_index: int):
    return ObjectContainingItems({'group_index': group_index})


def test_basic_mapping_group():
    assert grid_map(2, 2, 2, 2) == [
        [cell_in(0), cell_in(0)],
        [cell_in(0), cell_in(0)],
    ]


def test_basic_mapping_row_col():
    assert grid_map(2, 2, 2, 2) == [
        [
            cell_at(0, 0),
            cell_at(0, 1),
        ],
        [
            cell_at(1, 0),
            cell_at(1, 1),
        ],
    ]


def test_basic_mapping_index():
    assert grid_map(2, 2, 2, 2) == [
        [cell_at_index(0), cell_at_index(1)],
        [cell_at_index(2), cell_at_index(3)],
    ]


def test_leaves_empty_space():
    assert grid_map(3, 3, 2, 2) == [
        [Any(GridCell), Any(GridCell), None],
        [Any(GridCell), Any(GridCell), None],
        [None, None, None],
    ]


def test_fills_multiple():
    assert grid_map(4, 2, 2, 2) == [
        [cell_in(0), cell_in(0), cell_in(1), cell_in(1)],
        [cell_in(0), cell_in(0), cell_in(1), cell_in(1)],
    ]


def test_fills_in_expected_order():
    assert grid_map(4, 4, 2, 2) == [
        [cell_in(0), cell_in(0), cell_in(1), cell_in(1)],
        [cell_in(0), cell_in(0), cell_in(1), cell_in(1)],
        [cell_in(2), cell_in(2), cell_in(3), cell_in(3)],
        [cell_in(2), cell_in(2), cell_in(3), cell_in(3)],
    ]


def test_unset_width():
    assert grid_map(4, 2, None, 1) == [
        [cell_in(0), cell_in(0), cell_in(0), cell_in(0)],
        [cell_in(1), cell_in(1), cell_in(1), cell_in(1)],
    ]


def test_unset_height():
    assert grid_map(4, 3, 2, None) == [
        [cell_in(0), cell_in(0), cell_in(1), cell_in(1)],
        [cell_in(0), cell_in(0), cell_in(1), cell_in(1)],
        [cell_in(0), cell_in(0), cell_in(1), cell_in(1)],
    ]


def test_truncates():
    assert grid_map(3, 2, 4, 1, truncate_overflows=True) == [
        [cell_at_index(0), cell_at_index(1), cell_at_index(2)],
        [cell_at_index(0), cell_at_index(1), cell_at_index(2)],
    ]


def test_no_truncate_secondary_axis():
    """
    Truncate only affects the primary axis - if the secondary axis is too tall
    then nothing is filled
    """
    assert grid_map(2, 2, 1, 3, truncate_overflows=True) == [
        [None, None],
        [None, None],
    ]


def test_truncates_tall():
    assert grid_map(2, 2, 3, 2, truncate_overflows=True) == [
        [cell_at_index(0), cell_at_index(1)],
        [cell_at_index(3), cell_at_index(4)],
    ]


def test_wraps():
    assert grid_map(3, 2, 4, 1, wrap_overflows=True) == [
        [cell_at_index(0), cell_at_index(1), cell_at_index(2)],
        [cell_at_index(3), None, None],
    ]


def test_wraps_multiple_groups():
    assert grid_map(3, 4, 4, 1, wrap_overflows=True) == [
        [cell_in(0), cell_in(0), cell_in(0)],
        [cell_in(0), None, None],
        [cell_in(1), cell_in(1), cell_in(1)],
        [cell_in(1), None, None],
    ]


def test_wraps_tall():
    assert grid_map(3, 4, 4, 2, wrap_overflows=True) == [
        [cell_at(0, 0), cell_at(0, 1), cell_at(0, 2)],
        [cell_at(1, 0), cell_at(1, 1), cell_at(1, 2)],
        [cell_at(0, 3), None, None],
        [cell_at(1, 3), None, None],
    ]


def test_wraps_long_row():
    assert grid_map(3, 3, 8, 1, wrap_overflows=True) == [
        [cell_at_index(0), cell_at_index(1), cell_at_index(2)],
        [cell_at_index(3), cell_at_index(4), cell_at_index(5)],
        [cell_at_index(6), cell_at_index(7), None],
    ]


def test_bottom_to_top():
    assert grid_map(4, 4, 4, 2, top_to_bottom=False) == [
        [cell_in(1), cell_in(1), cell_in(1), cell_in(1)],
        [cell_in(1), cell_in(1), cell_in(1), cell_in(1)],
        [cell_in(0), cell_in(0), cell_in(0), cell_in(0)],
        [cell_in(0), cell_in(0), cell_in(0), cell_in(0)],
    ]


def test_indexes_bottom_to_top():
    assert grid_map(2, 4, 2, 2, top_to_bottom=False) == [
        [cell_at_index(0), cell_at_index(1)],
        [cell_at_index(2), cell_at_index(3)],
        [cell_at_index(0), cell_at_index(1)],
        [cell_at_index(2), cell_at_index(3)],
    ]
    assert grid_map(2, 4, 2, 2, top_to_bottom=False) == [
        [cell_at(0, 0), cell_at(0, 1)],
        [cell_at(1, 0), cell_at(1, 1)],
        [cell_at(0, 0), cell_at(0, 1)],
        [cell_at(1, 0), cell_at(1, 1)],
    ]
