
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

ID_PREFIX = "Novation.Launchkey.Mk2"

class LaunchkeyMk2(Device):
    """
    Novation Launchkey Mk2 series controllers
    """
    
    def __init__(self, matcher) -> None:
        
        # Faders added by child classes if necessary
        
        # Create knobs
        for i in range(1, 9):
            matcher.addControl(
                Knob(
                    EventPattern(0xB0, 0x14 + i, ...),
                    Data2Strategy(),
                    "knobs",
                    (i, 0)
                )
            )
        
        # Transport
        matcher.addControl(
            StopButton(
                EventPattern(0xB0, 0x72, ...),
                Data2Strategy(),
                "transport"
            )
        )
        matcher.addControl(
            PlayButton(
                EventPattern(0xB0, 0x73, ...),
                Data2Strategy(),
                "transport"
            )
        )
        matcher.addControl(
            LoopButton(
                EventPattern(0xB0, 0x74, ...),
                Data2Strategy(),
                "transport"
            )
        )
        matcher.addControl(
            RecordButton(
                EventPattern(0xB0, 0x75, ...),
                Data2Strategy(),
                "transport"
            )
        )
        matcher.addControl(
            DirectionNext(
                EventPattern(0xB0, 0x66, ...),
                Data2Strategy(),
                "transport"
            )
        )
        matcher.addControl(
            DirectionPrevious(
                EventPattern(0xB0, 0x67, ...),
                Data2Strategy(),
                "transport"
            )
        )
        matcher.addControl(
            RewindButton(
                EventPattern(0xB0, 0x70, ...),
                Data2Strategy(),
                "transport"
            )
        )
        matcher.addControl(
            FastForwardButton(
                EventPattern(0xB0, 0x71, ...),
                Data2Strategy(),
                "transport"
            )
        )
        
        super().__init__(
            matcher
        )
        
class LaunchkeyMk2_49_61(LaunchkeyMk2):
    """
    Standard controls with added faders
    """
    def __init__(self) -> None:
        matcher = BasicControlMatcher()
        
        # Create faders
        for i in range(1, 9):
            matcher.addControl(
                Fader(
                    EventPattern(0xB0, 0x28 + i, ...),
                    Data2Strategy(),
                    "faders",
                    (i, 0)
                )
            )
        # Master fader
        matcher.addControl(
            Fader(
                EventPattern(0xB0, 0x07, ...),
                Data2Strategy(),
                "knobs",
                (0, 0)
            )
        )
        
        super().__init__(matcher)

    @classmethod
    def create(cls, event: Optional[eventData]) -> Device:
        return cls()
    
    @staticmethod
    def getId() -> str:
        return f"{ID_PREFIX}.49-61"
    
    @staticmethod
    def getUniversalEnquiryResponsePattern():
        return EventPattern(
            [0xF0, 0x7E, 0x00, 0x06, 0x02, 0x00, 0x20, 0x29, (0x7C, 0x7D)]
        )
    
    @staticmethod
    def matchDeviceName(name: str) -> bool:
        """Controller can't be matched to FL device name"""
        return False

class LaunchkeyMk2_25(LaunchkeyMk2):
    """
    Standard controls with no faders
    """
    def __init__(self) -> None:
        super().__init__(BasicControlMatcher())

    @classmethod
    def create(cls, event: Optional[eventData]) -> Device:
        return cls()

    @staticmethod
    def getId() -> str:
        return f"{ID_PREFIX}.25"

    @staticmethod
    def getUniversalEnquiryResponsePattern():
        return EventPattern(
            [0xF0, 0x7E, 0x00, 0x06, 0x02, 0x00, 0x20, 0x29, 0x7B]
        )
    
    @staticmethod
    def matchDeviceName(name: str) -> bool:
        """Controller can't be matched to FL device name"""
        return False

# Register devices
ExtensionManager.registerDevice(LaunchkeyMk2_49_61)
ExtensionManager.registerDevice(LaunchkeyMk2_25)
