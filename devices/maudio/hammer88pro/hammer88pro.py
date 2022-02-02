

from typing import Optional
from common.eventpattern import BasicEventPattern, ForwardedEventPattern
from common.types import eventData
from common.extensionmanager import ExtensionManager
from controlsurfaces.valuestrategies import Data2Strategy, ButtonSinglePressStrategy
from devices import Device
from devices import BasicControlMatcher

from controlsurfaces import (
    NullEvent,
    Fader,
    Knob,
    PlayButton,
    StopButton,
    RecordButton,
    FastForwardButton,
    RewindButton,
    LoopButton
)
from controlsurfaces import (
    DirectionNext,
    DirectionPrevious
)
from .buttondatastrat import HammerButtonStrat

class Hammer88Pro(Device):
    
    def __init__(self) -> None:
        matcher = BasicControlMatcher()
        # Null events
        matcher.addControl(NullEvent(
            BasicEventPattern(0xFA, 0x0, 0x0)
        ))
        matcher.addControl(NullEvent(
            BasicEventPattern(0xFC, 0x0, 0x0)
        ))
        matcher.addControl(NullEvent(
            ForwardedEventPattern(3, BasicEventPattern(0xB0, 0x0F, 0x0E))
        ))
        
        # Transport buttons
        matcher.addControl(PlayButton(
            ForwardedEventPattern(3, BasicEventPattern(0xB0, 0x2F, (0x44, 0x4))),
            HammerButtonStrat(0x44),
            "transport"
        ))
        
        super().__init__(matcher)
    
    @classmethod
    def create(cls, event: Optional[eventData]) -> Device:
        return cls()
    
    @staticmethod
    def getId() -> str:
        return "Maudio.Hammer88Pro"
    
    @staticmethod
    def getUniversalEnquiryResponsePattern():
        return BasicEventPattern(
            [
                0xF0, # Sysex start
                0x7E, # Device response
                ..., # OS Device ID
                0x06, # Separator
                0x02, # Separator
                0x00, # Manufacturer
                0x01, # Manufacturer
                0x05, # Manufacturer
                0x00, # Family code
                0x3C, # Family code
                # Extra details omitted
                ]
        )

    @staticmethod
    def matchDeviceName(name: str) -> bool:
        """Controller can't be matched to FL device name"""
        return False

ExtensionManager.registerDevice(Hammer88Pro)
