
from typing import Any
import midi
import ui
import mixer
import transport
import general
from common import getContext
from common.extensionmanager import ExtensionManager
from common.util.apifixes import (
    UnsafeIndex,
    getSelectedDockMixerTracks,
    getMixerDockSides,
    getSelectedMixerTracks,
)
from common.util.snap import snap
from controlsurfaces import consts
from controlsurfaces import ControlShadowEvent
from controlsurfaces import (
    JogWheel,
    StandardJogWheel,
    Fader,
    Knob,
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
    return snap(value * 2 - 1, 0)

class Mixer(WindowPlugin):
    """
    Used to process events directed
    """
    def __init__(self, shadow: DeviceShadow) -> None:
        super().__init__(shadow, [])

        # Bind jog wheel
        self._faders = shadow.bindMatches(JogWheel, self.jogWheel, raise_on_failure=False)

        # Bind main controls
        self._faders  = shadow.bindMatches(Fader,              self.fader,  raise_on_failure=False)
        self._knobs   = shadow.bindMatches(Knob,               self.knob,   raise_on_failure=False)
        self._knobs   = shadow.bindMatches(Knob,               self.knob,   raise_on_failure=False)
        self._buttons = shadow.bindMatches(GenericFaderButton, self.button, raise_on_failure=False)
        self._mutes   = shadow.bindMatches(MuteButton,         self.mute,   raise_on_failure=False)
        self._solos   = shadow.bindMatches(SoloButton,         self.solo,   raise_on_failure=False)
        self._arms    = shadow.bindMatches(ArmButton,          self.arm,    raise_on_failure=False)
        self._selects = shadow.bindMatches(SelectButton,       self.select, raise_on_failure=False)

        # List of last presses for fader buttons
        self._button_press_times = [0.0 for _ in self._buttons]

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
        * This doesn't respect docking sides: as soon as the mixer rectangle can
          be displayed in a way that respects them, change this
        """
        selected = getSelectedMixerTracks()

        if len(selected) == 0:
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
         or last  > self._selection[0] + self._len - 1
        ):
            self._selection = list(range(first, first+self._len))
            ui.miDisplayRect(first, first+self._len-1, 2000)

    def tick(self):
        self.updateSelected()

    def jogWheel(self, control: ControlShadowEvent, index: UnsafeIndex, *args: Any) -> bool:
        selected = getSelectedMixerTracks()
        if len(selected) == 0:
            selected = [0]
        # Calculate increment
        if control.value == consts.ENCODER_NEXT:
            dest =  selected[-1] + 1
        elif control.value == consts.ENCODER_PREV:
            dest =  selected[0] - 1
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

    def fader(self, control: ControlShadowEvent, index: UnsafeIndex, *args: Any) -> bool:
        """Faders -> volume"""
        index = self._selection[control.getControl().coordinate[1]]

        mixer.setTrackVolume(index, snapFaders(control.value))

        return True

    def knob(self, control: ControlShadowEvent, index: UnsafeIndex, *args: Any) -> bool:
        """Knobs -> panning"""
        index = self._selection[control.getControl().coordinate[1]]
        mixer.setTrackPan(index, snapKnobs(control.value))

        return True

    @filterButtonLift
    def mute(self, control: ControlShadowEvent, index: UnsafeIndex, *args: Any) -> bool:
        """Mute track"""
        index = self._selection[control.getControl().coordinate[1]]
        mixer.muteTrack(index)
        return True

    @filterButtonLift
    def solo(self, control: ControlShadowEvent, index: UnsafeIndex, *args: Any) -> bool:
        """Solo track"""
        index = self._selection[control.getControl().coordinate[1]]
        mixer.soloTrack(index)
        return True

    @filterButtonLift
    def arm(self, control: ControlShadowEvent, index: UnsafeIndex, *args: Any) -> bool:
        """Arm track"""
        index = self._selection[control.getControl().coordinate[1]]
        mixer.armTrack(index)
        return True

    @filterButtonLift
    def select(self, control: ControlShadowEvent, index: UnsafeIndex, *args: Any) -> bool:
        """Select track"""
        index = self._selection[control.getControl().coordinate[1]]
        mixer.selectTrack(index)
        return True

    @filterButtonLift
    def button(self, control: ControlShadowEvent, index: UnsafeIndex, *args: Any) -> bool:
        index = self._selection[control.getControl().coordinate[1]]

        if control.double:
            mixer.soloTrack(index)
        else:
            mixer.muteTrack(index)

        return True

ExtensionManager.registerWindowPlugin(Mixer)
