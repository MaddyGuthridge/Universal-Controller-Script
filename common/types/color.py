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
        
    @staticmethod
    def fromInt(rgb: int) -> Color:
        """
        Create a color object from an FL Studio color int

        ### Args:
        * `rgb` (`int`): rgb color

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
    def fromHsv(hue: float, saturation: float, value: float):
        c = Color()
        
        # c.red = r
        # c.green = g
        # c.blue = b
        
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
    def rgb(self) -> int:
        return (
            self.red << 4
          + self.green << 2
          + self.blue
        )
    @rgb.setter
    def rgb(self, i: int) -> None:
        self.red = (i & 0xFF0000) >> 4
        self.green = (i & 0x00FF00) >> 2
        self.blue = (i & 0x0000FF)
    
    @property
    def hsv(self) -> tuple[float, float, float]:
        return utils.RGBToHSVColor(self.rgb)
    @hsv.setter
    def hsv(self, hsv: tuple[float, float, float]) -> None:
        r, g, b = utils.HSVtoRGB(*hsv)
        self.red = int(r * 255)
        self.green = int(g * 255)
        self.blue = int(b * 255)
    
    @property
    def red(self) -> int:
        return self.__red
    @red.setter
    def red(self, r: int) -> None:
        self.__red = Color.__valCheckRgb(r)
    
    @property
    def green(self) -> int:
        return self.__green
    @green.setter
    def green(self, g) -> None:
        self.__valCheckRgb(g)
        self.__green = g
    
    @property
    def blue(self) -> int:
        return self.__blue
    @blue.setter
    def blue(self, b) -> None:
        self.__valCheckRgb(b)
        self.__blue = b

    @property
    def hue(self) -> float:
        return self.hsv[0]
    @hue.setter
    def hue(self, h: float):
        _, s, v = self.hsv
        self.hsv = h, s, v
    
    @property
    def saturation(self) -> float:
        return self.hsv[1]
    @saturation.setter
    def saturation(self, s: float):
        h, _, v = self.hsv
        self.hsv = h, s, v

    @property
    def value(self) -> float:
        return self.hsv[2]
    @value.setter
    def value(self, v: float):
        h, s, _ = self.hsv
        self.hsv = h, s, v
