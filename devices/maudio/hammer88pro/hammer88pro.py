

from typing import Optional
from common.eventpattern import BasicEventPattern, ForwardedEventPattern
from common.types import eventData
from common.extensionmanager import ExtensionManager
from controlsurfaces.valuestrategies import ForwardedStrategy, ButtonData2Strategy
from devices import Device, BasicControlMatcher
from devices.controlgenerators import getNotesAllChannels, getPedals

from controlsurfaces import (
    NullEvent,
    Fader,
    Knob,
    PlayButton,
    StopButton,
    RecordButton,
    FastForwardButton,
    RewindButton,
    LoopButton,
    MetronomeButton,
    ModWheel,
    PitchWheel
)
from controlsurfaces import (
    DirectionNext,
    DirectionPrevious
)

class Hammer88Pro(Device):
    """
    Device definition for Hammer 88 Pro

    Note: this requires the presets for both DAW and User modes to be loaded
    on the device.
    """
    def __init__(self) -> None:
        matcher = BasicControlMatcher()
        # Null events
        matcher.addControl(NullEvent(
            BasicEventPattern(0xFA, 0x0, 0x0)
        ))
        matcher.addControl(NullEvent(
            BasicEventPattern(0xFC, 0x0, 0x0)
        ))
        
        # Notes and pedals
        matcher.addControls(getNotesAllChannels())
        matcher.addControls(getPedals())
        
        # Transport buttons
        matcher.addControl(StopButton(
            ForwardedEventPattern(3, BasicEventPattern(0xBF, 102, ...)),
            ForwardedStrategy(ButtonData2Strategy()),
            "transport"
        ))
        matcher.addControl(PlayButton(
            ForwardedEventPattern(3, BasicEventPattern(0xBF, 103, ...)),
            ForwardedStrategy(ButtonData2Strategy()),
            "transport"
        ))
        matcher.addControl(RecordButton(
            ForwardedEventPattern(3, BasicEventPattern(0xBF, 104, ...)),
            ForwardedStrategy(ButtonData2Strategy()),
            "transport"
        ))
        matcher.addControl(RewindButton(
            ForwardedEventPattern(3, BasicEventPattern(0xBF, 105, ...)),
            ForwardedStrategy(ButtonData2Strategy()),
            "transport"
        ))
        matcher.addControl(FastForwardButton(
            ForwardedEventPattern(3, BasicEventPattern(0xBF, 106, ...)),
            ForwardedStrategy(ButtonData2Strategy()),
            "transport"
        ))
        matcher.addControl(LoopButton(
            ForwardedEventPattern(3, BasicEventPattern(0xBF, 107, ...)),
            ForwardedStrategy(ButtonData2Strategy()),
            "transport"
        ))
        matcher.addControl(MetronomeButton(
            ForwardedEventPattern(3, BasicEventPattern(0xB9, 0x74, ...)),
            ForwardedStrategy(ButtonData2Strategy()),
            "transport"
        ))
        matcher.addControl(ModWheel())
        matcher.addControl(PitchWheel())
        
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
