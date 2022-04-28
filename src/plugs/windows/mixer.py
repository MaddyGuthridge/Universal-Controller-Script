
from typing import Any
import ui
import mixer
from common import getContext
from common.types import Color
from common.extensionmanager import ExtensionManager
from common.util.apifixes import (
    UnsafeIndex,
    getSelectedMixerTracks,
)
from common.util.snap import snap
from controlsurfaces import consts
from controlsurfaces import ControlShadowEvent
from controlsurfaces import (  # noqa: F401
    JogWheel,
    StandardJogWheel,
    Fader,
    Knob,
    MasterFader,
    MasterKnob,
    GenericFaderButton,
    MuteButton,
    SoloButton,
    ArmButton,
    SelectButton,
)
from devices import DeviceShadow
from plugs.eventfilters import filterButtonLift
from plugs import WindowPlugin

INDEX = 0


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
        super().__init__(shadow, [])

        # Bind jog wheel
        self._jog = shadow.bindMatches(
            JogWheel, self.jogWheel, raise_on_failure=False)

        # Bind main controls
        self._faders = shadow.bindMatches(
            Fader,
            self.fader,
            raise_on_failure=False,
            allow_substitution=True,
        )
        self._knobs = shadow.bindMatches(
            Knob,
            self.knob,
            raise_on_failure=False,
            allow_substitution=True,
        )
        self._buttons = shadow.bindMatches(
            GenericFaderButton,
            self.button,
            raise_on_failure=False
        )
        self._mutes = shadow.bindMatches(
            MuteButton,
            self.mute,
            raise_on_failure=False
        )
        self._solos = shadow.bindMatches(
            SoloButton,
            self.solo,
            raise_on_failure=False
        )
        self._arms = shadow.bindMatches(
            ArmButton,
            self.arm,
            raise_on_failure=False
        )
        self._selects = shadow.bindMatches(
            SelectButton,
            self.select,
            raise_on_failure=False
        )

        # TODO: Bind master controls

        # List of mapped channels
        self._selection: list[int] = []
        # Length of mapped channels
        self._len = max(map(len, [self._faders, self._knobs]))

    @staticmethod
    def getWindowId() -> int:
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
            ui.miDisplayRect(first, first+self._len-1, 2000)

    def tick(self):
        self.updateSelected()

    def jogWheel(
        self,
        control: ControlShadowEvent,
        index: UnsafeIndex,
        *args: Any
    ) -> bool:
        selected = getSelectedMixerTracks()
        if len(selected) == 0:
            selected = [0]
        # Calculate increment
        if control.value == consts.ENCODER_NEXT:
            dest = selected[-1] + 1
        elif control.value == consts.ENCODER_PREV:
            dest = selected[0] - 1
        elif control.value == consts.ENCODER_SELECT:
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
        index: UnsafeIndex,
        *args: Any
    ) -> bool:
        """Faders -> volume"""
        index = self._selection[control.getControl().coordinate[1]]

        mixer.setTrackVolume(index, snapFaders(control.value))

        return True

    def updateColors(self):
        # For each selected track
        for n, i in enumerate(self._selection):
            c = Color.fromInteger(mixer.getTrackColor(i))
            # Only apply to controls that are within range
            if len(self._faders) > n:
                self._faders[n].color = c
            if len(self._knobs) > n:
                self._knobs[n].color = c
            # Generic fader buttons
            if len(self._buttons) > n:
                if mixer.isTrackEnabled(i):
                    self._buttons[n].color = c
                else:
                    self._buttons[n].color = c.fadeBlack()
            # Mute buttons
            if len(self._mutes) > n:
                if mixer.isTrackMuted(i):
                    self._mutes[n].color = c
                else:
                    self._mutes[n].color = c.fadeBlack()
            # Solo buttons
            if len(self._solos) > n:
                if mixer.isTrackSolo(i):
                    self._solos[n].color = c
                else:
                    self._solos[n].color = c.fadeBlack()
            # Select buttons
            if len(self._selects) > n:
                if mixer.isTrackMuted(i):
                    self._selects[n].color = c
                else:
                    self._selects[n].color = c.fadeBlack()

    def knob(
        self,
        control: ControlShadowEvent,
        index: UnsafeIndex,
        *args: Any
    ) -> bool:
        """Knobs -> panning"""
        index = self._selection[control.getControl().coordinate[1]]
        mixer.setTrackPan(index, snapKnobs(control.value))

        return True

    @filterButtonLift
    def mute(
        self,
        control: ControlShadowEvent,
        index: UnsafeIndex,
        *args: Any
    ) -> bool:
        """Mute track"""
        index = self._selection[control.getControl().coordinate[1]]
        mixer.muteTrack(index)
        return True

    @filterButtonLift
    def solo(
        self,
        control: ControlShadowEvent,
        index: UnsafeIndex,
        *args: Any
    ) -> bool:
        """Solo track"""
        index = self._selection[control.getControl().coordinate[1]]
        mixer.soloTrack(index)
        return True

    @filterButtonLift
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

    @filterButtonLift
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

    @filterButtonLift
    def button(
        self,
        control: ControlShadowEvent,
        index: UnsafeIndex,
        *args: Any
    ) -> bool:
        """Generic fader buttons"""
        index = self._selection[control.getControl().coordinate[1]]

        if control.double or mixer.isTrackSolo(index):
            mixer.soloTrack(index)
        else:
            mixer.muteTrack(index)

        return True


ExtensionManager.registerWindowPlugin(Mixer)
