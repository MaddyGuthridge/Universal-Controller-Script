"""
devices > novation > launchkey > incontrol > incontrol

Contains code for managing the InControl state used by some launchkey devices.

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""
from typing import Optional
from control_surfaces import ControlSurface, ControlEvent, NullControl
from control_surfaces.matchers import IControlMatcher
from control_surfaces.event_patterns import BasicPattern, ForwardedPattern
from fl_classes import FlMidiMsg
from common.util.events import forwardEvent

from .controls.drum_pad import LkDrumPad

# Pattern for matching
INCONTROL_MATCH = ForwardedPattern(
    2,
    BasicPattern(0x9F, range(0x0C, 0x11), ...)
)

# Events for enabling and disabling  InControl
INCONTROL_ENABLE = FlMidiMsg(0x9F, 0x0C, 0x7F)
INCONTROL_DISABLE = FlMidiMsg(0x9F, 0x0C, 0x00)

# Patterns for recognizing and managing InControl buttons
FADERS_BUTTON = ForwardedPattern(2, BasicPattern(0x9F, 0x0E, 0x00))
FADERS_RESPONSE = FlMidiMsg(0x9F, 0x0E, 0x7F)
KNOBS_BUTTON = ForwardedPattern(2, BasicPattern(0x9F, 0x0D, 0x00))
KNOBS_RESPONSE = FlMidiMsg(0x9F, 0x0D, 0x7F)
DRUMS_BUTTON = ForwardedPattern(2, BasicPattern(0x9F, 0x0F, 0x00))
DRUMS_RESPONSE = FlMidiMsg(0x9F, 0x0F, 0x7F)


class InControl:
    """
    Contains code for managing the InControl/DAW mode for some LaunchKey
    Devices.
    """
    def __init__(self, matcher: IControlMatcher) -> None:
        self._enabled = False
        self._matcher = matcher

    def enable(self):
        # Disable before we enable to ensure it's set up correctly
        self.disable()
        forwardEvent(INCONTROL_ENABLE, 2)

    def disable(self):
        forwardEvent(INCONTROL_DISABLE, 2)

    def handleButtons(self, event: FlMidiMsg):
        """Handle presses of the InControl buttons, so that users don't
        accidentally disable InControl mode, which will lead to broken
        behavior.
        """
        if FADERS_BUTTON.matchEvent(event):
            forwardEvent(FADERS_RESPONSE, 2)
        elif KNOBS_BUTTON.matchEvent(event):
            forwardEvent(KNOBS_RESPONSE, 2)
        elif DRUMS_BUTTON.matchEvent(event):
            forwardEvent(DRUMS_RESPONSE, 2)
            self.refreshDrumPads()

    def refreshDrumPads(self):
        """Refresh drum pads on startup so that their colors don't break
        """
        for control in self._matcher.getControls():
            if isinstance(control, LkDrumPad):
                control.onColorChange(control.color)


class InControlMatcher(IControlMatcher):
    """Event matcher for InControl events
    """
    def __init__(self, manager: InControl) -> None:
        super().__init__()
        self._manager = manager
        self._event = NullControl.create(INCONTROL_MATCH)

    def matchEvent(self, event: FlMidiMsg) -> Optional[ControlEvent]:
        m = self._event.match(event)
        if m is not None:
            self._manager.handleButtons(event)
        return m

    def getGroups(self) -> set[str]:
        return {"null"}

    def getControls(self, group: Optional[str] = None) -> list[ControlSurface]:
        if group is not None and group != "InControl":
            return []
        else:
            return [self._event]

    def tick(self, thorough: bool) -> None:
        return
