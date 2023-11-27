"""
plugs > tick_filters

Filters that allow for filtering to be done of tick events. Note that these
can only be used to filter the overall plugin tick.

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""
__all__ = [
    'toWindowIndex',
    'toPluginIndex',
    'toGeneratorIndex',
    'toEffectIndex',
]

from .index import (
    toWindowIndex,
    toPluginIndex,
    toGeneratorIndex,
    toEffectIndex,
)
