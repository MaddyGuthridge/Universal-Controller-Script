"""
common > util > color

Contains definition for color type.
"""
from __future__ import annotations

from math import floor

def hsvToRgb(h: float, s: float, v: float) -> tuple[int, int, int]:
    """
    Convert HSV to RGB color spaces

    ### Args:
    * `h` (`float`): Hue (degrees: 0-360)
    * `s` (`float`): Saturation (0-1.0)
    * `v` (`float`): Value (0-1.0)

    ### Returns:
    * `tuple[int, int, int]`: Red, Green, Blue (all 0-255)
    
    ### Credits
    * Adapted from [Wikipedia](https://en.wikipedia.org/wiki/HSL_and_HSV)
    """
    # First, we find chroma:
    c = v * s
    
    # Find a point on the bottom three faces of the RGB cube with the same hue
    # and chroma as our color
    h_ = h / 60
    # intermediate value x for  second largest component of the color
    x = c * (1 - abs(h_ % 2 - 1))
    
    if h_ < 1:
        r, g, b = c, x, 0
    elif h_ < 2:
        r, g, b = x, c, 0
    elif h_ < 3:
        r, g, b = 0, c, x
    elif h_ < 4:
        r, g, b = 0, x, c
    elif h_ < 5:
        r, g, b = x, 0, c
    else: #h_ < 6
        r, g, b = c, 0, x
    
    # Finally, get a median value to add to each component
    m = v - c
    r, g, b = r+m, g+m, b+m
    
    # And return them in a reasonable format
    # 0-255
    return int(r*255), int(g*255), int(b*255)

def rgbToHsv(r: int, g: int, b: int) -> tuple[float, float, float]:
    """
    Convert RGB to HSV color spaces

    ### Args:
    * `r` (`int`): red (0-255)
    * `g` (`int`): green (0-255)
    * `b` (`int`): blue (0-255)

    ### Returns:
    * `tuple[float, float, float]`:
        * Hue: degrees (0-360)
        * Saturation: 0-1.0
        * Value: 0-1.0
    
    ### Credits
    * Adapted from [Wikipedia](https://en.wikipedia.org/wiki/HSL_and_HSV)
    """
    # Put RGB values into 0-1.0 range
    r_, g_, b_ = r/255, g/255, b/255
    
    x_max = max(r_, g_, b_)
    x_min = min(r_, g_, b_)
    
    # Find chroma
    c = x_max - x_min
    
    # Value is x_max
    v = x_max
    
    # Lightness (middle value) for HSL
    # l = (x_max + x_min) / 2
    
    # Calculate hue
    if c == 0:
        h = 0
    elif v == r_:
        h = ((g_ - b_) / c)
    elif v == g_:
        h = (2 + (b_ - r_)/c)
    else: #  v == b
        h = (4 + (r_ - g_)/c)
    h *= 60
    
    # Calculate saturation
    s = c/v if v != 0 else 0
    
    return h, s, v

