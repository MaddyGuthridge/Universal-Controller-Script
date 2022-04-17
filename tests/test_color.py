"""
tests > test_color

Tests for color object
"""

import pytest
from common.types import Color

from .helpers import floatApproxEq, combinations


def test_basic():
    c = Color()

    assert c.red == 0
    assert c.blue == 0
    assert c.green == 0


def test_rgb():
    c = Color.fromRgb(10, 15, 20)

    assert c.red == 10
    assert c.green == 15
    assert c.blue == 20


def test_hsv():
    c = Color.fromHsv(0.0, 0.5, 1.0)

    assert floatApproxEq(0.0, c.hue)
    assert floatApproxEq(0.5, c.saturation)
    assert floatApproxEq(1.0, c.value)

    assert c.red == 255
    assert c.green == 128
    assert c.blue == 128

# Need high saturation values, as low saturation leads to data loss and
# inaccuracy


@pytest.mark.parametrize('hsv', [
    (10.0, 0.7, 0.65),
    (180.0, 0.8, 1.0),
    (350.0, 0.9, 0.5),
    (210.0, 1.0, 1.0)
])
def test_hsv_get_set(hsv):
    c = Color.fromHsv(*hsv)
    h, s, v = hsv
    assert floatApproxEq(c.hue, h)
    assert floatApproxEq(c.saturation, s)
    assert floatApproxEq(c.value, v)


def test_integer():
    c = Color.fromInteger(0xAABBCC)

    assert c.red == 0xAA
    assert c.green == 0xBB
    assert c.blue == 0xCC

    assert c.integer == 0xAABBCC


def test_copy():
    c = Color.fromRgb(10, 15, 20)
    c2 = c.copy()
    c.blue = 10
    c.red = 50
    assert c2.red == 10
    assert c2.green == 15
    assert c2.blue == 20


def test_assign_out_of_bounds_rgb():
    c = Color.fromInteger(0xFF)

    c.red = -12
    assert c.red == 0

    c.green = 270
    assert c.green == 255

    with pytest.raises(TypeError):
        c.red = 0.75


def test_assign_out_of_bounds():
    c = Color.fromInteger(0xFF)

    c.saturation = 1.2
    assert floatApproxEq(1.0, c.saturation)

    c.value = 1.2
    assert floatApproxEq(1.0, c.value)

    c.hue = 370.0
    assert floatApproxEq(10.0, c.hue)
    c.hue = -10.0
    assert floatApproxEq(350.0, c.hue)


def test_add():
    c1 = Color.fromRgb(255, 0, 0)
    c2 = Color.fromRgb(0, 255, 0)

    assert c1 + c2 == 0xFFFF00

    assert c1 + 0xFF == 0xFFFFFF


def test_sub():
    c1 = Color.fromRgb(255, 0, 0)
    c2 = Color.fromRgb(10, 15, 0)

    assert c1 - c2 == Color.fromRgb(245, 0, 0)

    assert c1 - 0xFF == 0


def test_fade():
    c1 = Color.fromRgb(255, 0, 0)
    c2 = Color.fromRgb(0, 255, 0)
    c3 = Color.fromRgb(255, 255, 0)

    assert Color.fade(c1, c2) == 0xFFFF00
    assert Color.fade(c1, c3) == 0xFF7F00


@pytest.mark.parametrize(
    ["c1", "c2"],
    combinations([
        Color.fromHsv(10, 1, 1),
        Color.fromHsv(230, 0.5, 0.6),
        Color.fromHsv(345, 0.7, 0.8),
    ], 2)
)
def test_fade_distance(c1, c2):
    fade = Color.fade(c1, c2)
    assert floatApproxEq(Color.distance(c1, fade), Color.distance(c2, fade))


def test_fade_black():
    """Fading to black should halve the value"""
    c = Color.fromHsv(250, 1.0, 0.6)
    assert floatApproxEq(c.value / 2, Color.fadeBlack(c).value)


def test_fade_gray():
    """Fading to black should halve the saturation"""
    c = Color.fromHsv(250, 1.0, 0.6)
    assert floatApproxEq(c.saturation / 2, Color.fadeGray(c).saturation)


def test_distance():
    c1 = Color.fromHsv(180, 1, 1)
    c2 = Color.fromHsv(160, 1, 1)
    c3 = Color.fromHsv(140, 1, 1)
    c4 = Color.fromHsv(180, 0.8, 1)
    c5 = Color.fromHsv(180, 0.6, 1)

    dist = Color.distance

    assert dist(c1, c2) < dist(c1, c3)
    assert dist(c1, c4) < dist(c1, c5)


def test_distance_wrap():
    """Test that colour distances allow the wrapping of hue values,
    such that h=10deg is closer to 350deg than 180deg
    """
    c1 = Color.fromHsv(10, 1, 1)
    c2 = Color.fromHsv(350, 1, 1)
    c3 = Color.fromHsv(180, 1, 1)

    dist = Color.distance

    assert dist(c1, c2) == dist(c2, c1)
    assert dist(c1, c2) < dist(c1, c3)
    assert dist(c1, c2) < dist(c3, c2)


def test_closest():
    c = Color.fromInteger(0xFF0000)

    options = [
        Color.fromHsv(0, 1, 0.9),
        Color.fromHsv(10, 1, 1),
        Color.fromHsv(11, 1, 0.8),
        Color.fromHsv(355, 1, 0.9),
        Color.fromHsv(354, 1, 1),
        Color.fromHsv(355, 0.99, 1),
    ]

    assert c.closest(options) == options[-1]
