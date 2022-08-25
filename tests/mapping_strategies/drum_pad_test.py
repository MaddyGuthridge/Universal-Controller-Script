"""
tests > mapping_strategies > drum_pad_test.py

Tests for mapping strategies

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""
from devices import DeviceShadow
from plugs.mapping_strategies import DrumPadStrategy
from common.plug_indexes import UnsafeIndex
from common.types import Color
from control_surfaces import ControlShadowEvent, ControlShadow
from tests.helpers.devices import DummyDeviceDrumPads, getEventForDrumPad


class Flag:
    """
    Helper class for checking if a property has changed
    """
    def __init__(self) -> None:
        self.is_set = False
        self.count = 0

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
    def callback(index: int, event: ControlShadowEvent, plug: UnsafeIndex):
        assert index == expected_index
        flag.set()
    return callback


def colorizeCallbackGenerator(
    index_matrix: list[list[int]],
    flag: Flag
):
    """
    Generates a callback in order to check that indexes were created correctly.

    The callback will check that the index matches, and then set the flag.

    ### Args:
    * `expected_index` (`int`): the index you're expecting
    """
    index_lookup = matrixToDict(index_matrix)

    def callback(index: int, event: ControlShadow, plug: UnsafeIndex):
        assert index_lookup[index] == event.coordinate
        flag.set()
        return Color.fromGrayscale(1)
    return callback


def annotateCallbackGenerator(
    index_matrix: list[list[int]],
    flag: Flag
):
    """
    Generates a callback in order to check that indexes were created correctly.

    The callback will check that the index matches, and then set the flag.

    ### Args:
    * `expected_index` (`int`): the index you're expecting
    """
    index_lookup = matrixToDict(index_matrix)

    def callback(index: int, event: ControlShadow, plug: UnsafeIndex):
        assert index_lookup[index] == event.coordinate
        flag.set()
        return "My annotation"
    return callback


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
    shadow.processEvent(
        device.matchEvent(getEventForDrumPad(0, 0, 0)),
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
    shadow.processEvent(
        device.matchEvent(getEventForDrumPad(0, 1, 0)),
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
    shadow.processEvent(
        device.matchEvent(getEventForDrumPad(1, 0, 0)),
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
    shadow.processEvent(
        device.matchEvent(getEventForDrumPad(1, 0, 0)),
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
    shadow.processEvent(
        device.matchEvent(getEventForDrumPad(0, 2, 0)),
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
    1  2  5  6
    3  4  7  8
    9  10 13 14
    11 12 15 16
    """
    device = DummyDeviceDrumPads(4, 4)
    flag = Flag()
    strategy = DrumPadStrategy(2, 2, True, triggerCallbackGenerator(5, flag))
    # Create the bindings
    shadow = DeviceShadow(device)
    strategy.apply(shadow)

    # Now process the event
    shadow.processEvent(
        device.matchEvent(getEventForDrumPad(0, 2, 0)),
        0,
    )
    # And check that the callback was reached
    assert flag.is_set


def test_limited_height_wraps_around():
    """
    When we create the bindings with constraints on the width and height, do
    the values wrap around correctly?

        1  2  5  6
        3  4  7  8
    --> 9  10 13 14
        11 12 15 16
    """
    device = DummyDeviceDrumPads(4, 4)
    flag = Flag()
    strategy = DrumPadStrategy(2, 2, True, triggerCallbackGenerator(9, flag))
    # Create the bindings
    shadow = DeviceShadow(device)
    strategy.apply(shadow)

    # Now process the event
    shadow.processEvent(
        device.matchEvent(getEventForDrumPad(2, 0, 0)),
        0,
    )
    # And check that the callback was reached
    assert flag.is_set


def test_colorize_annotate():
    """
    Are the drum pads colored correctly?

    We check that the colorize callback is called 16 times, and that all the
    indexes match up.
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

    # The flag should have been set twice for each drum pad
    assert flag.count == 32