class Color:
    """
    Color class

    Defines an RGB color, as well as useful functions for converting between
    various color types.
    
    NOTE: colors are stored as separate red, green and blue components
    internally. Calculations for HSV representations are made when required
    """
    
    def __init__(self) -> None:
        """
        Create a blank color object.

        WARNING: This should only be called internally. Use any of the following
        instead:
        * `Color.fromInt()`
        * `Color.fromRgb()`
        * `Color.fromHsv()`
        """
        self.__red = 0
        self.__green = 0
        self.__blue = 0
    
    def __repr__(self) -> str:
        return f"Color({self.__red}, {self.__green}, {self.__blue})"
        
    def copy(self) -> Color:
        """
        Create an identical copy of this color object

        ### Returns:
        * `Color`: colour object copy
        """
        c = Color()
        c.integer = self.integer
        return c
        
    @staticmethod
    def fromInteger(rgb: int) -> Color:
        """
        Create a color object from an FL Studio color int

        ### Args:
        * `rgb` (`int`): rgb color (0xRRGGBB)

        ### Returns:
        * `Color`: new color object
        """
        c = Color()
        
        c.integer = rgb
        
        return c
    
    @staticmethod
    def fromRgb(r: int, g: int, b: int) -> Color:
        """
        Create a color object from RGB values

        ### Args:
        * `r` (`int`): red
        * `g` (`int`): green
        * `b` (`int`): blue

        ### Returns:
        * `Color`: colour
        """
        c = Color()
        
        c.red = r
        c.green = g
        c.blue = b
        
        return c
    
    @staticmethod
    def fromHsv(hue: float, saturation: float, value: float) -> Color:
        """
        Crewate a color object from hue, saturation and value values

        Each value should be a float between 0.0-1.0

        ### Args:
        * `hue` (`float`): hue
        * `saturation` (`float`): saturation
        * `value` (`float`): value (luminosity)

        ### Returns:
        * `Color`: colour
        """
        c = Color()
        
        c.hsv = hue, saturation, value
        
        return c
    
    @staticmethod
    def __valCheckRgb(val: int) -> int:
        """
        Ensure values used in setters are valid.
        For values outside the range 0-255, adjust them as required

        ### Args:
        * `val` (`int`): value to check

        ### Raises:
        * `TypeError`: bad value type
        
        ### Returns
        * `int`: adjusted and checked value
        """
        if not isinstance(val, int):
            raise TypeError("RGB values must be integers between 0 and 255")
        if val < 0: return 0
        if val > 255: return 255
        else: return val
    
    @property
    def integer(self) -> int:
        """
        Represents the colour as a 3-byte integer comprised of red green and
        blue values.

        The value takes the form 0xRRGGBB. This is useful for interacting with
        FL Studio's APIs

        ### Returns:
        * `int`: color rgb
        """
        return (
            (self.red << 16)
          + (self.green << 8)
          + self.blue
        )
    @integer.setter
    def integer(self, i: int) -> None:
        """
        Set the colour using a 3-byte integer comprised of red, green and blue
        values.

        The value takes the form 0xRRGGBB. This is useful for interacting with
        FL Studio's APIs

        ### Args:
        * `i` (`int`): color integer
        """
        self.red = (i & 0xFF0000) >> 16
        self.green = (i & 0x00FF00) >> 8
        self.blue = (i & 0x0000FF)
    
    @property
    def hsv(self) -> tuple[float, float, float]:
        """
        Represents the colour as a tuple of floats representing hue, saturation,
        and value

        NOTE: Under the hood, values are still stored as RGB - conversions are
        made as required.

        ### Returns:
        * `tuple[float, float, float]`:
            * hue (degrees: 0-360)
            * saturation (0-1.0)
            * value (0-1.0)
        """
        return rgbToHsv(self.red, self.green, self.blue)
    @hsv.setter
    def hsv(self, hsv: tuple[float, float, float]) -> None:
        """
        Set the color using an HSV value

        NOTE: Under the hood, values are still stored as RGB - conversions are
        made as required.

        ### Args:
        * `hsv` (`tuple[float, float, float]`):
            * hue (degrees: 0-360)
            * saturation (0-1.0)
            * value (0-1.0)
        """
        h, s, v = hsv
        
        # Get within range
        # h
        if h < 0:
            h += floor(h // 360) * 360
        if h >= 360.0:
            h -= floor(h // 360) * 360
        # s
        if s < 0:
            s = 0.0
        if s > 1.0:
            s = 1.0
        # v
        if v < 0:
            v = 0.0
        if v > 1.0:
            v = 1.0
        
        r, g, b = hsvToRgb(h, s, v)
        self.red = r
        self.green = g
        self.blue = b
    
    @property
    def red(self) -> int:
        """
        Represents the red component of the color

        ### Returns:
        * `int`: red
        """
        return self.__red
    @red.setter
    def red(self, r: int) -> None:
        """
        Set the red component of the color

        ### Args:
        * `r` (`int`): red
        """
        self.__red = Color.__valCheckRgb(r)
    
    @property
    def green(self) -> int:
        """
        Represents the green component of the color

        ### Returns:
        * `int`: green
        """
        return self.__green
    @green.setter
    def green(self, g) -> None:
        """
        Set the green component of the color

        ### Args:
        * `g` (`int`): green
        """
        self.__green = Color.__valCheckRgb(g)
    
    @property
    def blue(self) -> int:
        """
        Represents the blue component of the color

        ### Returns:
        * `int`: blue
        """
        return self.__blue
    @blue.setter
    def blue(self, b) -> None:
        """
        Set the blue component of the color

        ### Args:
        * `b` (`int`): blue
        """
        self.__blue = Color.__valCheckRgb(b)

    @property
    def hue(self) -> float:
        """
        Represents the hue of the color
        
        NOTE: Under the hood, values are still stored as RGB - conversions are
        made as required.

        ### Returns:
        * `float`: hue (degrees: 0-360)
        """
        return self.hsv[0]
    @hue.setter
    def hue(self, h: float):
        """
        Set the hue of the color
        
        NOTE: Under the hood, values are still stored as RGB - conversions are
        made as required.

        ### Args:
        * `h` (`float`): hue (degrees: 0-360)
        """
        _, s, v = self.hsv
        self.hsv = h, s, v
    
    @property
    def saturation(self) -> float:
        """
        Represents the saturation of the color
        
        NOTE: Under the hood, values are still stored as RGB - conversions are
        made as required.

        ### Returns:
        * `float`: saturation
        """
        return self.hsv[1]
    @saturation.setter
    def saturation(self, s: float):
        """
        Set the saturation of the color
        
        NOTE: Under the hood, values are still stored as RGB - conversions are
        made as required.

        ### Args:
        * `s` (`float`): saturation
        """
        h, _, v = self.hsv
        self.hsv = h, s, v

    @property
    def value(self) -> float:
        """
        Represents the value of the color
        
        NOTE: Under the hood, values are still stored as RGB - conversions are
        made as required.

        ### Returns:
        * `float`: value
        """
        return self.hsv[2]
    @value.setter
    def value(self, v: float):
        """
        Set the value of the color
        
        NOTE: Under the hood, values are still stored as RGB - conversions are
        made as required.

        ### Args:
        * `v` (`float`): value (luminosity)
        """
        h, s, _ = self.hsv
        self.hsv = h, s, v
