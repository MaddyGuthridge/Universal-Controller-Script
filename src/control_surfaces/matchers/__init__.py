"""
devices > matchers

Contains definitions for objects related to control matching

Authors:
* Maddy Guthridge [hello@maddyguthridge.com, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""

__all__ = [
    'IControlMatcher',
    'BasicControlMatcher',
    'IndexedMatcher',
    'ShiftMatcher',
    'ShiftView',
    'NoteMatcher',
    'NoteAfterTouchMatcher',
    'PedalMatcher',
]

from .control_matcher import IControlMatcher
from .basic_matcher import BasicControlMatcher
from .indexed_matcher import IndexedMatcher
from .shift_matcher import ShiftMatcher, ShiftView
from .notes import NoteMatcher, NoteAfterTouchMatcher
from .pedals import PedalMatcher
