"""
common > profiler

Contains code used to profile the performance of the device

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""

__all__ = [
    'ProfilerContext',
    'profilerDecoration',
    'ProfilerManager',
]

from .profiler_context import ProfilerContext, profilerDecoration
from .manager import ProfilerManager
