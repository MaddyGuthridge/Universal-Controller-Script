"""
devices > control_generators

Contains definitions for helper functions for creating and binding common
controls quickly.

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""

__all__ = [
    'NoteMatcher',
    'NoteAfterTouchMatcher',
    'PedalMatcher',
]

from .notes import NoteMatcher, NoteAfterTouchMatcher
from .pedals import PedalMatcher
