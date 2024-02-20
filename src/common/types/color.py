"""
common > types > color

Contains definition for color type, which is used to represent colors within
the script.

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""
# from __future__ import annotations

from math import floor
from typing import Optional

__all__ = [
    'Color'
]

# Constants for scaling color components when getting distances
# Higher values contribute more to closeness
HUE_SCALE = 10.0
SAT_SCALE = 0.9
VAL_SCALE = 2.0


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
    c = int(v * s * 255)

    # Find a point on the bottom three faces of the RGB cube with the same hue
    # and chroma as our color
    h_ = h / 60
    # intermediate value x for  second largest component of the color
    x = int(c * (1 - abs(h_ % 2 - 1)))

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
    else:  # h_ < 6
        r, g, b = c, 0, x

    # Finally, get a median value to add to each component
    m = int(v*255) - c
    r, g, b = r+m, g+m, b+m

    # And return them in a reasonable format
    # 0-255
    return r, g, b


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
        h = 0.0
    elif v == r_:
        h = ((g_ - b_) / c)
    elif v == g_:
        h = (2 + (b_ - r_)/c)
    else:  # v == b
        h = (4 + (r_ - g_)/c)
    h *= 60

    # Calculate saturation
    s = c/v if v != 0 else 0

    # Adjust hue to 0 - 360
    if h < 0:
        h += 360

    return h, s, v


class Color:
    """
    Color class

    Defines an RGB color, as well as useful functions for converting between
    various color types.

    NOTE: colors are stored as separate red, green and blue components
    internally. Calculations for HSV representations are made when required
    """
    __slots__ = ['__red', '__green', '__blue', '__grayscale', '__enabled']

    def __init__(self) -> None:
        """
        Create an empty color object: Color(0, 0, 0)

        To start from another value, use one of the creation functions:
        * `Color.fromInt()`
        * `Color.fromRgb()`
        * `Color.fromHsv()`
        """
        self.__red = 0
        self.__green = 0
        self.__blue = 0
        self.__grayscale = 0.0
        self.__enabled = False

    def __repr__(self) -> str:
        return f"Color(0x{self.integer:06X} | "\
            + f"r={self.red}, g={self.green}, b={self.blue})"

    def __hash__(self) -> int:
        return self.integer

#     def copy(self) -> 'Color':
#         """
#         Create an identical copy of this color object
#
#         ### Returns:
#         * `Color`: color object copy
#         """
#         c = Color()
#         c.integer = self.integer
#         return c

    ###########################################################################
    # Creation functions

    def __setGrayscaleEnabled(
        self,
        grayscale: Optional[float],
        enabled: Optional[bool],
    ):
        """Update the grayscale and enabled values of this color object"""
        if grayscale is None:
            self.__grayscale = self.value
        else:
            self.__grayscale = grayscale

        if enabled is None:
            self.__enabled = self != Color()
        else:
            self.__enabled = enabled

    @staticmethod
    def fromInteger(
        rgb: int,
        grayscale: Optional[float] = None,
        enabled: Optional[bool] = None,
    ) -> 'Color':
        """
        Create a color object from an FL Studio color int

        ### Args:
        * `rgb` (`int`): rgb color (0xRRGGBB)
        * `grayscale` (`float`, optional): brightness for grayscale LEDs.
          Defaults to value of color.
        * `enabled` (`bool`, optional): whether the LED should be on for on/off
          LEDs. Defaults to True for non-black colors.

        ### Returns:
        * `Color`: new color object
        """
        c = Color()

        r = (rgb & 0xFF0000) >> 16
        g = (rgb & 0x00FF00) >> 8
        b = (rgb & 0x0000FF)

        c.__red = r
        c.__green = g
        c.__blue = b

        c.__setGrayscaleEnabled(grayscale, enabled)

        return c

    @staticmethod
    def fromRgb(
        r: int,
        g: int,
        b: int,
        grayscale: Optional[float] = None,
        enabled: Optional[bool] = None,
    ) -> 'Color':
        """
        Create a color object from RGB values

        ### Args:
        * `r` (`int`): red (0-255)
        * `g` (`int`): green (0-255)
        * `b` (`int`): blue (0-255)
        * `grayscale` (`float`, optional): brightness for grayscale LEDs.
          Defaults to value of color.
        * `enabled` (`bool`, optional): whether the LED should be on for on/off
          LEDs. Defaults to True for non-black colors.

        ### Returns:
        * `Color`: color
        """
        c = Color()

        r = c.__valCheckRgb(r)
        g = c.__valCheckRgb(g)
        b = c.__valCheckRgb(b)

        c.__red = r
        c.__green = g
        c.__blue = b

        c.__setGrayscaleEnabled(grayscale, enabled)

        return c

    @staticmethod
    def fromHsv(
        hue: float,
        saturation: float,
        value: float,
        grayscale: Optional[float] = None,
        enabled: Optional[bool] = None,
    ) -> 'Color':
        """
        Create a color object from hue, saturation and value values

        ### Args:
        * `hue` (`float`): hue (degrees, 0-360)
        * `saturation` (`float`): saturation (0-1)
        * `value` (`float`): value (0-1)
        * `grayscale` (`float`, optional): brightness for grayscale LEDs.
          Defaults to value of color.
        * `enabled` (`bool`, optional): whether the LED should be on for on/off
          LEDs. Defaults to True for non-black colors.

        ### Returns:
        * `Color`: color
        """
        c = Color()

        hue = c.__valCheckHue(hue)
        saturation = c.__valCheckSatVal(saturation)
        value = c.__valCheckSatVal(value)

        r, g, b = hsvToRgb(hue, saturation, value)

        c.__red = r
        c.__green = g
        c.__blue = b

        c.__setGrayscaleEnabled(grayscale, enabled)

        return c

    @staticmethod
    def fromGrayscale(
        grayscale: float,
        enabled: Optional[bool] = None,
    ) -> 'Color':
        """
        Create a color object from a grayscale value

        ### Args:
        * `grayscale` (`float`): brightness for grayscale LEDs.
        * `enabled` (`bool`, optional): whether the LED should be on for on/off
          LEDs. Defaults to True for non-black colors.

        ### Returns:
        * `Color`: new color object
        """
        c = Color()

        value = int(grayscale*255)

        c.__red = value
        c.__green = value
        c.__blue = value
        c.__grayscale = grayscale
        if enabled is None:
            c.__enabled = grayscale != 0
        else:
            c.__enabled = enabled

        return c

    ###########################################################################
    # Helper functions

    @staticmethod
    def __valCheckRgb(val: int) -> int:
        """
        Ensure values used in RGB setters are valid.
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
        if val < 0:
            return 0
        if val > 255:
            return 255
        else:
            return val

    @staticmethod
    def __valCheckSatVal(val: float) -> float:
        """
        Ensure values used in saturation and value setters are valid.
        For values outside the range 0-1, adjust them as required

        ### Args:
        * `val` (`float`): value to check

        ### Returns
        * `float`: adjusted and checked value
        """
        if val < 0:
            return 0.0
        if val > 1.0:
            return 1.0
        else:
            return val

    @staticmethod
    def __valCheckHue(h: float) -> float:
        """
        Ensure values used in saturation and value setters are valid.
        For values outside the range 0-360, adjust them as required

        ### Args:
        * `h` (`float`): value to check

        ### Raises:
        * `TypeError`: bad value type

        ### Returns
        * `int`: adjusted and checked value
        """
        if h < 0:
            # Note that when h < 0, h // 360 < 0, hence subtraction
            h -= floor(h // 360) * 360
        if h >= 360.0:
            h -= floor(h // 360) * 360
        return h

    ###########################################################################
    # Properties

    @property
    def integer(self) -> int:
        """
        Represents the color as a 3-byte integer comprised of red green and
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

    @property
    def hsv(self) -> tuple[float, float, float]:
        """
        Represents the color as a tuple of floats representing hue,
        saturation, and value

        NOTE: Under the hood, values are still stored as RGB - conversions are
        made as required.

        ### Returns:
        * `tuple[float, float, float]`:
            * hue (degrees: 0-360)
            * saturation (0-1.0)
            * value (0-1.0)
        """
        return rgbToHsv(self.red, self.green, self.blue)

    @property
    def red(self) -> int:
        """
        Represents the red component of the color

        ### Returns:
        * `int`: red
        """
        return self.__red

    @property
    def green(self) -> int:
        """
        Represents the green component of the color

        ### Returns:
        * `int`: green
        """
        return self.__green

    @property
    def blue(self) -> int:
        """
        Represents the blue component of the color

        ### Returns:
        * `int`: blue
        """
        return self.__blue

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

    @property
    def grayscale(self) -> float:
        """
        Represents the color as a shade of grey (between 0.0 and 1.0).

        This value should be used by controllers whose LEDs don't support RGB
        colors.

        ### Returns:
        * `float`: grayscale value
        """
        return self.__grayscale

    @property
    def enabled(self) -> bool:
        """
        Represents the color as a either on or off.

        This value should be used by controllers whose LEDs don't support
        shading.

        ### Returns:
        * `bool`: grayscale value
        """
        return self.__enabled

    ###########################################################################
    # Operators

    @staticmethod
    def fade(
        start: 'Color',
        end: 'Color',
        position: float = 0.5,
        enabled: Optional[bool] = None,
    ) -> 'Color':
        """
        Fade between two colors, using the HSV color space to ensure that
        intermediate colors remain vibrant.

        Grayscale values are averaged, and enabled values are set to the
        default for the result.

        ### Args:
        * `start` (`Color`): color to fade from
        * `end` (`Color`): color to fade to
        * `position` (`float`, optional): position of the fade to use (0-1.0).
          Defaults to `0.5`.
        * `enabled` (`bool`, optional): whether the color should be considered
          enabled. Defaults to `None` to determine based on the result.

        ### Returns:
        * `Color`: faded color
        """
        hue_start = start.hue
        hue_end = end.hue
        # Ensure hues are within 180 deg
        if hue_start - hue_end > 180:
            hue_start -= 360
        elif hue_end - hue_start > 180:
            hue_end -= 360

        # Reverse Position
        rev_pos = 1 - position

        return Color.fromHsv(
            hue_end * position + hue_start * rev_pos,
            end.saturation * position + start.saturation * rev_pos,
            end.value * position + start.value * rev_pos,
            start.grayscale * position + end.grayscale * rev_pos,
            enabled,
        )

    def fadeBlack(
        self: 'Color',
        position: float = 0.5,
        enabled: Optional[bool] = None,
    ) -> 'Color':
        """
        Fade between this color and black

        Grayscale values are averaged, and enabled values are set to the
        default for the result.

        ### Args:
        * `position` (`float`, optional): position of the fade to use (0-1.0).
          Defaults to `0.5`.
        * `enabled` (`bool`, optional): whether the color should be considered
          enabled. Defaults to `None` to determine based on the result.

        ### Returns:
        * `Color`: Faded color
        """
        black = Color()
        return Color.fade(self, black, position, enabled)

    def fadeGray(
        self: 'Color',
        position: float = 0.5,
        enabled: Optional[bool] = None,
    ) -> 'Color':
        """
        Fade between this color and gray

        Grayscale values are averaged, and enabled values are set to the
        default for the result.

        ### Args:
        * `position` (`float`, optional): position of the fade to use (0-1.0).
          Defaults to `0.5`.
        * `enabled` (`bool`, optional): whether the color should be considered
          enabled. Defaults to `None` to determine based on the result.

        ### Returns:
        * `Color`: Faded color
        """
        gray = Color.fromHsv(
            self.hue,
            0.0,
            self.value
        )
        return Color.fade(self, gray, position, enabled)

    @staticmethod
    def distance(start: 'Color', end: 'Color') -> float:
        """
        Calculate the 'distance' between two colors, using the HSV color space
        to ensure that the closest visibly similar color is chosen.

        ### Args:
        * `start` (`Color`): starting color
        * `end` (`Color`): finishing color

        ### Returns:
        * `float`: distance
        """
        h1, s1, v1 = start.hsv
        h2, s2, v2 = end.hsv

        # Ensure hues are within 180 deg
        if h1 - h2 > 180:
            h1 -= 360
        elif h2 - h1 > 180:
            h2 -= 360

        # Get scaled deltas
        delta_h = abs(h2 - h1) / 360 * HUE_SCALE
        delta_s = abs(s2 - s1) * SAT_SCALE
        delta_v = abs(v2 - v1) * VAL_SCALE

        # Don't bother doing square root since it's arbitrary anyway
        return delta_h**2 + delta_s**2 + delta_v**2

    def closest(self, others: list['Color']) -> 'Color':
        """
        Given a set of colors, find the closest one and return it

        ### Args:
        * `others` (`list[Color]`): List of colors to pick from

        ### Returns:
        * `Color`: closest match
        """
        if len(others) == 0:
            raise ValueError("Set cannot be empty")

        closest = others[0]
        closest_dist = Color.distance(self, closest)

        for c in others[1:]:
            dist = Color.distance(self, c)
            if dist < closest_dist:
                closest = c
                closest_dist = dist

        return closest

    def closestGrayscale(self, others: list[float]) -> float:
        """
        Given a set of grayscale values, find the closest one and return it

        ### Args:
        * `others` (`list[float]`): List of values to pick from

        ### Returns:
        * `float`: closest match
        """
        if len(others) == 0:
            raise ValueError("Set cannot be empty")

        closest = others[0]
        closest_dist = 1.0

        for val in others[1:]:
            dist = abs(self.grayscale - val)
            if dist < closest_dist:
                closest = val
                closest_dist = dist

        return closest

    def __add__(self, other) -> 'Color':
        if isinstance(other, Color):
            return Color.fromRgb(
                self.red + other.red,
                self.green + other.green,
                self.blue + other.blue,
                self.grayscale + other.grayscale,
                self.enabled or other.enabled,
            )
        elif isinstance(other, int):
            return Color.fromRgb(
                self.red + other,
                self.green + other,
                self.blue + other
            )
        else:
            return NotImplemented

    def __radd__(self, other) -> 'Color':
        # Addition is commutative
        if isinstance(other, (int, Color)):
            return self + other
        return NotImplemented

    def __sub__(self, other) -> 'Color':
        if isinstance(other, Color):
            return Color.fromRgb(
                self.red - other.red,
                self.green - other.green,
                self.blue - other.blue,
                self.grayscale - other.grayscale,
            )
        elif isinstance(other, int):
            return Color.fromRgb(
                self.red - other,
                self.green - other,
                self.blue - other
            )
        else:
            return NotImplemented

    def __rsub__(self, other) -> 'Color':
        if isinstance(other, int):
            return Color.fromRgb(
                other - self.red,
                other - self.green,
                other - self.blue
            )
        else:
            return NotImplemented

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Color):
            return all([
                self.red == other.red,
                self.green == other.green,
                self.blue == other.blue,
                # self.grayscale == other.grayscale,
                # self.enabled == other.enabled,
            ])
        elif isinstance(other, int):
            return self == Color.fromInteger(other)
        else:
            return NotImplemented

    # Hopefully this duplicate code can be fixed if I get a better answer to
    # https://stackoverflow.com/q/75000973/6335363
    WHITE: 'Color'
    GRAY: 'Color'
    BLACK: 'Color'

    RED: 'Color'
    GREEN: 'Color'
    BLUE: 'Color'

    ENABLED: 'Color'
    DISABLED: 'Color'

    FL_SONG: 'Color'
    FL_SONG_ALT: 'Color'
    FL_PATTERN: 'Color'
    FL_PATTERN_ALT: 'Color'
    FL_RECORD: 'Color'
    FL_STOP: 'Color'


Color.RED = Color.fromRgb(255, 0, 0)
Color.GREEN = Color.fromRgb(0, 255, 0)
Color.BLUE = Color.fromRgb(0, 0, 255)
Color.WHITE = Color.fromGrayscale(1)
Color.GRAY = Color.fromGrayscale(0.5, enabled=False)
Color.BLACK = Color()

Color.ENABLED = Color.fromGrayscale(0.7)
Color.DISABLED = Color.fromGrayscale(0.3, enabled=False)

Color.FL_SONG = Color.fromInteger(0x45F147, 0.6, True)
Color.FL_SONG_ALT = Color.fromInteger(0x00A0F0, 1.0, True)
Color.FL_PATTERN = Color.fromInteger(0xF78F41, 0.6, True)
Color.FL_PATTERN_ALT = Color.fromInteger(0xA43A37, 1.0, True)
Color.FL_RECORD = Color.fromInteger(0xAF0000, 1.0, True)
Color.FL_STOP = Color.fromInteger(0xB9413E, 1.0, True)
