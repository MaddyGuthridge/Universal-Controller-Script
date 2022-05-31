"""
common > plug_indexes

Type definitions for plugin indexes.

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""
from typing import Optional, Union

GeneratorIndex = tuple[int]
UnsafeGeneratorIndex = Optional[GeneratorIndex]

EffectIndex = tuple[int, int]
UnsafeEffectIndex = Optional[EffectIndex]

PluginIndex = Union[GeneratorIndex, EffectIndex]
UnsafePluginIndex = Optional[PluginIndex]

WindowIndex = int
UnsafeWindowIndex = Optional[int]

UnsafeIndex = Union[UnsafePluginIndex, UnsafeWindowIndex]
