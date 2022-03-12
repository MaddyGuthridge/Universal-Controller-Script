"""
controlsurfaces > faderbutton

Classes representing fader buttons

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]
"""

from . import Button

class FaderButton(Button):
    """
    Represents buttons that are indexed to map to channels like faders. Fader
    buttons are often present beneath faders, so their functionality should
    be mapped to the same channel that the existing button is using.
    """

class GenericFaderButton(Button):
    """
    Represents a generic multi-purpose fader button: plugins should
    intelligently map the behaviour to required controls.
    """

class MuteButton(Button):
    """
    Represents a mute track button
    """

class SoloButton(Button):
    """
    Represents a solo track button
    """

class ArmButton(Button):
    """
    Represents an arm track button
    """

class SelectButton(Button):
    """
    Represents a select track button
    """
