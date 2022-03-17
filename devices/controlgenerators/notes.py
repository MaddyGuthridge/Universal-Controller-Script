"""
devices > controlgenerators > notes

Contains custom control matchers for the note and note aftertouch
event types

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]
"""

from typing import Optional
from common.eventpattern import BasicPattern, fromNibbles
from common.types.eventdata import EventData, isEventStandard
from controlsurfaces import ControlSurface, Note, NoteAfterTouch
from controlsurfaces.controlmapping import ControlEvent
from devices.matchers import IControlMatcher

class NoteMatcher(IControlMatcher):
    """
    Defines a matcher for note events
    """
    def __init__(self) -> None:
        self._notes: list[ControlSurface] = [Note(i) for i in range(128)]
        # A pattern to match any and all notes (this improves efficiency by
        # allowing us to only try to match events that are already notes)
        self._note_pattern = BasicPattern(
            fromNibbles((8, 9), ...),
            ...,
            ...
        )
        super().__init__()

    def matchEvent(self, event: EventData) -> Optional[ControlEvent]:
        if isEventStandard(event) and self._note_pattern.matchEvent(event):
            note = event.data1
            return self._notes[note].match(event)
        else:
            return None

    def getGroups(self) -> set[str]:
        return {"notes"}

    def getControls(self, group: str = None) -> list[ControlSurface]:
        return self._notes

class NoteAfterTouchMatcher(IControlMatcher):
    """
    Defines a matcher for note after-touch events
    """
    def __init__(self) -> None:
        self._touches: list[ControlSurface] = [NoteAfterTouch(i) for i in range(128)]
        self._touch_pattern = BasicPattern(
            fromNibbles((0xA), ...),
            ...,
            ...
        )
        super().__init__()

    def matchEvent(self, event: EventData) -> Optional[ControlEvent]:
        if isEventStandard(event) and self._touch_pattern.matchEvent(event):
            note = event.data1
            return self._touches[note].match(event)
        else:
            return None

    def getGroups(self) -> set[str]:
        return {"after touch"}

    def getControls(self, group: str = None) -> list[ControlSurface]:
        return self._touches
