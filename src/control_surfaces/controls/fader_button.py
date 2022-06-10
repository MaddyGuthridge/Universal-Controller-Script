"""
control_surfaces > controls > fader_button

Classes representing fader buttons.

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""
from . import Button

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


class FaderButton(Button):
    """
    Represents buttons that are indexed to map to channels like faders. Fader
    buttons are often present beneath faders, so their functionality should
    be mapped to the same channel that the existing button is using.
    """


class AbstractGenericFaderButton(FaderButton):
    """Generic fader button's abstract base class
    """


class GenericFaderButton(AbstractGenericFaderButton):
    """
    Represents a generic multi-purpose fader button: plugins should
    intelligently map the behavior to required controls.
    """


class MasterGenericFaderButton(AbstractGenericFaderButton):
    """
    Represents a master generic multi-purpose fader button: plugins should
    intelligently map the behavior to required controls.
    """


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
