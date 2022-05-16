from typing import Optional
from controlsurfaces.eventpattern import (
    IEventPattern,
    BasicPattern,
    ForwardedPattern
)
from common.types.eventdata import EventData, isEventStandard
from common.util.events import decodeForwardedEvent
from controlsurfaces import ControlEvent, ControlSurface
from . import IControlMatcher


class IndexedMatcher(IControlMatcher):
    """Indexed matchers are used to match control surfaces that are
    differentiated by their data1 value."""
    def __init__(
        self,
        status: int,
        data1: int,
        controls: list[ControlSurface],
        device: int = 1,
    ) -> None:
        self.__pattern: IEventPattern = BasicPattern(
            status,
            range(data1, data1 + len(controls)),
            ...
        )
        self.__start = data1
        self.__controls = controls

        if device != 1:
            self.__forwarded = True
            self.__pattern = ForwardedPattern(device, self.__pattern)
        else:
            self.__forwarded = False

    def matchEvent(self, event: EventData) -> Optional[ControlEvent]:
        if not self.__pattern.matchEvent(event):
            return None
        if self.__forwarded:
            decoded = decodeForwardedEvent(event)
        else:
            decoded = event
        assert isEventStandard(decoded)
        idx = decoded.data1 - self.__start
        match = self.__controls[idx].match(event)
        assert match is not None
        return match

    def getControls(self) -> list[ControlSurface]:
        return self.__controls

    def tick(self, thorough: bool) -> None:
        for c in self.__controls:
            c.doTick(thorough)
