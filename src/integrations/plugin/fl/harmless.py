"""
integrations > plugin > fl > harmless

Integration for FL Studio's Harmless plugin

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""
from common.types import Color
from integrations.plugin import basicPluginBuilder

PARAMS = [
    31,  # Pluck
    65,  # Unison
    79,  # Harmonizer
    71,  # Phaser
    91,  # Chorus
    94,  # Delay feedback
    97,  # Reverb
    98,  # Compression
]

COLOR = Color.fromInteger(0x47353f)

basicPluginBuilder(("Harmless",), PARAMS, COLOR, uses_presets=True)
