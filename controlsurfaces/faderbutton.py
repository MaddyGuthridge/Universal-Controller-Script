"""
controlsurfaces > faderbutton

Classes representing fader buttons

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]
"""

from . import Button

class FaderButton(Button):
    """
    Represents buttons that are indexed to map to channels like faders
    """

class GenericFaderButton(Button):
    """
    Represents a generic multi-purpose fader button: the script should 
    intelligently map the behaviour to the other controls
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
