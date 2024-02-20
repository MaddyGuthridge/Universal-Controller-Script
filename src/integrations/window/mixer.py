"""
integrations > window > mixer

Integration for FL Studio's mixer

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""
from typing import Any
import ui
import mixer
from common import getContext
from common.tracks.mixer_track import MixerTrack
from common.types import Color
from common.extension_manager import ExtensionManager
from common.plug_indexes import WindowIndex
from common.util.api_fixes import (
    getSelectedDockMixerTracks,
    getMixerDockSides,
    getSelectedMixerTracks,
)
from common.util.snap import snap
from common.util.misc import clamp
from control_surfaces import consts
from control_surfaces import ControlShadowEvent
from control_surfaces import (
    ControlSurface,
    JogWheel,
    StandardJogWheel,
    Fader,
    Knob,
    Encoder,
    MasterFader,
    MasterKnob,
    ArmButton,
    SelectButton,
    ControlSwitchButton,
)
from devices import DeviceShadow
from integrations.event_filters import filterButtonLift
from integrations.mapping_strategies import MuteSoloStrategy
from integrations import WindowIntegration

INDEX = WindowIndex.MIXER
COLOR_DISABLED = Color.fromGrayscale(0.3, False)
COLOR_ARMED = Color.fromInteger(0xAF0000, 1.0, True)


def snapVolume(value: float, control: ControlSurface) -> float:
    """
    Return the snapped value of a fader, so that getting volumes to 100% is
    easier

    ### Args:
    * `value` (`float`): value to snap
    * `force_range` (`bool`): whether to force the full ranger (for encoders)

    ### Returns:
    * `float`: snapped value
    """
    if (
        getContext().settings.get("plugins.mixer.allow_extended_volume")
        or isinstance(control, Encoder)
    ):
        return snap(value, 0.8)
    else:
        return value * 0.8


def unsnapVolume(value: float, control: ControlSurface) -> float:
    """
    Convert a mixer track volume to a fader value
    """
    if isinstance(control, Encoder):
        return value
    else:
        return clamp(value / 0.8, 0, 1)


def snapPan(value: float) -> float:
    return snap(value, 0.5) * 2 - 1


def unsnapPan(value: float) -> float:
    return (value + 1) / 2


class Mixer(WindowIntegration):
    """
    Used to process events directed
    """

    def __init__(self, shadow: DeviceShadow) -> None:

        # Bind jog wheel
        self._jog = shadow.bindMatches(
            JogWheel, self.jogWheel, raise_on_failure=False)

        # Bind main controls
        self._faders = shadow.bindMatches(
            Fader,
            self.fader,
        )
        self._knobs = shadow.bindMatches(
            Knob,
            self.knob,
        )
        self._fader_master = shadow.bindMatch(
            MasterFader,
            self.masterFader,
        )
        self._knob_master = shadow.bindMatch(
            MasterKnob,
            self.masterKnob,
        )
        self._arms = shadow.bindMatches(
            ArmButton,
            self.arm,
        )
        self._selects = shadow.bindMatches(
            SelectButton,
            self.select,
        )
        self._control_switch = shadow.bindMatch(
            ControlSwitchButton,
            self.controlSwitch,
        ).annotate("Show selected").colorize(Color.fromGrayscale(0.5))

        # Create bindings for mute, solo and generic buttons
        MuteSoloStrategy(shadow, lambda i: self._selection[i])

        # TODO: Bind master controls

        # List of mapped channels
        self._selection: list[MixerTrack] = []
        # List of mapped channels, respecting the dock side
        self._selection_docked: list[MixerTrack] = []
        # Dock side that we're mapping to
        self._dock_side = 1
        # Length of mapped channels
        self._len = max(map(len, [self._faders, self._knobs]))
        super().__init__(shadow)

    @classmethod
    def getWindowId(cls) -> WindowIndex:
        return INDEX

    @classmethod
    def create(cls, shadow: DeviceShadow) -> 'WindowIntegration':
        return cls(shadow)

    def updateSelected(self):
        """
        Update the list of selected tracks
        """
        dock_side = mixer.getTrackDockSide(mixer.trackNumber())
        selected = list(map(
            MixerTrack,
            getSelectedDockMixerTracks()[dock_side],
        ))
        dock_sides = list(map(
            MixerTrack,
            getMixerDockSides()[dock_side],
        ))

        if len(selected) == 0:
            # No selection, we need to generate one
            if not len(self._selection):
                selected = [dock_sides[0]]
            else:
                return

        assert len(dock_sides), "No elements on the dock side"

        # Find index of first selected track on that docking side
        for index, track_index in enumerate(dock_sides):
            if track_index == selected[0]:
                break

        # Calculate first track that should be selected
        if index + self._len >= len(dock_sides):
            first = max(len(dock_sides) - self._len, 0)
        else:
            first = index
        # And last track that should be selected
        last = min(len(dock_sides), first + self._len)

        # If we need to change selection
        if (
            dock_side != self._dock_side
            or len(self._selection) == 0
            or MixerTrack(first) < self._selection_docked[0]
            or MixerTrack(index) > self._selection_docked[-1]
        ):
            self._selection = [dock_sides[i] for i in range(first, last)]
            self._selection_docked = list(map(MixerTrack, range(first, last)))
            self._dock_side = dock_side
            self.displayRect()

    def displayRect(self):
        """
        Display the UI rectangle
        """
        first = self._selection_docked[0]
        ui.miDisplayDockRect(
            first.index + 1,
            len(self._selection),
            self._dock_side,
            2000,
        )

    def tick(self, *args):
        self.updateSelected()
        self.updateColors()

    def jogWheel(
        self,
        control: ControlShadowEvent,
        *args: Any
    ) -> bool:
        selected = getSelectedMixerTracks()
        if len(selected) == 0:
            selected = [0]
        # Calculate increment
        if control.value == consts.JOG_NEXT:
            dest = selected[-1] + 1
        elif control.value == consts.JOG_PREV:
            dest = selected[0] - 1
        elif control.value == consts.JOG_SELECT:
            # When we push the encoder, toggle the selected tracks' mutes
            for i in selected:
                mixer.muteTrack(i)
            return True
        else:
            return True

        # If it's a standard jog wheel, deselect the current selection
        if isinstance(control.getControl(), StandardJogWheel):
            mixer.deselectAll()

        if dest < 0:
            dest = mixer.trackCount() - 2
        if dest >= mixer.trackCount() - 1:
            dest = 0
        MixerTrack(dest).selected = True

        return True

    def fader(
        self,
        control: ControlShadowEvent,
        *args: Any
    ) -> bool:
        """Faders -> volume"""
        try:
            track = self._selection[control.getControl().coordinate[1]]
        except IndexError:
            return False
        track.volume = snapVolume(control.value, control.getControl())
        return True

    def masterFader(
        self,
        control: ControlShadowEvent,
        *args: Any
    ) -> bool:
        if len(self._faders) == 0:
            track = MixerTrack(mixer.trackNumber())
        else:
            track = MixerTrack(mixer.trackNumber())
        track.volume = snapVolume(control.value, control.getControl())
        return True

    def updateColors(self):
        # Master tracks
        idx = mixer.trackNumber()
        c = Color.fromInteger(mixer.getTrackColor(idx))
        name = mixer.getTrackName(idx)
        self._knob_master.color = c
        self._knob_master.annotation = name
        self._fader_master.color = c
        self._fader_master.annotation = name
        # For each selected track
        for fader_num, track in enumerate(self._selection):
            # Only apply to controls that are within range
            if len(self._faders) > fader_num:
                self._faders[fader_num].color = track.color
                self._faders[fader_num].annotation = track.name
                self._faders[fader_num].value = unsnapVolume(
                    track.volume, self._faders[fader_num].getControl())
            if len(self._knobs) > fader_num:
                self._knobs[fader_num].color = track.color
                self._knobs[fader_num].annotation = track.name
                self._knobs[fader_num].value = unsnapPan(track.pan)
            # Select buttons
            if len(self._selects) > fader_num:
                if track.selected:
                    self._selects[fader_num].color = track.color
                else:
                    self._selects[fader_num].color = COLOR_DISABLED
            # Arm buttons
            if len(self._arms) > fader_num:
                if track.armed:
                    self._arms[fader_num].color = COLOR_ARMED
                else:
                    self._arms[fader_num].color = COLOR_DISABLED

    def knob(
        self,
        control: ControlShadowEvent,
        *args: Any
    ) -> bool:
        """Knobs -> panning"""
        index = self._selection[control.getControl().coordinate[1]]
        index.pan = snapPan(control.value)
        return True

    def masterKnob(
        self,
        control: ControlShadowEvent,
        *args: Any
    ) -> bool:
        if len(self._knobs) == 0:
            track = MixerTrack(mixer.trackNumber())
        else:
            track = MixerTrack(0)
        track.pan = snapPan(control.value)
        return True

    @filterButtonLift()
    def arm(
        self,
        control: ControlShadowEvent,
        index: WindowIndex,
        *args: Any
    ) -> bool:
        """Arm track"""
        track = self._selection[control.getControl().coordinate[1]]
        mixer.armTrack(track.index)
        return True

    @filterButtonLift()
    def select(
        self,
        control: ControlShadowEvent,
        index: WindowIndex,
        *args: Any
    ) -> bool:
        """Select track"""
        track = self._selection[control.getControl().coordinate[1]]
        track.selectedToggle()
        return True

    @filterButtonLift()
    def controlSwitch(
        self,
        *args: Any
    ) -> bool:
        self.displayRect()
        return True


ExtensionManager.windows.register(Mixer)
