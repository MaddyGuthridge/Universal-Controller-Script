"""
integrations > window

Integrations for interacting with FL Studio windows

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""
__all__ = [
    'Mixer',
    'ChannelRack',
    'Playlist',
    'PianoRoll',
    'Browser',
]

from .mixer import Mixer
from .channel_rack import ChannelRack
from .playlist import Playlist
from .piano_roll import PianoRoll
from .browser import Browser
