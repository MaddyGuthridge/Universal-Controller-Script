"""
plugs > mapping_strategies > mute_solo

Mappings for mute/solo buttons

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""

from typing import Callable, Any
from common.types import Color
from common.plug_indexes import UnsafeIndex
from control_surfaces import (
    ControlShadowEvent,
    ControlShadow,
    GenericFaderButton,
    MuteButton,
    SoloButton,
)
from devices import DeviceShadow
from plugs.event_filters import filterButtonLift
from .mapping_strategy import IMappingStrategy

COLOR_DISABLED = Color.fromGrayscale(0.3, False)


class MuteSoloStrategy(IMappingStrategy):
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
        selected_callback: Callable[[int], int],
        mute_callback: Callable[[int], None],
        is_mute_callback: Callable[[int], bool],
        solo_callback: Callable[[int], None],
        is_solo_callback: Callable[[int], bool],
        color_callback: Callable[[int], int],
    ) -> None:
        """
        Create a MuteSoloStrategy

        This binds MuteButton, SoloButton and GenericFaderButton controls and
        maps them to the provided callback functions, which are used to handle
        events from the controls and color the controls.

        ### Args:
        * `selected_callback` (`Callable[[int], int]`): given an int n, returns
          the nth selected track index. Note that if there aren't enough
          tracks, an IndexError should be raised.

        * `mute_callback` (`Callable[[int], None]`): toggles whether the track
          at the given index is muted.

        * `is_mute_callback` (`Callable[[int], bool]`): returns whether the
          track at the given index is muted.

        * `solo_callback` (`Callable[[int], None]`): toggles whether the track
          at the given index is solo.

        * `is_solo_callback` (`Callable[[int], bool]`): returns whether the
          track at the given index is solo.

        * `color_callback` (`Callable[[int], int]`): returns the color of the
          track at the given index.
        """
        self.selected = selected_callback
        self.mute = mute_callback
        self.is_mute = is_mute_callback
        self.solo = solo_callback
        self.is_solo = is_solo_callback
        self.color = color_callback

    def apply(self, shadow: DeviceShadow) -> None:
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
        index: UnsafeIndex,
        number: int,
        *args: Any,
    ) -> bool:
        try:
            track = self.selected(number)
        except IndexError:
            return True
        if control.double or self.is_solo(track):
            self.solo(track)
        else:
            self.mute(track)
        return True

    def tGeneric(
        self,
        control: ControlShadow,
        index: UnsafeIndex,
        number: int,
        *args: Any,
    ):
        try:
            track = self.selected(number)
        except IndexError:
            # Out of range tracks should be disabled
            control.color = Color()
            return
        if self.is_mute(track):
            control.color = COLOR_DISABLED
        else:
            control.color = Color.fromInteger(self.color(track))
        return True

    @filterButtonLift()
    def eMute(
        self,
        control: ControlShadowEvent,
        index: UnsafeIndex,
        number: int,
        *args: Any,
    ) -> bool:
        try:
            track = self.selected(number)
        except IndexError:
            return True
        self.mute(track)
        return True

    def tMute(
        self,
        control: ControlShadow,
        index: UnsafeIndex,
        number: int,
        *args: Any,
    ):
        try:
            track = self.selected(number)
        except IndexError:
            # Out of range tracks should be disabled
            control.color = Color()
            return
        if self.is_mute(track):
            control.color = Color.fromInteger(self.color(track))
        else:
            control.color = COLOR_DISABLED
        return True

    @filterButtonLift()
    def eSolo(
        self,
        control: ControlShadowEvent,
        index: UnsafeIndex,
        number: int,
        *args: Any,
    ) -> bool:
        try:
            track = self.selected(number)
        except IndexError:
            return True
        if self.is_mute(track):
            self.mute(track)
        else:
            self.solo(track)
        return True

    def tSolo(
        self,
        control: ControlShadow,
        index: UnsafeIndex,
        number: int,
        *args: Any,
    ):
        try:
            track = self.selected(number)
        except IndexError:
            # Out of range tracks should be disabled
            control.color = Color()
            return
        if self.is_mute(track):
            control.color = COLOR_DISABLED
        else:
            control.color = Color.fromInteger(self.color(track))
        return True
