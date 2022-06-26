"""
control_surfaces > event_patterns > union_pattern

Contains the definition for the union type event pattern, which allows events
to be detected if they match any of a number of patterns.

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]
"""

import random
from fl_classes import FlMidiMsg
from .event_pattern import IEventPattern


class UnionPattern(IEventPattern):
    """
    Represents the union of multiple event patterns. A match with any of those
    patterns is considered a match overall.
    """

    def __init__(self, *patterns: IEventPattern) -> None:
        """
        Create a UnionPattern, which will match with any of the given event
        patterns.

        Args:
        * `*patterns` (`IEventPattern`): event patterns to match, each as
        separate arguments. At least two patterns are expected
        """
        if len(patterns) < 2:
            raise ValueError("Expected at least two event patterns to union")
        self._patterns = patterns

    def matchEvent(self, event: FlMidiMsg) -> bool:
        return any(p.matchEvent(event) for p in self._patterns)

    def fulfil(self) -> FlMidiMsg:
        return random.choice(self._patterns).fulfil()
