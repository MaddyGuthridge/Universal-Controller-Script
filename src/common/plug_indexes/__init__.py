"""
common > plug_indexes

Type definitions for plugin and window indexes.

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""
__all__ = [
    'FlIndex',
    'PluginIndex',
    'WindowIndex',
    'GeneratorIndex',
    'EffectIndex',
]


from .fl_index import FlIndex
from .plugin import PluginIndex
from .window import WindowIndex
from .generator import GeneratorIndex
from .effect import EffectIndex
