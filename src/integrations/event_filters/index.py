"""
integrations > event_filters > index

Contains filters for filtering by plugin and window indexes

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""
from common.plug_indexes import (
    FlIndex,
    PluginIndex,
    GeneratorIndex,
    EffectIndex,
    WindowIndex,
)
from .decorator import do_filter


@do_filter
def toPluginIndex(control, index: FlIndex, *args, **kwargs):
    """
    Filter out events when the index is not a plugin
    """
    return isinstance(index, PluginIndex)


@do_filter
def toGeneratorIndex(control, index: FlIndex, *args, **kwargs):
    """
    Filter out events when the index is not a generator plugin
    """
    return isinstance(index, GeneratorIndex)


@do_filter
def toEffectIndex(control, index: FlIndex, *args, **kwargs):
    """
    Filter out events when the index is not an effect plugin
    """
    return isinstance(index, EffectIndex)


@do_filter
def toWindowIndex(control, index: FlIndex, *args, **kwargs):
    """
    Filter out events when the index is not a window
    """
    return isinstance(index, WindowIndex)
