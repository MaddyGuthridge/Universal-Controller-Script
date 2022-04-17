
from typing import Optional
from controlsurfaces import ControlSurface, ControlEvent, NullEvent
from devices.matchers import IControlMatcher
from common.eventpattern import BasicPattern, ForwardedPattern
from common.types import EventData
from common.util.events import forwardEvent

# Pattern for matching
INCONTROL_MATCH = ForwardedPattern(
    2,
    BasicPattern(0x9F, range(0x0C, 0x11), ...)
)

# Events for enabling and disabling  InControl
INCONTROL_ENABLE = EventData(0x9F, 0x0C, 0x7F)
INCONTROL_DISABLE = EventData(0x9F, 0x0C, 0x00)

# Patterns for recognising and managing InControl buttons
FADERS_BUTTON = ForwardedPattern(2, BasicPattern(0x9F, 0x0E, 0x00))
FADERS_RESPONSE = EventData(0x9F, 0x0E, 0x7F)
KNOBS_BUTTON = ForwardedPattern(2, BasicPattern(0x9F, 0x0D, 0x00))
KNOBS_RESPONSE = EventData(0x9F, 0x0D, 0x7F)
DRUMS_BUTTON = ForwardedPattern(2, BasicPattern(0x9F, 0x0F, 0x00))
DRUMS_RESPONSE = EventData(0x9F, 0x0F, 0x7F)


class InControl:

    def __init__(self) -> None:
        self._enabled = False

    def enable(self):
        forwardEvent(INCONTROL_ENABLE, 2)

    def disable(self):
        forwardEvent(INCONTROL_DISABLE, 2)

    def handleButtons(self, event: EventData):
        """Handle presses of the InControl buttons, so that users don't
        accidentally disable InControl mode, which will lead to broken
        behaviour.
        """
        if FADERS_BUTTON.matchEvent(event):
            forwardEvent(FADERS_RESPONSE, 2)
        elif KNOBS_BUTTON.matchEvent(event):
            forwardEvent(KNOBS_RESPONSE, 2)
        elif DRUMS_BUTTON.matchEvent(event):
            forwardEvent(DRUMS_RESPONSE, 2)


class InControlMatcher(IControlMatcher):
    """Event matcher for InControl events
    """
    def __init__(self, manager: InControl) -> None:
        super().__init__()
        self._manager = manager
        self._event = NullEvent(INCONTROL_MATCH)

    def matchEvent(self, event: EventData) -> Optional[ControlEvent]:
        m = self._event.match(event)
        if m is not None:
            self._manager.handleButtons(event)
        return m

    def getGroups(self) -> set[str]:
        return {"null"}

    def getControls(self, group: str = None) -> list[ControlSurface]:
        if group is not None and group != "InControl":
            return []
        else:
            return [self._event]
