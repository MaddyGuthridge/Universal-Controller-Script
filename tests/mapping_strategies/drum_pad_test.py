"""
tests > mapping_strategies > drum_pad_test.py

Tests for mapping strategies

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""
import pytest
from devices import DeviceShadow
from plugs.mapping_strategies import DrumPadStrategy
from common.plug_indexes import UnsafeIndex
from common.types import Color
from control_surfaces import ControlShadowEvent, ControlShadow, DrumPad
from tests.helpers.devices import DummyDeviceDrumPads


class Flag:
    """
    Helper class for checking if a property has changed
    """
    def __init__(self) -> None:
        self.is_set = False
        self.count = 0

    def __repr__(self) -> str:
        return f"Flag(is_set={self.is_set}, count={self.count})"

    def set(self):
        self.is_set = True
        self.count += 1


def matrixToDict(matrix: list[list[int]]) -> dict[int, tuple[int, int]]:
    """
    Convert a matrix of indexes to a reverse lookup dictionary

    ### Args:
    * `matrix` (`list[list[int]]`): matrix to convert

    ### Returns:
    * `dict[int, tuple[int, int]]`: converted values
    """
    mappings: dict[int, tuple[int, int]] = {}
    for r in range(len(matrix)):
        for c in range(len(matrix[r])):
            mappings[matrix[r][c]] = (r, c)
    return mappings


def triggerCallbackGenerator(expected_index: int, flag: Flag):
    """
    Generates a callback in order to check that indexes were created correctly.

    The callback will check that the index matches, and then set the flag.

    ### Args:
    * `expected_index` (`int`): the index you're expecting
    """
    def callback(event: ControlShadowEvent, plug: UnsafeIndex, index: int):
        assert index == expected_index
        flag.set()
        return True
    return callback


def colorizeCallbackGenerator(
    index_matrix: list[list[int]],
    flag: Flag,
):
    """
    Generates a callback in order to check that indexes were created correctly.

    The callback will check that the index matches, and then set the flag.

    ### Args:
    * `expected_index` (`int`): the index you're expecting
    """
    index_lookup = matrixToDict(index_matrix)

    def callback(event: ControlShadow, plug: UnsafeIndex, index: int):
        assert index_lookup[index] == event.coordinate
        flag.set()
        return Color.fromGrayscale(1)
    return callback


def annotateCallbackGenerator(
    index_matrix: list[list[int]],
    flag: Flag,
):
    """
    Generates a callback in order to check that indexes were created correctly.

    The callback will check that the index matches, and then set the flag.

    ### Args:
    * `expected_index` (`int`): the index you're expecting
    """
    index_lookup = matrixToDict(index_matrix)

    def callback(event: ControlShadow, plug: UnsafeIndex, index: int):
        assert index_lookup[index] == event.coordinate
        flag.set()
        return "My annotation"
    return callback


def test_cant_create_with_invalid_height():
    """
    Do we get a ValueError when we attempt to create a drum pad mapping
    strategy with a specified height but unspecified width?
    """
    with pytest.raises(ValueError):
        DrumPadStrategy(-1, 2, True, triggerCallbackGenerator(0, Flag()))


def test_callback_reached():
    """
    Do events actually reach the callback function?
    """
    device = DummyDeviceDrumPads(4, 4)
    flag = Flag()
    strategy = DrumPadStrategy(-1, -1, True, triggerCallbackGenerator(0, flag))
    # Create the bindings
    shadow = DeviceShadow(device)
    strategy.apply(shadow)

    # Now process the event
    assert shadow.processEvent(
        device.matchEvent(device.getEventForDrumPad(0, 0, 0)),  # type: ignore
        0,
    )
    # And check that the callback was reached
    assert flag.is_set


def test_basic_coordinates_rows():
    """
    When we create the bindings with no specific constraints, do the
    controls bind from left to right, top to bottom?

       |
       V
    0  1  2  3
    4  5  6  7
    8  9  10 11
    12 13 14 15
    """
    device = DummyDeviceDrumPads(4, 4)
    flag = Flag()
    strategy = DrumPadStrategy(-1, -1, True, triggerCallbackGenerator(1, flag))
    # Create the bindings
    shadow = DeviceShadow(device)
    strategy.apply(shadow)

    # Now process the event
    assert shadow.processEvent(
        device.matchEvent(device.getEventForDrumPad(0, 1, 0)),  # type: ignore
        0,
    )
    # And check that the callback was reached
    assert flag.is_set


def test_basic_coordinates_cols():
    """
    When we create the bindings with no specific constraints, do the
    controls bind from left to right, top to bottom?

        0  1  2  3
    --> 4  5  6  7
        8  9  10 11
        12 13 14 15
    """
    device = DummyDeviceDrumPads(4, 4)
    flag = Flag()
    strategy = DrumPadStrategy(-1, -1, True, triggerCallbackGenerator(4, flag))
    # Create the bindings
    shadow = DeviceShadow(device)
    strategy.apply(shadow)

    # Now process the event
    assert shadow.processEvent(
        device.matchEvent(device.getEventForDrumPad(1, 0, 0)),  # type: ignore
        0,
    )
    # And check that the callback was reached
    assert flag.is_set


def test_limited_width():
    """
    When we create the bindings with constraints on the width, do the values
    wrap around correctly.

        0  1  8  9
    --> 2  3  10 11
        4  5  12 13
        6  7  14 15
    """
    device = DummyDeviceDrumPads(4, 4)
    flag = Flag()
    strategy = DrumPadStrategy(2, -1, True, triggerCallbackGenerator(2, flag))
    # Create the bindings
    shadow = DeviceShadow(device)
    strategy.apply(shadow)

    # Now process the event
    assert shadow.processEvent(
        device.matchEvent(device.getEventForDrumPad(1, 0, 0)),  # type: ignore
        0,
    )
    # And check that the callback was reached
    assert flag.is_set


def test_limited_width_column_groups():
    """
    When we create the bindings with constraints on the width, do we get
    multiple columns if available?

          |
          V
    0  1  8  9
    2  3  10 11
    4  5  12 13
    6  7  14 15
    """
    device = DummyDeviceDrumPads(4, 4)
    flag = Flag()
    strategy = DrumPadStrategy(2, -1, True, triggerCallbackGenerator(8, flag))
    # Create the bindings
    shadow = DeviceShadow(device)
    strategy.apply(shadow)

    # Now process the event
    assert shadow.processEvent(
        device.matchEvent(device.getEventForDrumPad(0, 2, 0)),  # type: ignore
        0,
    )
    # And check that the callback was reached
    assert flag.is_set


def test_limited_height():
    """
    When we create the bindings with constraints on the width and height, do
    the values wrap around correctly?

          |
          V
    0  1  4  5
    2  3  6  7
    8  9  12 13
    10 11 14 15
    """
    device = DummyDeviceDrumPads(4, 4)
    flag = Flag()
    strategy = DrumPadStrategy(2, 2, True, triggerCallbackGenerator(4, flag))
    # Create the bindings
    shadow = DeviceShadow(device)
    strategy.apply(shadow)

    # Now process the event
    assert shadow.processEvent(
        device.matchEvent(device.getEventForDrumPad(0, 2, 0)),  # type: ignore
        0,
    )
    # And check that the callback was reached
    assert flag.is_set


def test_limited_height_wraps_around():
    """
    When we create the bindings with constraints on the width and height, do
    the values wrap around correctly?

        0  1  4  5
        2  3  6  7
    --> 8  9  12 13
        10 11 14 15
    """
    device = DummyDeviceDrumPads(4, 4)
    flag = Flag()
    strategy = DrumPadStrategy(2, 2, True, triggerCallbackGenerator(8, flag))
    # Create the bindings
    shadow = DeviceShadow(device)
    strategy.apply(shadow)

    # Now process the event
    assert shadow.processEvent(
        device.matchEvent(device.getEventForDrumPad(2, 0, 0)),  # type: ignore
        0,
    )
    # And check that the callback was reached
    assert flag.is_set


def test_colorize_annotate():
    """
    Are the drum pads colored and annotated correctly?

    We check that the colorize and annotate callbacks are called 16 times each,
    that all the indexes match up, and that the colors and annotations are set
    correctly.
    """
    device = DummyDeviceDrumPads(4, 4)
    layout = [
        [0,  1,  2,  3],
        [4,  5,  6,  7],
        [8,  9,  10, 11],
        [12, 13, 14, 15],
    ]
    flag = Flag()
    strategy = DrumPadStrategy(
        -1,
        -1,
        True,
        triggerCallbackGenerator(0, flag),
        colorizeCallbackGenerator(layout, flag),
        annotateCallbackGenerator(layout, flag),
    )
    # Create the bindings
    shadow = DeviceShadow(device)
    strategy.apply(shadow)

    # Now colorize each one
    shadow.tick(0)

    # The flag should have been set twice for each drum pad (once for each
    # callback)
    assert flag.count == 32

    # Check the annotations and colors
    shadow.apply(False)
    for row in device.drums:
        for drum in row:
            assert drum.color == Color.fromGrayscale(1)
            assert drum.annotation == "My annotation"


def test_colorize_annotate_ignore_unmapped():
    """
    Are the drum pads colored and annotated correctly?

    We check that the colorize and annotate callbacks are not called for
    unmapped controls, that all the indexes match up, and that the colors and
    annotations for unmapped controls are unset.
    """
    device = DummyDeviceDrumPads(4, 4)
    layout = [
        [0,  1,  2,  -1],
        [3,  4,  5,  -1],
        [6,  7,  8, -1],
        [9, 10, 11, -1],
    ]
    flag = Flag()
    strategy = DrumPadStrategy(
        3,
        -1,
        True,
        triggerCallbackGenerator(0, flag),
        colorizeCallbackGenerator(layout, flag),
        annotateCallbackGenerator(layout, flag),
    )
    # Create the bindings
    shadow = DeviceShadow(device)
    strategy.apply(shadow)

    # Now colorize each one
    shadow.tick(0)

    # The flag should have been set twice for each drum pad, but not for
    # unassigned ones
    assert flag.count == 24

    # Check the annotations and colors
    shadow.apply(False)
    for row in device.drums:
        # The unmapped drums shouldn't be colored or annotated
        drum = row[3]
        assert drum.color == Color()
        assert drum.annotation == ""


def test_colorize_annotate_defaults():
    """
    Are the drum pads colored and annotated correctly when using the default
    callbacks?
    """
    device = DummyDeviceDrumPads(4, 4)
    flag = Flag()
    strategy = DrumPadStrategy(
        -1,
        -1,
        True,
        triggerCallbackGenerator(0, flag),
    )
    # Create the bindings
    shadow = DeviceShadow(device)
    strategy.apply(shadow)

    # Now colorize each one
    shadow.tick(0)

    # Check the annotations and colors
    shadow.apply(False)
    for row in device.drums:
        for drum in row:
            assert drum.color == Color.fromGrayscale(0.3)
            assert drum.annotation == ""


def test_unassigned_column():
    """
    When we make the columns wrap around, but there aren't enough remaining
    columns to create a full column group, the remaining columns are ignored.

             |
             V
    0  1  2  x
    3  4  5  x
    6  7  8  x
    9  10 11 x
    """
    device = DummyDeviceDrumPads(4, 4)
    flag = Flag()
    strategy = DrumPadStrategy(3, -1, True, triggerCallbackGenerator(0, flag))
    # Create the bindings
    shadow = DeviceShadow(device)
    strategy.apply(shadow)

    # Now process the event
    # Even though it is ignored, it should still be handled
    assert shadow.processEvent(
        device.matchEvent(device.getEventForDrumPad(0, 3, 0)),  # type: ignore
        0,
    )
    # And check that the callback was not reached
    assert not flag.is_set


def test_unassigned_row():
    """
    When we make the rows wrap around, but there aren't enough remaining
    rows to create a full row group, the remaining rows are ignored.

        0  1  2  3
        4  5  6  7
        8  9  10 11
    --> x  x  x  x
    """
    device = DummyDeviceDrumPads(4, 4)
    flag = Flag()
    strategy = DrumPadStrategy(4, 3, True, triggerCallbackGenerator(0, flag))
    # Create the bindings
    shadow = DeviceShadow(device)
    strategy.apply(shadow)

    # Now process the event
    # Even though it is ignored, it should still be handled
    assert shadow.processEvent(
        device.matchEvent(device.getEventForDrumPad(3, 0, 0)),  # type: ignore
        0,
    )
    # And check that the callback was not reached
    assert not flag.is_set


def test_prevent_updates():
    """
    Are the colors and annotations only updated once if the
    `do_property_update` is set to `False`?
    """
    device = DummyDeviceDrumPads(4, 4)
    layout = [
        [0,  1,  2,  3],
        [4,  5,  6,  7],
        [8,  9,  10, 11],
        [12, 13, 14, 15],
    ]
    flag = Flag()
    strategy = DrumPadStrategy(
        -1,
        -1,
        False,
        triggerCallbackGenerator(0, flag),
        colorizeCallbackGenerator(layout, flag),
        annotateCallbackGenerator(layout, flag),
    )
    # Create the bindings
    shadow = DeviceShadow(device)
    strategy.apply(shadow)

    # Tick it twice
    shadow.tick(0)
    shadow.tick(0)

    # The flag should have been set twice for each drum pad,
    # once for the color and once for the annotation
    # It won't be four times, even though we ticked it twice
    assert flag.count == 32


def test_error_when_drums_already_assigned():
    """
    Do we get a ValueError when we try to use this with another mapping
    strategy on this plugin that assigns drum pads
    """
    device = DummyDeviceDrumPads(4, 4)
    shadow = DeviceShadow(device)

    def callback(*args, **kwargs) -> bool: return True

    # Assign a few drum pads
    shadow.bindMatches(DrumPad, callback, target_num=3)

    # Now when we try to bind the matcher it will fail
    strategy = DrumPadStrategy(
        -1,
        -1,
        False,
        triggerCallbackGenerator(0, Flag()),
    )
    with pytest.raises(ValueError):
        strategy.apply(shadow)


def test_invert_rows():
    """
    Can we invert rows correctly?
    """
    device = DummyDeviceDrumPads(4, 4)
    layout = [
        [12, 13, 14, 15],
        [8,  9,  10, 11],
        [4,  5,  6,  7],
        [0,  1,  2,  3],
    ]
    strategy = DrumPadStrategy(
        -1,
        -1,
        False,
        triggerCallbackGenerator(0, Flag()),
        colorizeCallbackGenerator(layout, Flag()),
        invert_rows=True
    )
    # Create the bindings
    shadow = DeviceShadow(device)
    strategy.apply(shadow)

    # Tick it, which will ensure the correct layout
    shadow.tick(0)


def test_invert_rows_ignores_empty():
    """
    When we invert the rows, does it leave empty rows at the bottom?
    """
    device = DummyDeviceDrumPads(4, 4)
    layout = [
        [8,   9, 10, 11],
        [4,   5,  6,  7],
        [0,   1,  2,  3],
        [-1, -1, -1, -1],
    ]
    strategy = DrumPadStrategy(
        4,
        3,
        False,
        triggerCallbackGenerator(0, Flag()),
        colorizeCallbackGenerator(layout, Flag()),
        invert_rows=True
    )
    # Create the bindings
    shadow = DeviceShadow(device)
    strategy.apply(shadow)

    # Tick it, which will ensure the correct layout
    shadow.tick(0)


def test_subdivide_when_lacking_height():
    """
    When we try to assign a 4x4 grid onto a 2x8 grid, does it wrap around so
    that all the tiles can still be used correctly?

    0  1  2  3
    4  5  6  7   -->  0  1  2  3  8  9  10 11
    8  9  10 11       4  5  6  7  12 13 14 15
    12 13 14 15
    """
    flag = Flag()
    device = DummyDeviceDrumPads(2, 8)
    strategy = DrumPadStrategy(
        4,
        4,
        True,
        triggerCallbackGenerator(8, flag)
    )
    # Create the bindings
    shadow = DeviceShadow(device)
    strategy.apply(shadow)

    # Now process the event
    # Even though it is ignored, it should still be handled
    assert shadow.processEvent(
        device.matchEvent(device.getEventForDrumPad(0, 4, 0)),  # type: ignore
        0,
    )
    # And check that the callback was not reached
    assert flag.is_set


def test_subdivide_when_lacking_width():
    """
    When we try to assign a 2x8 grid onto a 4x4 grid, does it wrap around so
    that all the tiles can still be used correctly?

                                 0  1  2  3
    0  1  2  3  4  5  6  7   ->  4  5  6  7
    8  9  10 11 12 13 14 15      8  9  10 11
                                 12 13 14 15
    """
    flag = Flag()
    device = DummyDeviceDrumPads(2, 8)
    strategy = DrumPadStrategy(
        4,
        4,
        True,
        triggerCallbackGenerator(8, flag)
    )
    # Create the bindings
    shadow = DeviceShadow(device)
    strategy.apply(shadow)

    # Now process the event
    # Even though it is ignored, it should still be handled
    assert shadow.processEvent(
        device.matchEvent(device.getEventForDrumPad(0, 4, 0)),  # type: ignore
        0,
    )
    # And check that the callback was not reached
    assert flag.is_set
