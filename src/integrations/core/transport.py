"""
integrations > core > transport

Contains the definition for the transport integration, which provides mappings
for transport controls such as play and stop.

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""

import arrangement
import transport
import ui

from typing import Any
from common.context_manager import getContext

from common.extension_manager import ExtensionManager
from common.types import Color
from control_surfaces import (
    ControlShadowEvent,
    NullControl,
    PlayButton,
    StopButton,
    FastForwardButton,
    RewindButton,
    RecordButton,
    LoopButton,
    MetronomeButton,
    HintMsg,
)
from control_surfaces.control_shadow import ControlShadow
from devices import DeviceShadow
from integrations import CoreIntegration
from integrations.event_filters import filterButtonLift

# Constants
FAST_FORWARDING = 1
REWINDING = -1
NORMAL_SPEED = 0


def getPatSongCol() -> Color:
    if transport.getLoopMode():
        return Color.FL_SONG
    else:
        return Color.FL_PATTERN


def getBeatColor(off: Color) -> Color:
    beat = transport.getHWBeatLEDState()
    # print(beat)
    # odd number -> off beat
    if beat % 2 == 1:
        return off
    # 0 -> new bar
    elif beat == 0:
        if transport.getLoopMode():
            return Color.FL_SONG_ALT
        else:
            return Color.FL_PATTERN_ALT
    # -> new beat
    else:
        return getPatSongCol()


class Transport(CoreIntegration):
    """
    The transport plugin manages basic transport commands, such as play/pause
    commands and navigation commands.
    """

    def __init__(self, shadow: DeviceShadow) -> None:
        shadow.setMinimal(True)
        shadow.bindMatches(NullControl, self.nullEvent)
        shadow.bindMatch(PlayButton, self.playButton, self.tickPlay)
        # Need to be able to determine whether the stop button is assigned
        self._stop = shadow.bindMatch(StopButton, self.stopButton,
                                      self.tickStop)
        shadow.bindMatch(RecordButton, self.recButton, self.tickRec)
        shadow.bindMatch(LoopButton, self.loopButton, self.tickLoop)
        shadow.bindMatch(MetronomeButton, self.metroButton, self.tickMetro)
        shadow.bindMatch(HintMsg, self.nullEvent, self.tickHint)
        shadow.bindMatch(FastForwardButton, self.fastForward, self.tickFf)
        shadow.bindMatch(RewindButton, self.rewind, self.tickRw)
        # Whether we're fast forwarding or rewinding
        self._playback_ff_rw = 0
        super().__init__(shadow)

    @classmethod
    def create(cls, shadow: DeviceShadow) -> 'CoreIntegration':
        return cls(shadow)

    @classmethod
    def shouldBeActive(cls) -> bool:
        return True

    @filterButtonLift()
    def playButton(self, *args: Any) -> bool:
        # If there's no stop button, this should behave like a stop button
        # when playing
        if not self._stop.isBound() and transport.isPlaying():
            transport.stop()
        else:
            transport.start()
        return True

    @filterButtonLift()
    def stopButton(self, *args: Any) -> bool:
        transport.stop()
        return True

    @filterButtonLift()
    def recButton(self, *args: Any) -> bool:
        transport.record()
        return True

    @filterButtonLift()
    def loopButton(self, *args: Any) -> bool:
        transport.setLoopMode()
        return True

    @filterButtonLift()
    def metroButton(self, *args: Any) -> bool:
        transport.globalTransport(110, 1)
        return True

    def nullEvent(self, *args: Any) -> bool:
        """Handle NullEvents for which no action should be taken
        """
        return True

    def fastForward(self, control: ControlShadowEvent, *args: Any,) -> bool:
        val = control.value != 0
        transport.fastForward(2 if val else 0)
        self._playback_ff_rw = FAST_FORWARDING if val else 0
        # If it was a short press, jump between markers
        if (
            not val
            and control.press_length
            < getContext().settings.get("controls.short_press_time")
        ):
            arrangement.jumpToMarker(1, False)

        return True

    def rewind(self, control: ControlShadowEvent, *args: Any,) -> bool:
        val = control.value != 0
        transport.rewind(2 if val else 0)
        self._playback_ff_rw = REWINDING if val else 0
        # If it was a short press, jump between markers
        if (
            not val
            and control.press_length
            < getContext().settings.get("controls.short_press_time")
        ):
            arrangement.jumpToMarker(-1, False)
        return True

    def tickPlay(self, control: ControlShadow, *args):
        if transport.isPlaying():
            control.color = getBeatColor(off=Color.DISABLED)
        else:
            control.color = Color.DISABLED

    def tickStop(self, control: ControlShadow, *args):
        if transport.isPlaying():
            control.color = Color.DISABLED
        else:
            control.color = Color.FL_STOP

    def tickLoop(self, control: ControlShadow, *args):
        """Color loop mode button"""
        control.color = getPatSongCol()

    def tickRec(self, control: ControlShadow, *args):
        """Color record button"""
        control.color = (
            Color.FL_RECORD
            if transport.isRecording()
            else Color.DISABLED
        )

    def tickMetro(self, control: ControlShadow, *args):
        """Color metronome button"""
        if ui.isMetronomeEnabled():
            if transport.isPlaying():
                control.color = getBeatColor(Color.DISABLED)
            else:
                control.color = Color.WHITE
        else:
            control.color = Color.DISABLED

    def tickHint(self, control: ControlShadow, *args):
        """Set hint message"""
        control.annotation = ui.getHintMsg()

    def tickFf(self, control: ControlShadow, *args):
        """Fast forward"""
        if self._playback_ff_rw == FAST_FORWARDING:
            control.color = Color.WHITE
        else:
            control.color = Color.DISABLED

    def tickRw(self, control: ControlShadow, *args):
        """Rewind"""
        if self._playback_ff_rw == REWINDING:
            control.color = Color.WHITE
        else:
            control.color = Color.DISABLED


ExtensionManager.super_special.register(Transport)
