
from common.eventpattern import BasicEventPattern, fromNibbles, IEventPattern
from . import ControlSurface, IValueStrategy, Data2Strategy, Data1Strategy

class AfterTouch(ControlSurface):
    @staticmethod
    def getControlAssignmentPriorities() -> 'tuple[type[ControlSurface], ...]':
        # Allow substitution between different aftertouch types
        return (AfterTouch,)
    
    def __init__(
        self,
        event_pattern: IEventPattern,
        value_strategy: IValueStrategy,
        coordinate: tuple[int, int] = (0, 0)
    ) -> None:
        super().__init__(
            event_pattern,
            Data2Strategy(),
            "after touch",
            coordinate
        )

class ChannelAfterTouch(AfterTouch):
    def __init__(self, channel: 'int|ellipsis' = ...) -> None:
        super().__init__(
            BasicEventPattern(fromNibbles(0xD,channel), ..., ...),
            Data1Strategy()
            )

class NoteAfterTouch(AfterTouch):
    def __init__(self, note: int, channel: 'int|ellipsis' = ...) -> None:
        super().__init__(
            BasicEventPattern(fromNibbles(0xA,channel), note, ...),
            Data1Strategy()
            )
