"""
common > util > color

Contains definition for color type.
"""

import utils

from __future__ import annotations

class Color:
    """
    Color class

    Defines an RGB color, as well as useful functions for converting between
    various color types.
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
        
        c.red = (rgb & 0xFF0000) >> 4
        c.green = (rgb & 0x00FF00) >> 2
        c.blue = (rgb & 0x0000FF)
        
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
            self.red << 4
          + self.green << 2
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
        self.red = (i & 0xFF0000) >> 4
        self.green = (i & 0x00FF00) >> 2
        self.blue = (i & 0x0000FF)
    
    @property
    def hsv(self) -> tuple[float, float, float]:
        """
        Represents the colour as a tuple of floats representing hue, saturation,
        and value (luminosity)

        NOTE: Under the hood, values are still stored as RGB - conversions are
        made as required.

        ### Returns:
        * `tuple[float, float, float]`: color data, all between 0.0-1.0
        """
        return utils.RGBToHSVColor(self.integer)
    @hsv.setter
    def hsv(self, hsv: tuple[float, float, float]) -> None:
        """
        Set the color using an HSV value

        NOTE: Under the hood, values are still stored as RGB - conversions are
        made as required.

        ### Args:
        * `hsv` (`tuple[float, float, float]`): hue, saturation and value 
          (luminosity). Each between 0.0-1.0
        """
        r, g, b = utils.HSVtoRGB(*hsv)
        self.red = int(r * 255)
        self.green = int(g * 255)
        self.blue = int(b * 255)
    
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
        self.__valCheckRgb(g)
        self.__green = g
    
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
        self.__valCheckRgb(b)
        self.__blue = b

    @property
    def hue(self) -> float:
        """
        Represents the hue of the color
        
        NOTE: Under the hood, values are still stored as RGB - conversions are
        made as required.

        ### Returns:
        * `int`: hue
        """
        return self.hsv[0]
    @hue.setter
    def hue(self, h: float):
        """
        Set the hue of the color
        
        NOTE: Under the hood, values are still stored as RGB - conversions are
        made as required.

        ### Args:
        * `h` (`int`): hue
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
        * `int`: saturation
        """
        return self.hsv[1]
    @saturation.setter
    def saturation(self, s: float):
        """
        Set the saturation of the color
        
        NOTE: Under the hood, values are still stored as RGB - conversions are
        made as required.

        ### Args:
        * `s` (`int`): saturation
        """
        h, _, v = self.hsv
        self.hsv = h, s, v

    @property
    def value(self) -> float:
        """
        Represents the value (luminosity) of the color
        
        NOTE: Under the hood, values are still stored as RGB - conversions are
        made as required.

        ### Returns:
        * `int`: value (luminosity)
        """
        return self.hsv[2]
    @value.setter
    def value(self, v: float):
        """
        Set the value (luminosity) of the color
        
        NOTE: Under the hood, values are still stored as RGB - conversions are
        made as required.

        ### Args:
        * `v` (`int`): value (luminosity)
        """
        h, s, _ = self.hsv
        self.hsv = h, s, v
