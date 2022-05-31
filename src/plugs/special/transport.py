"""
plugs > special > transport

Contains the definition for the transport plugin, which provides mappings for
transport controls such as play and stop.

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""

import transport
import ui

from typing import Any

from common.extension_manager import ExtensionManager
from common.types import Color
from control_surfaces import (
    ControlShadowEvent,
    NullEvent,
    PlayButton,
    StopButton,
    FastForwardButton,
    RewindButton,
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
from control_surfaces.control_shadow import ControlShadow
from devices import DeviceShadow
from plugs import SpecialPlugin
from plugs.event_filters import filterButtonLift
from plugs.mapping_strategies import DirectionStrategy, JogStrategy

# Constants
FAST_FORWARDING = 1
REWINDING = -1
NORMAL_SPEED = 0

# Color definitions

OFF = Color()
GRAY = Color.fromInteger(0x606060, 0.3, False)
ON = Color.fromInteger(0xFFFFFF, 1.0, True)

SONG_COLOR = Color.fromInteger(0x45A147, 0.6, True)
PAT_COLOR = Color.fromInteger(0xF78F41, 0.6, True)
REC_COLOR = Color.fromInteger(0xAF0000, 1.0, True)
STOP_COLOR = Color.fromInteger(0xB9413E, 1.0, True)

BEAT_SONG_COLOR = Color.fromInteger(0x00A0F0, 1.0, True)
BEAT_PAT_COLOR = Color.fromInteger(0xA43A37, 1.0, True)


def getPatSongCol() -> Color:
    if transport.getLoopMode():
        return SONG_COLOR
    else:
        return PAT_COLOR


def getBeatColor(off: Color) -> Color:
    beat = transport.getHWBeatLEDState()
    # print(beat)
    # odd number -> off beat
    if beat % 2 == 1:
        return off
    # 0 -> new bar
    elif beat == 0:
        if transport.getLoopMode():
            return BEAT_SONG_COLOR
        else:
            return BEAT_PAT_COLOR
    # -> new beat
    else:
        return getPatSongCol()


class Transport(SpecialPlugin):
    """
    The transport plugin manages basic transport commands, such as play/pause
    commands and navigation commands.
    """

    def __init__(self, shadow: DeviceShadow) -> None:
        shadow.setMinimal(True)
        shadow.bindMatches(NullEvent, self.nullEvent)
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
        shadow.bindMatches(NavigationButton, self.navButtons)
        # Whether we're fast forwarding or rewinding
        self._playback_ff_rw = 0
        super().__init__(shadow, [
            DirectionStrategy(),
            JogStrategy(),
        ])

    @classmethod
    def create(cls, shadow: DeviceShadow) -> 'SpecialPlugin':
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

    @filterButtonLift()
    def navButtons(self, control: ControlShadowEvent, *args: Any) -> bool:
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

    def fastForward(self, control: ControlShadowEvent, *args: Any,) -> bool:
        val = control.value != 0
        transport.fastForward(2 if val else 0)
        self._playback_ff_rw = FAST_FORWARDING if val else 0
        return True

    def rewind(self, control: ControlShadowEvent, *args: Any,) -> bool:
        val = control.value != 0
        transport.rewind(2 if val else 0)
        self._playback_ff_rw = REWINDING if val else 0
        return True

    def tickPlay(self, control: ControlShadow, *args):
        if transport.isPlaying():
            control.color = getBeatColor(off=GRAY)
        else:
            control.color = GRAY

    def tickStop(self, control: ControlShadow, *args):
        if transport.isPlaying():
            control.color = GRAY
        else:
            control.color = STOP_COLOR

    def tickLoop(self, control: ControlShadow, *args):
        """Color loop mode button"""
        control.color = getPatSongCol()

    def tickRec(self, control: ControlShadow, *args):
        """Color record button"""
        control.color = REC_COLOR if transport.isRecording() else GRAY

    def tickMetro(self, control: ControlShadow, *args):
        """Color metronome button"""
        if ui.isMetronomeEnabled():
            if transport.isPlaying():
                control.color = getBeatColor(GRAY)
            else:
                control.color = ON
        else:
            control.color = GRAY

    def tickHint(self, control: ControlShadow, *args):
        """Set hint message"""
        control.annotation = ui.getHintMsg()

    def tickFf(self, control: ControlShadow, *args):
        """Fast forward"""
        if self._playback_ff_rw == FAST_FORWARDING:
            control.color = ON
        else:
            control.color = GRAY

    def tickRw(self, control: ControlShadow, *args):
        """Rewind"""
        if self._playback_ff_rw == REWINDING:
            control.color = ON
        else:
            control.color = GRAY


ExtensionManager.special.register(Transport)
