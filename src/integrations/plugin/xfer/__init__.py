"""
integrations > plugin > xfer

Adds support for some XFER plugins
* Serum
* OTT

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""

from common.types import Color
from integrations.plugin import basicPluginBuilder


# Serum
basicPluginBuilder(
    ('Serum',),
    [218, 219, 220, 221],
    Color.fromInteger(0x206cc8),
)


# OTT
basicPluginBuilder(
    ('OTT',),
    list(range(4)),
    Color.fromInteger(0xb1c1cf),
)
