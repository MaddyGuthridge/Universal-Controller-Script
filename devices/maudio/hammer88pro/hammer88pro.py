

from typing import Optional
from common.eventpattern import BasicPattern, ForwardedPattern, ForwardedUnionPattern, NotePattern
from common.types import EventData
from common.extensionmanager import ExtensionManager
from controlsurfaces.valuestrategies import ForwardedStrategy, ButtonData2Strategy, Data2Strategy, NoteStrategy
from devices import Device, BasicControlMatcher
from devices.controlgenerators import NoteMatcher, PedalMatcher

from controlsurfaces import (
    NullEvent,
    Fader,
    Knob,
    DrumPad,
    PlayButton,
    StopButton,
    RecordButton,
    FastForwardButton,
    RewindButton,
    LoopButton,
    MetronomeButton,
    StandardModWheel,
    ChannelAfterTouch,
)
from .hammerpitch import HammerPitchWheel
from .jogmatcher import JogMatcher

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
            BasicPattern(0xFA, 0x0, 0x0)
        ))
        matcher.addControl(NullEvent(
            BasicPattern(0xFC, 0x0, 0x0)
        ))
        
        # Jog wheel stuff
        matcher.addSubMatcher(JogMatcher())
        
        # Notes and pedals
        matcher.addSubMatcher(NoteMatcher())
        matcher.addSubMatcher(PedalMatcher())
        matcher.addControl(ChannelAfterTouch())
        
        # Drum pads
        matcher.addControls([
            DrumPad(NotePattern(i, 9), NoteStrategy(), (i // 8, i % 8))
            for i in range(16)
        ])
        
        # Knobs
        matcher.addControls([
            Knob(
                ForwardedUnionPattern(3, BasicPattern(0xB0, i+80, ...)),
                ForwardedStrategy(Data2Strategy()),
                (0, i)
            ) for i in range(8)
        ])
        
        # Faders
        matcher.addControls([
            Fader(
                ForwardedUnionPattern(3, BasicPattern(0xB0, i+48, ...)),
                ForwardedStrategy(Data2Strategy()),
                (0, i)
            ) for i in range(9)
        ])
        # matcher.addControl(
        #     Fader(
        #         ForwardedUnionPattern(3, BasicPattern(0xB0, i+48, ...)),
        #         ForwardedStrategy(Data2Strategy()),
        #         (0, 9))
        #     for i in range(8)
        # )
        
        
        # Transport buttons
        matcher.addControl(StopButton(
            ForwardedPattern(3, BasicPattern(0xBF, 102, ...)),
            ForwardedStrategy(ButtonData2Strategy())
        ))
        matcher.addControl(PlayButton(
            ForwardedPattern(3, BasicPattern(0xBF, 103, ...)),
            ForwardedStrategy(ButtonData2Strategy())
        ))
        matcher.addControl(RecordButton(
            ForwardedPattern(3, BasicPattern(0xBF, 104, ...)),
            ForwardedStrategy(ButtonData2Strategy())
        ))
        matcher.addControl(RewindButton(
            ForwardedPattern(3, BasicPattern(0xBF, 105, ...)),
            ForwardedStrategy(ButtonData2Strategy())
        ))
        matcher.addControl(FastForwardButton(
            ForwardedPattern(3, BasicPattern(0xBF, 106, ...)),
            ForwardedStrategy(ButtonData2Strategy())
        ))
        matcher.addControl(LoopButton(
            ForwardedPattern(3, BasicPattern(0xBF, 107, ...)),
            ForwardedStrategy(ButtonData2Strategy())
        ))
        matcher.addControl(MetronomeButton(
            ForwardedPattern(3, BasicPattern(0xB9, 0x74, ...)),
            ForwardedStrategy(ButtonData2Strategy())
        ))
        matcher.addControl(StandardModWheel())
        matcher.addControl(HammerPitchWheel())
        
        super().__init__(matcher)
    
    @staticmethod
    def getDrumPadSize() -> tuple[int, int]:
        return 2, 8
    
    @classmethod
    def create(cls, event: Optional[EventData]) -> Device:
        return cls()
    
    @staticmethod
    def getId() -> str:
        return "Maudio.Hammer88Pro"
    
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
