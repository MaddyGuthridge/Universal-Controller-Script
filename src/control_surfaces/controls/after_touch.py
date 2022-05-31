"""
control_surfaces > controls > after_touch

Contains the definition of after-touch control surfaces

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""

from ..event_patterns import BasicPattern, fromNibbles, IEventPattern
from . import ControlSurface
from ..value_strategies import IValueStrategy, Data2Strategy, Data1Strategy


class AfterTouch(ControlSurface):
    """
    The definition of a generic after-touch control surface.
    """
    @staticmethod
    def getControlAssignmentPriorities() -> 'tuple[type[ControlSurface], ...]':
        # Allow substitution between different after-touch types
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
            coordinate
        )


class ChannelAfterTouch(AfterTouch):
    """
    The definition of channel after-touch, which represents the strongest key
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
    The definition of note after-touch, which represents the pressure of a
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
