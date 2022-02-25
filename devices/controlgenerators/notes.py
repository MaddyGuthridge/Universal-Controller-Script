
from typing import Optional
from common.eventpattern import BasicPattern, fromNibbles
from common.types.eventdata import EventData, isEventStandard
from controlsurfaces import ControlSurface, Note, NoteAfterTouch, ChannelAfterTouch
from controlsurfaces.controlmapping import ControlEvent
from devices.matchers import IControlMatcher

class NoteMatcher(IControlMatcher):
    def __init__(self) -> None:
        self._notes: list[ControlSurface] = [Note(i) for i in range(128)]
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
