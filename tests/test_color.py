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
    assert c.green == 127
    assert c.blue == 127

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
    
    c.hue = 1.2
    assert floatApproxEq(0.2, c.hue)
