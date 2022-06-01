"""
devices > novation > launchkey > incontrol > controls > drum_pad > drum_pad

Definition for the Launchkey drum pad base class

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""

from typing import TYPE_CHECKING
from control_surfaces.event_patterns import ForwardedPattern,  NotePattern
from common.types import Color
from control_surfaces.value_strategies import NoteStrategy, ForwardedStrategy
from control_surfaces import ControlSurface, DrumPad, MuteButton, SoloButton
from .. import ColorInControlSurface
from ...consts import DRUM_ROWS, DRUM_COLS
from control_surfaces.matchers import (
    BasicControlMatcher,
)


class ILkDrumPad(ControlSurface):  # pragma: no cover
    """
    Interface representing the methods used by classes created by the
    createLkDrumPadBase() function

    Note that these function are never called, they only serve to keep mypy
    happy
    """
    def __init__(
        self,
        coordinate: tuple[int, int],
        channel: int,
        note_num: int,
        colors: dict[Color, int]
    ) -> None:
        ...

    @classmethod
    def create(cls, row: int, col: int) -> 'ILkDrumPad':
        ...

    @staticmethod
    def getControlAssignmentPriorities() -> 'tuple[type[ControlSurface], ...]':
        ...


def createLkDrumPadBase(
    extends: type[ControlSurface]
) -> type[ILkDrumPad]:
    """
    Create a control surface type mapping to a Launchkey drum pad.

    This creates and returns a new class inheriting from the given class.

    ### Args:
    * `extends` (`type[ControlSurface]`): class to extend

    ### Returns:
    * `type[ControlSurface]`: new class
    """
    name = f"LkDrumPad{extends.__class__}"

    def constructor(
        self,
        coordinate: tuple[int, int],
        channel: int,
        note_num: int,
        colors: dict[Color, int]
    ) -> None:
        ColorInControlSurface.__init__(
            self,
            channel,
            note_num,
            colors,
        )
        extends.__init__(
            self,
            ForwardedPattern(2, NotePattern(note_num, channel)),
            ForwardedStrategy(NoteStrategy()),
            coordinate
        )

    @classmethod  # type: ignore
    def create(cls, row: int, col: int) -> 'ILkDrumPad':
        raise NotImplementedError()

    return type(
        name,
        (ColorInControlSurface, extends),
        {
            "__init__": constructor,
            "create": create
        }
    )


if not TYPE_CHECKING:
    LkDrumPad = createLkDrumPadBase(DrumPad)
    LkDrumPadMute = createLkDrumPadBase(MuteButton)
    LkDrumPadSolo = createLkDrumPadBase(SoloButton)
else:
    LkDrumPad = ILkDrumPad
    LkDrumPadMute = ILkDrumPad
    LkDrumPadSolo = ILkDrumPad


class LkDrumPadMatcher(BasicControlMatcher):
    """Matcher for launchkey drum pads"""
    def __init__(
        self,
        drum_type: type[ILkDrumPad],
        row_2_type: type[ILkDrumPad] = None,
    ) -> None:
        super().__init__()
        if row_2_type is None:
            row_2_type = drum_type

        for r, t in zip(range(DRUM_ROWS), [drum_type, row_2_type]):
            for c in range(DRUM_COLS):
                self.addControl(t.create(r, c), 10)
