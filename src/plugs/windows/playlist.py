
from typing import Any
import ui
import playlist
import transport
import general
from common.extension_manager import ExtensionManager
from common.util.api_fixes import UnsafeIndex, getSelectedPlaylistTrack
from control_surfaces import consts
from control_surfaces import ControlShadowEvent
from control_surfaces import MoveJogWheel, StandardJogWheel, JogWheel
from devices import DeviceShadow
from plugs import WindowPlugin

INDEX = 2


class Playlist(WindowPlugin):
    """
    Used to process events directed at the playlist
    """

    def __init__(self, shadow: DeviceShadow) -> None:
        shadow.bindMatches(JogWheel, self.jogWheel)
        super().__init__(shadow, [])

    @staticmethod
    def getWindowId() -> int:
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
        if control.value == consts.ENCODER_NEXT:
            increment = 1
        elif control.value == consts.ENCODER_PREV:
            increment = -1
        elif control.value == consts.ENCODER_SELECT:
            ui.enter()
            return True
        else:
            return True

        if isinstance(control.getControl(), MoveJogWheel):
            # Scroll through tracks
            track = getSelectedPlaylistTrack() + increment
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
