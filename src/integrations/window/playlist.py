"""
integrations > window > playlist

Integration for FL Studio's playlist

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""
from typing import Any, cast
import arrangement
import ui
import playlist
import patterns
import transport
import general
from common import getContext
from common.tracks import PlaylistTrack
from common.types import Color
from common.extension_manager import ExtensionManager
from common.plug_indexes import WindowIndex, FlIndex
from common.util.api_fixes import getFirstPlaylistSelection
from control_surfaces import consts
from control_surfaces import ControlShadowEvent
from control_surfaces import (
    MoveJogWheel,
    StandardJogWheel,
    JogWheel,
    ToolSelector,
    DirectionNext,
    DirectionPrevious,
    DirectionLeft,
    DirectionRight,
    DirectionUp,
    DirectionDown,
)
from devices import DeviceShadow
from integrations import WindowIntegration
from integrations.event_filters import filterButtonLift
from integrations.mapping_strategies import MuteSoloStrategy

# Thanks, https://stackoverflow.com/a/8081580/6335363
TOOL_COLORS, TOOL_NAMES = cast(
    tuple[list[Color], list[str]],
    map(list, zip(*[
        (Color.fromInteger(0xffc43f),  "Pencil"),
        (Color.fromInteger(0x7bcefd),  "Paint"),
        (Color.fromInteger(0xfe5750),  "Delete"),
        (Color.fromInteger(0xff54b0),  "Mute"),
        (Color.fromInteger(0xffa64a),  "Slip"),
        (Color.fromInteger(0x85b3f2),  "Slice"),
        (Color.fromInteger(0xff9354),  "Select"),
        (Color.fromInteger(0x80acff),  "Zoom"),
        # (Color.fromInteger(0xffa64a),  "Preview"),
    ])),
)


def getNumDrumCols() -> int:
    """Returns the number of columns that the are supported by the controller
    """
    return getContext().getDevice().getDrumPadSize()[1]


def getSelection(i: int) -> PlaylistTrack:
    selection = getFirstPlaylistSelection()
    if i >= getNumDrumCols():
        raise IndexError()
    return PlaylistTrack(selection + i)


class Playlist(WindowIntegration):
    """
    Used to process events directed at the playlist
    """

    def __init__(self, shadow: DeviceShadow) -> None:
        shadow.bindMatches(JogWheel, self.jogWheel)
        shadow.bindMatches(
            ToolSelector,
            self.eSelectTool,
            args_generator=...,
            target_num=len(TOOL_COLORS),
        )\
            .colorize(TOOL_COLORS)\
            .annotate(TOOL_NAMES)

        MuteSoloStrategy(shadow, getSelection)

        # Navigation mappings
        # FIXME: This is super yucky, come up with a better system for it
        # at some point
        try:
            next = shadow.getControlMatches(
                DirectionNext, False, 1, raise_on_zero=True)[0]
            prev = shadow.getControlMatches(
                DirectionPrevious, False, 1, raise_on_zero=True)[0]
            prev_next = (prev, next)
        except ValueError:
            prev_next = None
        try:
            left = shadow.getControlMatches(
                DirectionLeft, False, 1, raise_on_zero=True)[0]
            right = shadow.getControlMatches(
                DirectionRight, False, 1, raise_on_zero=True)[0]
            left_right = (left, right)
        except ValueError:
            left_right = None
        try:
            up = shadow.getControlMatches(
                DirectionUp, False, 1, raise_on_zero=True)[0]
            down = shadow.getControlMatches(
                DirectionDown, False, 1, raise_on_zero=True)[0]
            up_down = (up, down)
        except ValueError:
            up_down = None

        # Pattern selection
        if prev_next is not None:
            shadow.bindControl(prev_next[0], self.ePrevPattern)
            shadow.bindControl(prev_next[1], self.eNextPattern)
            prev_next = None
        elif up_down is not None:
            shadow.bindControl(up_down[0], self.ePrevPattern)
            shadow.bindControl(up_down[1], self.eNextPattern)
            up_down = None
        elif left_right is not None:
            shadow.bindControl(left_right[0], self.ePrevPattern)
            shadow.bindControl(left_right[1], self.eNextPattern)
            left_right = None

        # Marker selection
        if left_right is not None:
            shadow.bindControl(left_right[0], self.ePrevMarker)
            shadow.bindControl(left_right[1], self.eNextMarker)
            left_right = None
        elif up_down is not None:
            shadow.bindControl(up_down[0], self.ePrevMarker)
            shadow.bindControl(up_down[1], self.eNextMarker)
            up_down = None

        # Track selection
        if up_down is not None:
            shadow.bindControl(up_down[0], self.ePrevTrack)
            shadow.bindControl(up_down[1], self.eNextTrack)
            up_down = None

        super().__init__(shadow)

    @classmethod
    def getWindowId(cls) -> WindowIndex:
        return WindowIndex.PLAYLIST

    @classmethod
    def create(cls, shadow: DeviceShadow) -> 'WindowIntegration':
        return cls(shadow)

    def jogWheel(
        self,
        control: ControlShadowEvent,
        index: FlIndex,
        *args: Any
    ) -> bool:
        if control.value == consts.JOG_NEXT:
            increment = 1
        elif control.value == consts.JOG_PREV:
            increment = -1
        elif control.value == consts.JOG_SELECT:
            ui.enter()
            return True
        else:
            return True

        if isinstance(control.getControl(), MoveJogWheel):
            # Scroll through tracks
            track = getFirstPlaylistSelection() + increment
            if track <= 0:
                track = 1
            elif track >= 500:
                track = playlist.trackCount() - 1
            playlist.deselectAll()
            playlist.selectTrack(track)
            ui.scrollWindow(WindowIndex.PLAYLIST.index, track)
        elif isinstance(control.getControl(), StandardJogWheel):
            # Need to account for ticks being zero-indexed and bars being
            # 1-indexed
            bar = int(transport.getSongPos(3)) + increment - 1
            ui.scrollWindow(WindowIndex.PLAYLIST.index, bar, 1)
            # TODO: Make this work with time signature markers
            transport.setSongPos(bar * general.getRecPPB(), 2)
        return True

    @filterButtonLift()
    def eSelectTool(
        self,
        control: ControlShadowEvent,
        window,
        idx: int,
    ) -> bool:
        # HACK: This uses keyboard shortcuts which are extremely unreliable
        if idx < len(TOOL_COLORS):
            # If we're already in a menu, close it
            if ui.isInPopupMenu():
                ui.closeActivePopupMenu()
            # Open menu
            transport.globalTransport(90, 1)
            # Move down until we reach the required tool (including initial
            # downwards navigation)
            for _ in range(idx + 1):
                ui.down()
            # Select it
            ui.enter()
        return True

    def jumpPattern(self, delta: int):
        if patterns.patternCount() == 0:
            return
        pat = patterns.patternNumber()
        new_pat = (pat + delta - 1) % patterns.patternCount() + 1
        patterns.jumpToPattern(new_pat)

    @filterButtonLift()
    def eNextPattern(
        self,
        *args,
    ) -> bool:
        self.jumpPattern(1)
        return True

    @filterButtonLift()
    def ePrevPattern(
        self,
        *args,
    ) -> bool:
        self.jumpPattern(-1)
        return True

    def jumpTracks(self, delta: int):
        for i in range(1, playlist.trackCount() + 1):
            if playlist.isTrackSelected(i):
                break
        else:
            playlist.selectTrack(1)
            return
        # Apply the delta
        i += delta
        i %= playlist.trackCount()
        if i == 0:
            # Wrap around
            # TODO: When API supports, wrap around to the last track that's in
            # use
            i = playlist.trackCount()
        playlist.deselectAll()
        playlist.selectTrack(i)

    @filterButtonLift()
    def eNextTrack(
        self,
        *args,
    ) -> bool:
        self.jumpTracks(1)
        return True

    @filterButtonLift()
    def ePrevTrack(
        self,
        *args,
    ) -> bool:
        self.jumpTracks(-1)
        return True

    @filterButtonLift()
    def eNextMarker(
        self,
        *args,
    ) -> bool:
        arrangement.jumpToMarker(1, False)
        return True

    @filterButtonLift()
    def ePrevMarker(
        self,
        *args,
    ) -> bool:
        arrangement.jumpToMarker(-1, False)
        return True


ExtensionManager.windows.register(Playlist)
