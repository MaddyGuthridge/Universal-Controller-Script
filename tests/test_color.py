"""
tests > test_color

Tests for color object
"""

from common.types import Color

from .helpers import floatApproxEq

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

def test_integer():
    c = Color.fromInteger(0xAABBCC)
    
    assert c.red == 0xAA
    assert c.green == 0xBB
    assert c.blue == 0xCC
    
    assert c.integer == 0xAABBCC

def test_assign_out_of_bounds():
    c = Color.fromInteger(0xFF)
    
    c.red = -12
    assert c.red == 0
    
    c.green = 270
    assert c.green == 255
    
    c.saturation = 1.2
    assert floatApproxEq(1.0, c.saturation)
    
    c.hue = 370.0
    assert floatApproxEq(10.0, c.hue)

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

def test_distance():
    c1 = Color.fromHsv(180, 1, 1)
    c2 = Color.fromHsv(160, 1, 1)
    c3 = Color.fromHsv(140, 1, 1)
    c4 = Color.fromHsv(180, 0.8, 1)
    c5 = Color.fromHsv(180, 0.6, 1)
    
    dist = Color.distance
    
    assert dist(c1, c2) < dist(c1, c3)
    assert dist(c1, c4) < dist(c1, c5)

def test_closest():
    c = Color.fromInteger(0xFF0000)
    
    options = [
        Color.fromHsv(0, 1, 0.9),
        Color.fromHsv(10, 1, 1),
        Color.fromHsv(11, 1, 0.8),
        Color.fromHsv(355, 1, 0.9),
        Color.fromHsv(355, 0.99, 1),
        Color.fromHsv(354, 1, 1)
    ]
    
    assert c.closest(options) == options[-2]
