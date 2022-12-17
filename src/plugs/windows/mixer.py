"""
plugs > windows > mixer

Plugin for FL Studio's mixer

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""
from typing import Any
import ui
import mixer
from common import getContext
from common.types import Color
from common.extension_manager import ExtensionManager
from common.plug_indexes import (UnsafeIndex)
from common.util.api_fixes import getSelectedMixerTracks
from common.util.snap import snap
from control_surfaces import consts
from control_surfaces import ControlShadowEvent
from control_surfaces import (
    JogWheel,
    StandardJogWheel,
    Fader,
    Knob,
    MasterFader,
    MasterKnob,
    ArmButton,
    SelectButton,
    ControlSwitchButton,
)
from devices import DeviceShadow
from plugs.event_filters import filterButtonLift
from plugs.mapping_strategies import MuteSoloStrategy
from plugs import WindowPlugin

INDEX = 0
COLOR_DISABLED = Color.fromGrayscale(0.3, False)
COLOR_ARMED = Color.fromInteger(0xAF0000, 1.0, True)


def snapFaders(value: float) -> float:
    """
    Return the snapped value of a fader, so that getting volumes to 100% is
    easier

    ### Args:
    * `value` (`float`): value to snap

    ### Returns:
    * `float`: snapped value
    """
    if getContext().settings.get("plugins.mixer.allow_extended_volume"):
        return snap(value, 0.8)
    else:
        return value * 0.8


def snapKnobs(value: float) -> float:
    return snap(value, 0.5) * 2 - 1


class Mixer(WindowPlugin):
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
        mutes_solos = MuteSoloStrategy(
            lambda i: self._selection[i],
            mixer.muteTrack,
            mixer.isTrackMuted,
            mixer.soloTrack,
            mixer.isTrackSolo,
            mixer.getTrackColor,
        )

        # TODO: Bind master controls

        # List of mapped channels
        self._selection: list[int] = []
        # Length of mapped channels
        self._len = max(map(len, [self._faders, self._knobs]))
        super().__init__(shadow, [mutes_solos])

    @classmethod
    def getWindowId(cls) -> int:
        return INDEX

    @classmethod
    def create(cls, shadow: DeviceShadow) -> 'WindowPlugin':
        return cls(shadow)

    def updateSelected(self):
        """
        Update the list of selected tracks

        KNOWN ISSUES:
        * This doesn't respect docking sides: as soon as the mixer rectangle
          can be displayed in a way that respects them, change this
        """
        selected = getSelectedMixerTracks()

        if len(selected) == 0:
            # No selection, we need to generate one
            if not len(self._selection):
                selected = [1]
            else:
                return

        first = selected[0]
        last = first
        for i in selected:
            if i - first < self._len:
                last = i

        if first + self._len >= mixer.trackCount() - 1:
            first = (mixer.trackCount() - 1) - self._len

        # If we need to change selection
        if (
            len(self._selection) == 0
            or first < self._selection[0]
            or last > self._selection[0] + self._len - 1
        ):
            self._selection = list(range(first, first+self._len))
            self.displayRect()

    def displayRect(self):
        """
        Display the UI rectangle
        """
        first = self._selection[0]
        ui.miDisplayRect(first, first+self._len-1, 2000)

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
        mixer.selectTrack(dest)

        return True

    def fader(
        self,
        control: ControlShadowEvent,
        *args: Any
    ) -> bool:
        """Faders -> volume"""
        index = self._selection[control.getControl().coordinate[1]]
        mixer.setTrackVolume(index, snapFaders(control.value))
        return True

    def masterFader(
        self,
        control: ControlShadowEvent,
        *args: Any
    ) -> bool:
        track = mixer.trackNumber()
        mixer.setTrackVolume(track, snapFaders(control.value))
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
        for n, i in enumerate(self._selection):
            c = Color.fromInteger(mixer.getTrackColor(i))
            name = mixer.getTrackName(i)
            # Only apply to controls that are within range
            if len(self._faders) > n:
                self._faders[n].color = c
                self._faders[n].annotation = name
            if len(self._knobs) > n:
                self._knobs[n].color = c
                self._knobs[n].annotation = name
            # Select buttons
            if len(self._selects) > n:
                if mixer.isTrackSelected(i):
                    self._selects[n].color = c
                else:
                    self._selects[n].color = COLOR_DISABLED
            # Arm buttons
            if len(self._arms) > n:
                if mixer.isTrackArmed(i):
                    self._arms[n].color = COLOR_ARMED
                else:
                    self._arms[n].color = COLOR_DISABLED

    def knob(
        self,
        control: ControlShadowEvent,
        *args: Any
    ) -> bool:
        """Knobs -> panning"""
        index = self._selection[control.getControl().coordinate[1]]
        mixer.setTrackPan(index, snapKnobs(control.value))
        return True

    def masterKnob(
        self,
        control: ControlShadowEvent,
        *args: Any
    ) -> bool:
        track = mixer.trackNumber()
        mixer.setTrackPan(track, snapKnobs(control.value))
        return True

    @filterButtonLift()
    def arm(
        self,
        control: ControlShadowEvent,
        index: UnsafeIndex,
        *args: Any
    ) -> bool:
        """Arm track"""
        index = self._selection[control.getControl().coordinate[1]]
        mixer.armTrack(index)
        return True

    @filterButtonLift()
    def select(
        self,
        control: ControlShadowEvent,
        index: UnsafeIndex,
        *args: Any
    ) -> bool:
        """Select track"""
        index = self._selection[control.getControl().coordinate[1]]
        mixer.selectTrack(index)
        return True

    @filterButtonLift()
    def controlSwitch(
        self,
        *args: Any
    ) -> bool:
        self.displayRect()
        return True


ExtensionManager.windows.register(Mixer)
