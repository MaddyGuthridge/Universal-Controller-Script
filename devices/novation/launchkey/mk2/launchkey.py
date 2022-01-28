
from common.eventpattern import EventPattern
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
    RewindButton
)

class LaunchkeyMk2(Device):
    
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
        
        # Create knobs
        for i in range(1, 8):
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
                EventPattern(0xBF, 0x72, ...),
                Data2Strategy(),
                "transport"
            )
        )
        matcher.addControl(
            PlayButton(
                EventPattern(0xBF, 0x73, ...),
                Data2Strategy(),
                "transport"
            )
        )
        # matcher.addControl(
        #     LoopButton(
        #         EventPattern(0xBF, 0x74, ...),
        #         Data2Strategy(),
        #         "transport"
        #     )
        # )
        matcher.addControl(
            RecordButton(
                EventPattern(0xBF, 0x75, ...),
                Data2Strategy(),
                "transport"
            )
        )
        # matcher.addControl(
        #     NextButton(
        #         EventPattern(0xBF, 0x67, ...),
        #         Data2Strategy(),
        #         "transport"
        #     )
        # )
        # matcher.addControl(
        #     PreviousButton(
        #         EventPattern(0xBF, 0x66, ...),
        #         Data2Strategy(),
        #         "transport"
        #     )
        # )
        
        super().__init__(
            matcher
        )
