"""
devices > novation > launchkey > mk2 > colors

Colour definitions for the Novation Launchkey Mk2
"""

from common.types.color import Color


COLORS = {
    #                 0xRRGGBB
    Color.fromInteger(0x000000):   0, # Off
    Color.fromInteger(0xFFFFFF): 127, # White
    Color.fromInteger(0x94323E):  15, # Red
    Color.fromInteger(0x45A147):  60, # Green
    Color.fromInteger(0xBF8F40):  91, # Orange
    Color.fromInteger(0x77A145):  53, # Lime
    Color.fromInteger(0xD1D176):  39, # Light yellow
    Color.fromInteger(0xCFAB6F):  23, # Light orange
}
