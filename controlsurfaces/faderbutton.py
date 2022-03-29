"""
controlsurfaces > faderbutton

Classes representing fader buttons

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]
"""

__all__ = [
    'FaderButton',
    'GenericFaderButton',
    'MuteButton',
    'SoloButton',
    'ArmButton',
    'SelectButton',
]

from common.eventpattern.ieventpattern import IEventPattern
from controlsurfaces.valuestrategies.ivaluestrategy import IValueStrategy
from . import Button


class FaderButton(Button):
    """
    Represents buttons that are indexed to map to channels like faders. Fader
    buttons are often present beneath faders, so their functionality should
    be mapped to the same channel that the existing button is using.
    """

    def __init__(
        self,
        event_pattern: IEventPattern,
        value_strategy: IValueStrategy,
        coordinate: tuple[int, int]
    ) -> None:
        super().__init__(
            event_pattern,
            value_strategy,
            "fader buttons",
            coordinate
        )


class GenericFaderButton(FaderButton):
    """
    Represents a generic multi-purpose fader button: plugins should
    intelligently map the behaviour to required controls.
    """


class MuteButton(FaderButton):
    """
    Represents a mute track button
    """


class SoloButton(FaderButton):
    """
    Represents a solo track button
    """


class ArmButton(FaderButton):
    """
    Represents an arm track button
    """


class SelectButton(FaderButton):
    """
    Represents a select track button
    """
