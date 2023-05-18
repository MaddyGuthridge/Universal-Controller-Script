"""
# src / common / util / grid_mapper

Code to map groups of elements onto an overall grid.

## TODO

Some features are currently untested which may be required for some layouts.

* Support for vertical-before-horizontal filling
* Support for fill directions
"""
import math
from typing import Optional


def fill_in_group(
    grid: list[list[Optional[int]]],
    width: int,
    height: int,
    group_width: int,
    group_height: int,
    group_num: int,
    row: int,
    col: int,
    truncate_overflows: bool,
    wrap_overflows: bool,
    horizontal_before_vertical: bool,
) -> tuple[list[list[Optional[int]]], int]:
    """
    Fill in a group number to the specified region on the grid.

    ### Args:
    * `grid` (`list[list[Optional[int]]]`): grid to fill into

    * `width` (`int`): width of the overall grid

    * `height` (`int`): height of the overall grid

    * `group_width` (`int`): width of the group

    * `group_height` (`int`): height of the group

    * `group_num` (`int`): group number to fill

    * `row` (`int`): starting row of group

    * `col` (`int`): starting column of group

    * `truncate_overflows` (`bool`): whether to truncate overflows for the
      group

    * `wrap_overflows` (`bool`): whether to wrap overflows for the group

    * `horizontal_before_vertical` (`bool`, optional): Whether to fill groups
      horizontally first or vertically first.

    ### Returns:

    * `list[list[Optional[int]]]`: new grid

    * `int`: amount to increment the group number by
    """
    grid_copy = [[i for i in o] for o in grid]
    # Yuck
    filled_items = 0
    while True:
        try:
            for curr_row in range(row, row + group_height):
                og_row = curr_row
                for curr_col in range(col, col + group_width):
                    # Reset the row each iteration to fix issues with long
                    # wraps
                    curr_row = og_row
                    # Check if we've filled enough items
                    if filled_items == group_width * group_height:
                        raise StopIteration()
                    # If it's out of range, we need to wrap it
                    # Past the right-hand edge
                    if curr_col >= width:
                        if truncate_overflows and horizontal_before_vertical:
                            # We still need to fill the rest of the row
                            # Pretend we filled in all those other items
                            filled_items += width - group_width
                            break
                        elif wrap_overflows:
                            # Fill it in on a later row instead
                            curr_row += curr_col // width * group_height
                            curr_col = curr_col % width
                        else:
                            # Can't place this group
                            return grid, 0
                    if curr_row >= height:
                        if (
                            truncate_overflows
                            and not horizontal_before_vertical
                        ):
                            # We've filled enough
                            return grid_copy, 1
                        elif wrap_overflows:
                            # Fill it in on a later column instead
                            curr_col += curr_row // height * group_width
                            curr_row = curr_row % height
                        else:
                            # Can't place this group
                            return grid, 0
                    # If we reach this point, we can fill it normally
                    grid_copy[curr_row][curr_col] = group_num
                    filled_items += 1
        except StopIteration:
            # If we've filled all the items
            if filled_items == group_width * group_height:
                break
            # Or if we went off the end
            elif horizontal_before_vertical and row >= height:
                break
            elif not horizontal_before_vertical and col >= width:
                break
            # Otherwise, keep trying to fill things in
            else:
                continue
        break
    return grid_copy, 1


def template_map_to_index_map(
    grid: list[list[Optional[int]]],
    width: int,
    height: int,
    group_width: int,
    group_height: int,
    horizontal_before_vertical: bool,
) -> list[list[Optional[tuple[int, int, int]]]]:
    """
    Map group numbers in a grid to a new grid where each cell is a tuple
    containing the group number, row and column within the group.
    """
    result: list[list[Optional[tuple[int, int, int]]]] = \
        [[None] * width for _ in range(height)]

    # Starting indexes of each group, used to calculate the indexes for each
    # element in the group
    group_starts: dict[int, tuple[int, int]] = {}
    if horizontal_before_vertical:
        for row in range(height):
            for col in range(width):
                group_number = grid[row][col]
                if (
                    group_number is not None
                    and group_number not in group_starts
                ):
                    group_starts[group_number] = (row, col)
    else:
        for col in range(width):
            for row in range(height):
                group_number = grid[row][col]
                if (
                    group_number is not None
                    and group_number not in group_starts
                ):
                    group_starts[group_number] = (row, col)

    # Now go and calculate the offsets for each index
    for row in range(height):
        for col in range(width):
            if (group_number := grid[row][col]) is not None:
                start_row, start_col = group_starts[group_number]
                # Calculate offsets
                off_row = row - start_row
                off_col = col - start_col
                # Adjust if it goes past the end of the indexes
                if horizontal_before_vertical:
                    # rows fill first
                    off_col += off_row // group_height * width
                    off_row %= group_height
                else:
                    # columns fill first
                    off_row += off_col // group_width * height
                    off_col %= group_width
                result[row][col] = (
                    group_number,
                    off_row,
                    off_col,
                )

    return result


