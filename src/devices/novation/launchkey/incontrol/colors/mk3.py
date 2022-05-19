"""
devices > novation > launchkey > mk2 > colors

Colour definitions for the Novation Launchkey Mk2

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]
"""

import math
from common.types.color import Color


COLORS = {
    #                 0xRRGGBB
    Color.fromInteger(0x0): 0,
    Color.fromInteger(0x505050): 2,
    Color.fromInteger(0xFFFFFF): 3,
    Color.fromInteger(0xFFE9E9): 4,
    Color.fromInteger(0xE0B0B): 7,
    Color.fromInteger(0xFFFDF9): 8,
    Color.fromInteger(0xFFCF9E): 9,
    Color.fromInteger(0x503F37): 10,
    Color.fromInteger(0xE0B0B): 11,
    Color.fromInteger(0xFFF8DD): 12,
    Color.fromInteger(0xFFFF9E): 13,
    Color.fromInteger(0x505037): 14,
    Color.fromInteger(0xE0E0B): 15,
    Color.fromInteger(0xF2FFDD): 16,
    Color.fromInteger(0xD8FF9E): 17,
    Color.fromInteger(0x435037): 18,
    Color.fromInteger(0xC0E0B): 19,
    Color.fromInteger(0xEDFFE9): 20,
    Color.fromInteger(0x375037): 22,
    Color.fromInteger(0xF1FFF1): 24,
    Color.fromInteger(0x9EFFB8): 25,
    Color.fromInteger(0x37503B): 26,
    Color.fromInteger(0xB0E0B): 27,
    Color.fromInteger(0xF1FFF3): 28,
    Color.fromInteger(0x375043): 30,
    Color.fromInteger(0xB0E0C): 31,
    Color.fromInteger(0xF1FFFC): 32,
    Color.fromInteger(0x9EFFF1): 33,
    Color.fromInteger(0x37504A): 34,
    Color.fromInteger(0xB0E0C): 35,
    Color.fromInteger(0xF1FCFF): 36,
    Color.fromInteger(0x9EF3FF): 37,
    Color.fromInteger(0x374B50): 38,
    Color.fromInteger(0xB0D0E): 39,
    Color.fromInteger(0xF1F7FF): 40,
    Color.fromInteger(0x9EDCFF): 41,
    Color.fromInteger(0x374350): 42,
    Color.fromInteger(0xB0C0E): 43,
    Color.fromInteger(0xD5CDFF): 44,
    Color.fromInteger(0x373750): 46,
    Color.fromInteger(0xB0B0E): 47,
    Color.fromInteger(0xF0E9FF): 48,
    Color.fromInteger(0xC59EFF): 49,
    Color.fromInteger(0x3D3750): 50,
    Color.fromInteger(0xB0B0E): 51,
    Color.fromInteger(0xFFE9FF): 52,
    Color.fromInteger(0xFF9EFF): 53,
    Color.fromInteger(0x503750): 54,
    Color.fromInteger(0xE0B0E): 55,
    Color.fromInteger(0xFFE9F2): 56,
    Color.fromInteger(0xFF9ED9): 57,
    Color.fromInteger(0x503743): 58,
    Color.fromInteger(0xE0B0C): 59,
    Color.fromInteger(0xFFAA9E): 60,
    Color.fromInteger(0x7A6951): 61,
    Color.fromInteger(0x504A37): 62,
    Color.fromInteger(0x60605): 63,
    Color.fromInteger(0xB0E0C): 65,
    Color.fromInteger(0x2B313C): 66,
    Color.fromInteger(0x9E9EFF): 67,
    Color.fromInteger(0xB0E0E): 68,
    Color.fromInteger(0x806EAC): 69,
    Color.fromInteger(0x2A2A2A): 70,
    Color.fromInteger(0x20202): 71,
    Color.fromInteger(0xFF9E9E): 72,
    Color.fromInteger(0xFAFFDD): 73,
    Color.fromInteger(0xDEE790): 74,
    Color.fromInteger(0xDFFF9E): 75,
    Color.fromInteger(0x3B5037): 76,
    Color.fromInteger(0x9EFFDF): 77,
    Color.fromInteger(0x9EF1FF): 78,
    Color.fromInteger(0x9EC4FF): 79,
    Color.fromInteger(0xB89EFF): 80,
    Color.fromInteger(0xCB90E7): 81,
    Color.fromInteger(0x927A8D): 82,
    Color.fromInteger(0x60505): 83,
    Color.fromInteger(0xFFC49E): 84,
    Color.fromInteger(0xC2D184): 86,
    Color.fromInteger(0x9EFF9E): 87,
    Color.fromInteger(0xE3FFDD): 88,
    Color.fromInteger(0xDFE7E0): 89,
    Color.fromInteger(0xE9FFFC): 90,
    Color.fromInteger(0xF6FAFF): 91,
    Color.fromInteger(0xA7AFBD): 92,
    Color.fromInteger(0xCAC7D1): 93,
    Color.fromInteger(0x6C586E): 94,
    Color.fromInteger(0xFF9EDF): 95,
    Color.fromInteger(0xFFD89E): 96,
    Color.fromInteger(0xEEFF9E): 98,
    Color.fromInteger(0x504C37): 99,
    Color.fromInteger(0x101410): 101,
    Color.fromInteger(0x181C19): 102,
    Color.fromInteger(0x25252A): 104,
    Color.fromInteger(0x2A2725): 105,
    Color.fromInteger(0x503737): 106,
    Color.fromInteger(0xD1BCB8): 107,
    Color.fromInteger(0xD1B598): 108,
    Color.fromInteger(0xFFF9CD): 109,
    Color.fromInteger(0xCCD1B8): 110,
    Color.fromInteger(0x8A926E): 111,
    Color.fromInteger(0x60606): 112,
    Color.fromInteger(0xD1D1CD): 113,
    Color.fromInteger(0xE4E7E4): 114,
    Color.fromInteger(0xFEFEFF): 115,
    Color.fromInteger(0xFBF9FF): 116,
    Color.fromInteger(0xE0E0E): 117,
    Color.fromInteger(0x3C3C3C): 118,
    Color.fromInteger(0xFFFFFF): 119,
    Color.fromInteger(0x7A5151): 120,
    Color.fromInteger(0x90808): 121,
    Color.fromInteger(0x86BD78): 122,
    Color.fromInteger(0xB0E0B): 123,
    Color.fromInteger(0xACA96E): 124,
    Color.fromInteger(0xE0D0B): 125,
    Color.fromInteger(0x928260): 126,
    Color.fromInteger(0x1C1716): 127,
}


# Algorithm to get more accurate colors
new = {}
newer = {}
for c, v in COLORS.items():
    rad = math.radians(c.value * 180 - 90)
    c = Color.fromHsv(c.hue, c.saturation, ((math.sin(rad) + 1) / 2))
    new[v] = c

for v in sorted(new.keys()):
    c = new[v]
    if c not in newer:
        newer[c] = v
    # print(f"    Color.fromInteger(0x{c.integer:X}): {v},")
