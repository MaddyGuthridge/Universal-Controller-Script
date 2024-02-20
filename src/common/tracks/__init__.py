"""
A wrapper around track-like objects in FL Studio, allowing them to be
controlled in a more Pythonic manner.
"""
__all__ = [
    'AbstractTrack',
    'Channel',
    'MixerTrack',
    'PlaylistTrack',
]


from .abstract import AbstractTrack
from .channel import Channel
from .mixer_track import MixerTrack
from .playlist_track import PlaylistTrack
