
from typing import Optional
from common.eventpattern import BasicPattern
from common.types import EventData
from common.extensionmanager import ExtensionManager
from controlsurfaces.valuestrategies import Data2Strategy,ButtonData2Strategy
from devices import Device, BasicControlMatcher
from devices.controlgenerators import NoteMatcher

from controlsurfaces import (
    Knob
)
from controlsurfaces import (
    DirectionNext,
    DirectionPrevious
)
from .drumpad import LaunchkeyDrumpad

class LaunchkeyMiniMk2(Device):
    """
    Novation Launchkey Mini Mk2 controller
    """
    
    def __init__(self) -> None:
        matcher = BasicControlMatcher()
        
        # Notes
        matcher.addSubMatcher(NoteMatcher())
        
        # Drum pads (high priority because they just use note on events)
        for r in range(self.getDrumPadSize()[0]):
            for c in range(self.getDrumPadSize()[1]):
                matcher.addControl(LaunchkeyDrumpad((r, c)), 10)
        
        # Create knobs
        for i in range(1, 9):
            matcher.addControl(
                Knob(
                    BasicPattern(0xB0, 0x14 + i, ...),
                    Data2Strategy(),
                    (i, 0)
                )
            )
        
        # Transport
        matcher.addControl(DirectionNext(
            BasicPattern(0xB0, 0x66, ...),
            ButtonData2Strategy()
        ))
        matcher.addControl(DirectionPrevious(
            BasicPattern(0xB0, 0x67, ...),
            ButtonData2Strategy(),
        ))
        
        super().__init__(matcher)
    
    @staticmethod
    def getDrumPadSize() -> tuple[int, int]:
        return 2, 8
    
    @staticmethod
    def getUniversalEnquiryResponsePattern():
        return BasicPattern(
            [
                0xF0, # Sysex start
                0x7E, # Device response
                ..., # OS Device ID
                0x06, # Separator
                0x02, # Separator
                0x00, # Manufacturer
                0x20, # Manufacturer
                0x29, # Manufacturer
                tuple()
                # (0x7C, 0x7D) # Family code (documented as 0x7A???)
            ]
        )
        
    @classmethod
    def create(cls, event: Optional[EventData]) -> Device:
        return cls()
    
    @staticmethod
    def getId() -> str:
        return 'Novation.Launchkey.Mini.Mk2'

    @staticmethod
    def matchDeviceName(name: str) -> bool:
        """Controller can't be matched to FL device name"""
        return False

# Register devices
ExtensionManager.registerDevice(LaunchkeyMiniMk2)
