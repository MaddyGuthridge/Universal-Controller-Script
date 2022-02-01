

from typing import Optional
from common.eventpattern import EventPattern
from common.types import eventData
from common.extensionmanager import ExtensionManager
from controlsurfaces.valuestrategies import Data2Strategy
from devices import Device
from devices import BasicControlMatcher

from controlsurfaces import (
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

ID_PREFIX = "Maudio.Hammer88Pro"

class Hammer88Pro(Device):
    
    def __init__(self) -> None:
        super().__init__(BasicControlMatcher())
    
    @classmethod
    def create(cls, event: Optional[eventData]) -> Device:
        return cls()
    
    @staticmethod
    def getId() -> str:
        return f"{ID_PREFIX}"
    
    @staticmethod
    def getUniversalEnquiryResponsePattern():
        return EventPattern(
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