def grid_map(
    width: int,
    height: int,
    group_width: int,
    group_height: int,
    left_to_right: bool = True,
    top_to_bottom: bool = True,
    horizontal_before_vertical: bool = True,
    truncate_overflows: bool = False,
    wrap_overflows: bool = False,
) -> list[list[Optional[tuple[int, int, int]]]]:
    """
    Map groups of elements to an overall grid of the given width and height.

    This returns a 2D of the shape of the overall grid, with each element being
    a three-element tuple of `(group_num, row, col)`, where `group_num` is the
    index of the group it belongs to, `row` is the row within that group, and
    `col` is the column within that group.

    ### Args:
    * `width` (`int`): width of the overall grid

    * `height` (`int`): height of the overall grid

    * `group_width` (`int`): width of each group

    * `group_height` (`int`): height of each group

    * `left_to_right` (`bool`, optional): whether to place groups
      left-to-right (`True`) or right-to-left (`False`). Defaults to `True`.

    * `top_to_bottom` (`bool`, optional): whether to place groups
      top-to-bottom (`True`) or bottom-to-top (`False`). Defaults to `True`.

    * `horizontal_before_vertical` (`bool`, optional): Whether to fill groups
      horizontally first or vertically first. If `True`, elements are filled
      across, then vertically once each row is filled. Defaults to `True`.

    * `truncate_overflows` (`bool`, optional): whether to truncate groups that
      are too big to fit into the group (`True`) or to not place them at all
      (`False`). Defaults to `False`.

    * `wrap_overflows` (`bool`, optional): whether to wrap groups that
      are too big to fit into the group (`True`) or to not place them at all
      (`False`). Defaults to `False`.
    """
    # A template grid - instead of filling each group element, we'll just say
    # which group goes where and figure out the specific elements later
    template_grid: list[list[Optional[int]]] = \
        [[None] * width for _ in range(height)]

    # All of the following operations assume left-to-right, top-to-bottom
    # We can then transform the result as required afterwards

    # Figure out what an overall shape looks like (accounting for wrapping and
    # the like)
    if group_width < width:
        group_calc_width = group_width
        height_multiplier = 1
    else:
        group_calc_width = width
        if truncate_overflows:
            height_multiplier = 1
        else:
            height_multiplier = math.ceil(group_width / width)
    apparent_group_height = group_height * height_multiplier
    if apparent_group_height < height:
        group_calc_height = apparent_group_height
    else:
        group_calc_height = height
        # We might be able to wrap it
        if not truncate_overflows:
            # But only if there's enough horizontal space
            width_multiplier = math.ceil(group_height / width)
            if group_calc_width * width_multiplier <= width:
                # There was enough space
                group_calc_width *= width_multiplier

    # Keep track of how many groups we've filled
    group_number = 0

    if horizontal_before_vertical:
        for row in range(0, height, group_calc_height):
            for col in range(0, width, group_calc_width):
                # Fill in the group
                template_grid, inc = fill_in_group(
                    template_grid,
                    width,
                    height,
                    group_width,
                    group_height,
                    group_number,
                    row,
                    col,
                    truncate_overflows,
                    wrap_overflows,
                    horizontal_before_vertical,
                )
                group_number += inc
    else:
        for col in range(0, width, group_calc_width):
            for row in range(0, height, group_calc_height):
                # Fill in the group
                template_grid, inc = fill_in_group(
                    template_grid,
                    width,
                    height,
                    group_width,
                    group_height,
                    group_number,
                    row,
                    col,
                    truncate_overflows,
                    wrap_overflows,
                    horizontal_before_vertical,
                )
                group_number += inc

    # Now flip it if required
    if not left_to_right:
        for row_list in template_grid:
            row_list.reverse()
    if not top_to_bottom:
        template_grid.reverse()

    return template_map_to_index_map(
        template_grid,
        width,
        height,
        group_width,
        group_height,
        horizontal_before_vertical,
    )
