"""
integrations > mapping_strategies > mute_solo

Mappings for mute/solo buttons

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""

from typing import Callable, Any
from common.tracks import AbstractTrack
from common.types import Color
from common.plug_indexes.fl_index import FlIndex
from control_surfaces import (
    ControlShadowEvent,
    ControlShadow,
    GenericFaderButton,
    MuteButton,
    SoloButton,
)
from devices import DeviceShadow
from integrations.event_filters import filterButtonLift

COLOR_DISABLED = Color.fromGrayscale(0.3, False)


class MuteSoloStrategy:
    """
    Binds mute and solo buttons to mute tracks at the given callback functions,
    as well as providing colorization functionality.

    ### Selection
    * The plugin using this strategy must provide a selected_callback which
      returns the track number associated with a control index. The plugin
      should either calculate these indexes dynamically or maintain a list of
      indexes itself. If a track is out of bounds, an IndexError should be
      raised.

    ### Colorization
    * If a track is enabled, generic and solo buttons will be colored and the
      mute button will be dull.
    * If a track is disabled, generic and solo buttons will be dull and the
      mute button will be colored.
    * Out of bounds tracks will be colored black.

    This is so that all available tracks are colored, which will improve
    usability.
    """
    def __init__(
        self,
        shadow: DeviceShadow,
        selected_callback: Callable[[int], AbstractTrack],
    ) -> None:
        """
        Create a MuteSoloStrategy

        This binds MuteButton, SoloButton and GenericFaderButton controls and
        maps them to the provided callback functions, which are used to handle
        events from the controls and color the controls.

        ### Args:
        * `shadow` (`DeviceShadow`): the device shadow to bind to

        * `selected_callback` (`Callable[[int], AbstractTrack]`): given an int
          n, returns the nth selected track. Note that if there aren't enough
          tracks, an IndexError should be raised.
        """
        self.selected = selected_callback

        self._buttons = shadow.bindMatches(
            GenericFaderButton,
            self.eGeneric,
            self.tGeneric,
            args_generator=...
        )
        self._mutes = shadow.bindMatches(
            MuteButton,
            self.eMute,
            self.tMute,
            args_generator=...
        )
        self._solos = shadow.bindMatches(
            SoloButton,
            self.eSolo,
            self.tSolo,
            args_generator=...
        )

    @filterButtonLift()
    def eGeneric(
        self,
        control: ControlShadowEvent,
        index: FlIndex,
        number: int,
        *args: Any,
    ) -> bool:
        try:
            track = self.selected(number)
        except IndexError:
            return True
        if control.double or track.solo:
            track.soloToggle()
        else:
            track.muteToggle()
        return True

    def tGeneric(
        self,
        control: ControlShadow,
        index: FlIndex,
        number: int,
        *args: Any,
    ):
        try:
            track = self.selected(number)
        except IndexError:
            # Out of range tracks should be disabled
            control.color = Color()
            return
        if track.mute:
            control.color = COLOR_DISABLED
        else:
            control.color = track.color
        return True

    @filterButtonLift()
    def eMute(
        self,
        control: ControlShadowEvent,
        index: FlIndex,
        number: int,
        *args: Any,
    ) -> bool:
        try:
            track = self.selected(number)
        except IndexError:
            return True
        track.muteToggle()
        return True

    def tMute(
        self,
        control: ControlShadow,
        index: FlIndex,
        number: int,
        *args: Any,
    ):
        try:
            track = self.selected(number)
        except IndexError:
            # Out of range tracks should be disabled
            control.color = Color()
            return
        if track.mute:
            control.color = track.color
        else:
            control.color = COLOR_DISABLED
        return True

    @filterButtonLift()
    def eSolo(
        self,
        control: ControlShadowEvent,
        index: FlIndex,
        number: int,
        *args: Any,
    ) -> bool:
        try:
            track = self.selected(number)
        except IndexError:
            return True
        if track.mute:
            track.muteToggle()
        else:
            track.soloToggle()
        return True

    def tSolo(
        self,
        control: ControlShadow,
        index: FlIndex,
        number: int,
        *args: Any,
    ):
        try:
            track = self.selected(number)
        except IndexError:
            # Out of range tracks should be disabled
            control.color = Color()
            return
        if track.mute:
            control.color = COLOR_DISABLED
        else:
            control.color = track.color
        return True
