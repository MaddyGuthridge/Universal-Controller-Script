"""
plugs > special > transport

Contains the definition for the transport plugin

Authors:
* Miguel Guthridge [hdsq@outlook.com.au]
"""

import transport
import ui

from typing import Any

from common.extensionmanager import ExtensionManager
from common.types import Color
from common.util.apifixes import UnsafeIndex
from controlsurfaces import (
    ControlShadowEvent,
    NullEvent,
    PlayButton,
    StopButton,
    DirectionNext,
    DirectionPrevious,
    NavigationButton,
    DirectionUp,
    DirectionDown,
    DirectionRight,
    DirectionLeft,
    DirectionSelect,
    RecordButton,
    LoopButton,
    MetronomeButton,
    HintMsg,
)
from devices import DeviceShadow
from plugs import SpecialPlugin
from plugs.eventfilters import filterButtonLift

OFF = Color()
GRAY = Color.fromInteger(0x606060)
ON = Color.fromInteger(0xFFFFFF)

SONG_COLOR = Color.fromInteger(0x45A147)
PAT_COLOR = Color.fromInteger(0xF78F41)
REC_COLOR = Color.fromInteger(0xAF0000)
STOP_COLOR = Color.fromInteger(0xB9413E)

BEAT_SONG_COLOR = Color.fromInteger(0x00A0F0)
BEAT_PAT_COLOR = Color.fromInteger(0xA43A37)


def getPatSongCol() -> Color:
    if transport.getLoopMode():
        return SONG_COLOR
    else:
        return PAT_COLOR


def getBeatColor(off: Color) -> Color:
    beat = transport.getHWBeatLEDState()
    # print(beat)
    if beat % 2 == 1:
        return off
    elif beat == 0:
        if transport.getLoopMode():
            return BEAT_SONG_COLOR
        else:
            return BEAT_PAT_COLOR
    else:
        return getPatSongCol()


class Transport(SpecialPlugin):
    """
    The transport plugin manages basic transport commands, such as play/pause
    commands and navigation commands.
    """

    def __init__(self, shadow: DeviceShadow) -> None:
        shadow.setMinimal(True)
        shadow.bindMatches(NullEvent, self.nullEvent, raise_on_failure=False)
        self._play = shadow.bindMatch(
            PlayButton, self.playButton, raise_on_failure=False
        )
        self._stop = shadow.bindMatch(
            StopButton, self.stopButton, raise_on_failure=False
        )
        self._rec = shadow.bindMatch(
            RecordButton, self.recButton, raise_on_failure=False
        )
        self._loop = shadow.bindMatch(
            LoopButton, self.loopButton, raise_on_failure=False
        )
        self._metronome = shadow.bindMatch(
            MetronomeButton, self.metroButton, raise_on_failure=False
        )
        self._navigation = shadow.bindMatches(
            NavigationButton, self.navigationButtons, raise_on_failure=False
        )
        self._hint = shadow.bindMatch(
            HintMsg, self.nullEvent, raise_on_failure=False
        )
        super().__init__(shadow, [])

    @classmethod
    def create(cls, shadow: DeviceShadow) -> 'SpecialPlugin':
        return cls(shadow)

    @staticmethod
    def shouldBeActive() -> bool:
        return True

    @filterButtonLift
    def playButton(
        self,
        control: ControlShadowEvent,
        index: UnsafeIndex,
        *args: Any
    ) -> bool:
        # If there's no stop button, this should behave like a stop button
        # when playing
        if self._stop is None and transport.isPlaying():
            transport.stop()
        else:
            transport.start()
        return True

    @filterButtonLift
    def stopButton(
        self,
        control: ControlShadowEvent,
        index: UnsafeIndex,
        *args: Any
    ) -> bool:
        transport.stop()
        return True

    @filterButtonLift
    def recButton(
        self,
        control: ControlShadowEvent,
        index: UnsafeIndex,
        *args: Any
    ) -> bool:
        transport.record()
        return True

    @filterButtonLift
    def loopButton(
        self,
        control: ControlShadowEvent,
        index: UnsafeIndex,
        *args: Any
    ) -> bool:
        transport.setLoopMode()
        return True

    @filterButtonLift
    def metroButton(
        self,
        control: ControlShadowEvent,
        index: UnsafeIndex,
        *args: Any
    ) -> bool:
        transport.globalTransport(110, 1)
        return True

    def nullEvent(
        self,
        control: ControlShadowEvent,
        index: UnsafeIndex,
        *args: Any
    ) -> bool:
        """Handle NullEvents for which no action should be taken
        """
        return True

    @filterButtonLift
    def navigationButtons(
        self,
        control: ControlShadowEvent,
        index: UnsafeIndex,
        *args: Any
    ) -> bool:
        c_type = type(control.getControl())
        if c_type == DirectionUp:
            ui.up()
        elif c_type == DirectionDown:
            ui.down()
        elif c_type == DirectionLeft:
            ui.left()
        elif c_type == DirectionRight:
            ui.right()
        elif c_type == DirectionNext:
            ui.next()
        elif c_type == DirectionPrevious:
            ui.previous()
        elif c_type == DirectionSelect:
            ui.enter()
        else:
            return False
        return True

    def tick(self):
        self.tickLoopMode()
        self.tickPlayback()
        self.tickRec()
        self.tickMetro()
        self.tickHint()

    def tickPlayback(self):
        """Color play and stop buttons"""
        # Playback on
        if transport.isPlaying():
            if self._play is not None:
                self._play.color = getBeatColor(off=GRAY)
            if self._stop is not None:
                self._stop.color = STOP_COLOR
        # Playback off
        else:
            if self._play is not None:
                self._play.color = OFF
            if self._stop is not None:
                self._stop.color = GRAY

    def tickLoopMode(self):
        """Color loop mode button"""
        if self._loop is not None:
            self._loop.color = getPatSongCol()

    def tickRec(self):
        """Color record button"""
        if self._rec is not None:
            self._rec.color = REC_COLOR if transport.isRecording() else GRAY

    def tickMetro(self):
        """Color metronome button"""
        if self._metronome is not None:
            if ui.isMetronomeEnabled():
                self._metronome.color = getBeatColor(GRAY)
            else:
                self._metronome.color = OFF

    def tickHint(self):
        """Set hint message"""
        if self._hint is not None:
            self._hint.annotation = ui.getHintMsg()


ExtensionManager.registerSpecialPlugin(Transport)
