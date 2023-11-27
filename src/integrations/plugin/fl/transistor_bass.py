"""
integrations > plugin > fl > transistor_bass

Integration with FL Studio's Transistor Bass plugin

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""
from common.types import Color
from integrations.plugin import basicPluginBuilder

PARAMS = [
    0,  # Tuning
    1,  # Waveform
    2,  # Cutoff
    4,  # Resonance
    5,  # Envelope Modulation
    6,  # Decay
    7,  # Accent
    8,  # Volume
]

COLOR = Color.fromInteger(0x455765)

basicPluginBuilder(("Transistor Bass",), PARAMS, COLOR, uses_presets=True)
