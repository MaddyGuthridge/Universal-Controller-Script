"""
plugs > standard > xfer

Adds support for some XFER plugins
* Serum
* OTT

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""

from common.types import Color
from plugs.standard import basicFaderBuilder


SERUM_COLOR = Color.fromInteger(0x206cc8)
basicFaderBuilder(
    ('Serum',),
    [45, 46, 35, 37, 218, 219, 220, 221],
    SERUM_COLOR
)


OTT_COLOR = Color.fromInteger(0xb1c1cf)
basicFaderBuilder(
    ('OTT',),
    list(range(4)),
    OTT_COLOR
)
