"""
plugs > standard > matt_tytel > vital

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""
from common.types import Color
from plugs.standard import basicFaderBuilder

MACRO_START = 211
VITAL_COLOR = Color.fromInteger(0xAA88FF)

basicFaderBuilder(('Vital',), [MACRO_START + i for i in range(4)], VITAL_COLOR)
