"""
controlsurfaces > aftertouch

Contains the definition of aftertouch control surfaces

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]
"""

from common.eventpattern import BasicPattern, fromNibbles, IEventPattern
from . import ControlSurface, IValueStrategy, Data2Strategy, Data1Strategy


class AfterTouch(ControlSurface):
    """
    The definition of a generic aftertouch control surface.
    """
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
            value_strategy,
            "after touch",
            coordinate
        )


class ChannelAfterTouch(AfterTouch):
    """
    The definition of channel aftertouch, which represents the strongest key
    pressure out of all active keys
    """

    def __init__(
        self,
        channel: 'int|ellipsis' = ...  # noqa: F821
    ) -> None:
        super().__init__(
            BasicPattern(fromNibbles(0xD, channel), ..., ...),
            Data1Strategy()
        )


class NoteAfterTouch(AfterTouch):
    """
    The definition of note aftertouch, which represents the pressure of a
    single key
    """

    def __init__(
        self,
        note: int,
        channel: 'int|ellipsis' = ...  # noqa: F821
    ) -> None:
        super().__init__(
            BasicPattern(fromNibbles(0xA, channel), note, ...),
            Data2Strategy()
        )
