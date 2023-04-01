"""
devices > novation > sl > mk3 > controls > drum_pad

Definition for the SL Mk3 drum pads

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""
from control_surfaces import ControlSurface, DrumPad
from control_surfaces.event_patterns import ForwardedPattern, NotePattern
from control_surfaces.value_strategies import NoteStrategy, ForwardedStrategy
from . import SlColorSurface
from control_surfaces.matchers import (
    BasicControlMatcher,
)


DRUM_NOTES = [
    [i + 0x60 for i in range(8)],
    [i + 0x70 for i in range(8)]
]
DRUM_LIGHTS = [
    [i + 0x26 for i in range(8)],
    [i + 0x2E for i in range(8)]
]


class ISlDrumPad(ControlSurface):  # pragma: no cover
    """
    Interface representing the methods used by classes created by the
    createSlDrumPadBase() function

    Note that these functions are never called, they only serve to keep mypy
    happy
    """
    def __init__(
        self,
        coordinate: tuple[int, int],
    ) -> None:
        raise NotImplementedError("ISlDrumPad")

    @classmethod
    def create(cls, row: int, col: int) -> 'ISlDrumPad':
        raise NotImplementedError("ISlDrumPad")

    @staticmethod
    def getControlAssignmentPriorities() -> 'tuple[type[ControlSurface], ...]':
        raise NotImplementedError("ISlDrumPad")

    def onColorChange(self, *args):
        raise NotImplementedError("ISlDrumPad")


def createSlDrumPadBase(kind: type[ControlSurface]) -> type[ISlDrumPad]:
    name = f"SlDrumPad{kind.__class__}"

    def constructor(
        self,
        coordinate: tuple[int, int],
    ) -> None:
        r, c = coordinate
        kind.__init__(
            self,
            ForwardedPattern(2, NotePattern(DRUM_NOTES[r][c], 0xF)),
            ForwardedStrategy(NoteStrategy()),
            coordinate,
            color_manager=SlColorSurface(DRUM_LIGHTS[r][c])
        )

    @classmethod  # type: ignore
    def create(cls, row: int, col: int) -> 'ISlDrumPad':
        raise NotImplementedError("Bruh")

    return type(
        name,
        (kind,),
        {
            "__init__": constructor,
            "create": create
        }
    )


class SlDrumPadMatcher(BasicControlMatcher):
    """Matcher for SL drum pads"""
    def __init__(self, kind: type[ControlSurface] = DrumPad) -> None:
        super().__init__()
        sl_drum_pad = createSlDrumPadBase(kind)
        for r in range(2):
            for c in range(8):
                self.addControl(sl_drum_pad((r, c)), 10)
