"""
integrations > core > manual_mapper.py

Contains code used to manually map control surface events to CC events in the
case where said events aren't handled.

This mapping is done by taking a snapshot of available device controls and
then assigning each control an index which it will output.

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""
from typing import Optional
import device
import general
import midi
from common.types import Color
from common.extension_manager import ExtensionManager
from control_surfaces import (
    GenericFader,
    GenericKnob,
    Encoder,
    ModXY,
    ControlShadowEvent,
    ControlShadow,
)
from devices import DeviceShadow
from integrations import CoreIntegration

# Only assign to CC values that are undefined by the MIDI spec
AVAILABLE_CCS = (
    [3, 9, 14, 15]
    + list(range(20, 32))
    + list(range(85, 91))
    + list(range(102, 120))
)
NUM_CCS = len(AVAILABLE_CCS)  # = 40

# After this, we cycle through all 16 channels to give 640 total events
# available, which should be more than enough for reasonable people.


class ManualMapper(CoreIntegration):
    """
    A plugin that manually maps controls from faders, knobs and various other
    controls into CC events that users can manually assign to parameters.
    """

    def __init__(self, shadow: DeviceShadow) -> None:
        shadow.setMinimal(True)
        self._faders_start = 0
        self._knobs_start = len(shadow.bindMatches(
            # https://github.com/python/mypy/issues/4717 is the bane of my
            # existence
            GenericFader,  # type: ignore
            self.eFaders,
            self.tFaders,
            allow_substitution=False,
            one_type=False,
            args_generator=...,
        ))
        self._encoders_start = len(shadow.bindMatches(
            Encoder,
            self.eEncoders,
            self.tEncoders,
            allow_substitution=False,
            one_type=False,
            args_generator=...,
        )) + self._knobs_start
        self._mods_start = len(shadow.bindMatches(
            GenericKnob,  # type: ignore
            self.eKnobs,
            self.tKnobs,
            allow_substitution=False,
            one_type=False,
            args_generator=...,
        )) + self._encoders_start
        shadow.bindMatches(
            ModXY,
            self.eMods,
            self.tMods,
            allow_substitution=False,
            args_generator=...,
        )
        super().__init__(shadow)

    @classmethod
    def create(cls, shadow: DeviceShadow) -> 'CoreIntegration':
        return cls(shadow)

    @classmethod
    def shouldBeActive(cls) -> bool:
        return True

    @staticmethod
    def getChannelAndCc(index: int) -> tuple[int, int]:
        """
        Returns the channel and CC number that should be assigned to an event
        given the index of that event

        ### Args:
        * `index` (`int`): index of event

        ### Returns:
        * `tuple[int, int]`: MIDI channel and CC number
        """
        return (index // NUM_CCS), (AVAILABLE_CCS[index % NUM_CCS])

    @staticmethod
    def calcEventId(channel: int, cc: int) -> Optional[int]:
        """
        Calculates and returns the event ID associated with an event, or
        `None` if it isn't linked.

        ### Args:
        * `channel` (`int`): channel

        * `cc` (`int`): control change number

        ### Returns:
        * `int`: event id
        """
        event_id = device.findEventID(
            midi.EncodeRemoteControlID(device.getPortNumber(), channel, cc)
        )
        if event_id == midi.REC_InvalidID:
            return None
        else:
            return event_id

    @classmethod
    def editEvent(cls, control: ControlShadowEvent, c_index: int) -> bool:
        """
        Edits the event to make it into a CC event that can be processed by FL
        Studio
        """
        channel, cc = cls.getChannelAndCc(c_index)
        # Find the associated event ID
        event_id = cls.calcEventId(channel, cc)
        # If that event ID is valid
        if event_id is not None:
            # Process it and prevent further processing
            general.processRECEvent(
                event_id,
                control.value_rec,
                midi.REC_MIDIController,
            )
            return True
        else:
            # Otherwise, let other plugins process it
            # but only after editing it so it can be assigned
            control.midi.status = (0xB << 4) + channel
            control.midi.data1 = cc
            control.midi.data2 = control.value_midi
            return False

    @classmethod
    def tickEvent(cls, control: ControlShadow, c_index: int):
        """
        Applies properties to the event if it is assigned as a REC event
        """
        channel, cc = cls.getChannelAndCc(c_index)
        # Find the associated event ID
        event_id = cls.calcEventId(channel, cc)
        # If that event ID isn't invalid
        if event_id is not None:
            control.connected = True
            control.annotation = device.getLinkedParamName(event_id)
            control.color = Color.ENABLED
            control.value = device.getLinkedValue(event_id)
        else:
            control.connected = False

    def eFaders(self, control: ControlShadowEvent, _, c_index: int) -> bool:
        return self.editEvent(control, self._faders_start + c_index)

    def tFaders(self, control: ControlShadow, _, c_index: int):
        return self.tickEvent(control, self._faders_start + c_index)

    def eKnobs(self, control: ControlShadowEvent, _, c_index: int) -> bool:
        return self.editEvent(control, self._knobs_start + c_index)

    def tKnobs(self, control: ControlShadow, _, c_index: int):
        return self.tickEvent(control, self._knobs_start + c_index)

    def eEncoders(self, control: ControlShadowEvent, _, c_index: int) -> bool:
        return self.editEvent(control, self._encoders_start + c_index)

    def tEncoders(self, control: ControlShadow, _, c_index: int):
        return self.tickEvent(control, self._encoders_start + c_index)

    def eMods(self, control: ControlShadowEvent, _, c_index: int) -> bool:
        return self.editEvent(control, self._mods_start + c_index)

    def tMods(self, control: ControlShadow, _, c_index: int):
        self.tickEvent(control, self._mods_start + c_index)


ExtensionManager.super_special.register(ManualMapper)
