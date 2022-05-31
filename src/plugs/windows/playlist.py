"""
plugs > windows > playlist

Plugin for interacting with FL Studio's playlist

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""
from typing import Any
import ui
import playlist
import transport
import general
from common import getContext
from common.extension_manager import ExtensionManager
from common.plug_indexes import UnsafeIndex
from common.util.api_fixes import getFirstPlaylistSelection
from control_surfaces import consts
from control_surfaces import ControlShadowEvent
from control_surfaces import MoveJogWheel, StandardJogWheel, JogWheel
from devices import DeviceShadow
from plugs import WindowPlugin
from plugs.mapping_strategies import MuteSoloStrategy

INDEX = 2


def getNumDrumCols() -> int:
    """Returns the number of columns that the are supported by the controller
    """
    return getContext().getDevice().getDrumPadSize()[1]


def getSelection(i: int):
    selection = getFirstPlaylistSelection()
    if i >= getNumDrumCols():
        raise IndexError()
    return selection + i


class Playlist(WindowPlugin):
    """
    Used to process events directed at the playlist
    """

    def __init__(self, shadow: DeviceShadow) -> None:
        shadow.bindMatches(JogWheel, self.jogWheel)
        mute_solo = MuteSoloStrategy(
            getSelection,
            playlist.muteTrack,
            playlist.isTrackMuted,
            playlist.soloTrack,
            playlist.isTrackSolo,
            playlist.getTrackColor,
        )
        super().__init__(shadow, [mute_solo])

    @classmethod
    def getWindowId(cls) -> int:
        return INDEX

    @classmethod
    def create(cls, shadow: DeviceShadow) -> 'WindowPlugin':
        return cls(shadow)

    def jogWheel(
        self,
        control: ControlShadowEvent,
        index: UnsafeIndex,
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
            ui.scrollWindow(INDEX, track)
        elif isinstance(control.getControl(), StandardJogWheel):
            # Need to account for ticks being zero-indexed and bars being
            # 1-indexed
            bar = int(transport.getSongPos(3)) + increment - 1
            ui.scrollWindow(INDEX, bar, 1)
            # TODO: Make this work with time signature markers
            transport.setSongPos(bar * general.getRecPPB(), 2)
        return True


ExtensionManager.windows.register(Playlist)
