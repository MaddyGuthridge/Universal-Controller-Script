from typing import Optional
from common.eventpattern import ByteMatch, BasicPattern
from common.types.eventdata import EventData, isEventStandard
from controlsurfaces import ControlEvent, ControlSurface
from . import IControlMatcher


class IndexedMatcher(IControlMatcher):
    """Indexed matchers are used to match control surfaces that are
    differentiated by their data1 value."""
    def __init__(
        self,
        status: int,
        data1: int,
        controls: list[ControlSurface]
    ) -> None:
        self.__pattern = BasicPattern(
            status,
            range(data1, data1 + len(controls)),
            ...
        )
        self.__start = data1
        self.__controls = controls

    def matchEvent(self, event: EventData) -> Optional[ControlEvent]:
        if not self.__pattern.matchEvent(event):
            return None
        assert isEventStandard(event)
        idx = event.data1 - self.__start
        match = self.__controls[idx].match(event)
        assert match is not None
        return match

    def getGroups(self) -> set[str]:
        ret = set()
        for c in self.__controls:
            ret |= {c.group}
        return ret

    def getControls(self, group: str = None) -> list[ControlSurface]:
        if group is None:
            return self.__controls
        else:
            ret = []
            for c in self.__controls:
                if c.group == group:
                    ret.append(c)
            return ret
