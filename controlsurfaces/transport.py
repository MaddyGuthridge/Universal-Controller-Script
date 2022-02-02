"""
controlsurfaces > transport

Defines transport control surfaces

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]
"""
from .button import Button

class TransportButton(Button):
    pass

class PlayButton(TransportButton):
    pass

class StopButton(TransportButton):
    pass

class LoopButton(TransportButton):
    pass

class RecordButton(TransportButton):
    pass

class FastForwardButton(TransportButton):
    pass

class RewindButton(TransportButton):
    pass

class MetronomeButton(TransportButton):
    pass
