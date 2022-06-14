"""
devices > novation > launchkey > incontrol > controls > metronome > mk2

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""
from ...colors.mk2 import COLORS
from control_surfaces.event_patterns import ForwardedPattern,  NotePattern
from control_surfaces.value_strategies import NoteStrategy, ForwardedStrategy
from control_surfaces import MetronomeButton
from ..incontrol_surface import ColorInControlSurface


class LkMk2MetronomeButton(MetronomeButton):
    """
    Custom drum pad implementation used by Launchkey series controllers
    to provide RGB functionality
    """
    def __init__(self,) -> None:
        channel = 0xF
        note_num = 0x78
        event_num = 0x9
        super().__init__(
            ForwardedPattern(2, NotePattern(note_num, channel)),
            ForwardedStrategy(NoteStrategy()),
            color_manager=ColorInControlSurface(
                channel,
                note_num,
                COLORS,
                event_num,
            ),
        )
