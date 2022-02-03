"""
controlsurfaces > transport

Defines transport control surfaces

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]
"""
from common.eventpattern import IEventPattern
from controlsurfaces.valuestrategies import IValueStrategy
from .button import Button

class TransportButton(Button):
    def __init__(self, event_pattern: IEventPattern, value_strategy: IValueStrategy) -> None:
        super().__init__(event_pattern, value_strategy, "transport")

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
