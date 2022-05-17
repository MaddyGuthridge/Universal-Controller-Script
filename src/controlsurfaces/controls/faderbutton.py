"""
controlsurfaces > faderbutton

Classes representing fader buttons

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]
"""

__all__ = [
    'FaderButton',
    'GenericFaderButton',
    'MasterGenericFaderButton',
    'MuteButton',
    'MasterMuteButton',
    'SoloButton',
    'MasterSoloButton',
    'ArmButton',
    'MasterArmButton',
    'SelectButton',
    'MasterSelectButton',
]

from ..eventpatterns.ieventpattern import IEventPattern
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
            coordinate
        )


class AbstractGenericFaderButton(FaderButton):
    """Generic fader button's abstract base class
    """


class GenericFaderButton(AbstractGenericFaderButton):
    """
    Represents a generic multi-purpose fader button: plugins should
    intelligently map the behaviour to required controls.
    """


class MasterGenericFaderButton(AbstractGenericFaderButton):
    """
    Represents a master generic multi-purpose fader button: plugins should
    intelligently map the behaviour to required controls.
    """

    def __init__(
        self,
        event_pattern: IEventPattern,
        value_strategy: IValueStrategy
    ) -> None:
        super().__init__(event_pattern, value_strategy, (0, 0))


class AbstractMuteButton(FaderButton):
    """
    Represents an abstract mute track button
    """


class MuteButton(AbstractMuteButton):
    """
    Represents a mute track button
    """


class MasterMuteButton(AbstractMuteButton):
    """
    Represents a master mute track button
    """

    def __init__(
        self,
        event_pattern: IEventPattern,
        value_strategy: IValueStrategy
    ) -> None:
        super().__init__(event_pattern, value_strategy, (0, 0))


class AbstractSoloButton(FaderButton):
    """
    Represents an abstract solo track button
    """


class SoloButton(AbstractSoloButton):
    """
    Represents a solo track button
    """


class MasterSoloButton(AbstractSoloButton):
    """
    Represents a master solo track button
    """

    def __init__(
        self,
        event_pattern: IEventPattern,
        value_strategy: IValueStrategy
    ) -> None:
        super().__init__(event_pattern, value_strategy, (0, 0))


class AbstractArmButton(FaderButton):
    """
    Represents an abstract arm track button
    """


class ArmButton(AbstractArmButton):
    """
    Represents a arm track button
    """


class MasterArmButton(AbstractArmButton):
    """
    Represents a master arm track button
    """

    def __init__(
        self,
        event_pattern: IEventPattern,
        value_strategy: IValueStrategy
    ) -> None:
        super().__init__(event_pattern, value_strategy, (0, 0))


class AbstractSelectButton(FaderButton):
    """
    Represents an abstract select track button
    """


class SelectButton(AbstractSelectButton):
    """
    Represents a select track button
    """


class MasterSelectButton(AbstractSelectButton):
    """
    Represents a master select track button
    """

    def __init__(
        self,
        event_pattern: IEventPattern,
        value_strategy: IValueStrategy
    ) -> None:
        super().__init__(event_pattern, value_strategy, (0, 0))
