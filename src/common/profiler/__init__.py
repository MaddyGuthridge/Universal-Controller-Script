"""
common > profiler

Contains code used to profile the performance of the device
"""

__all__ = [
    'ProfilerContext',
    'profilerDecoration',
    'ProfilerManager',
]

from .profiler_context import ProfilerContext, profilerDecoration
from .manager import ProfilerManager
