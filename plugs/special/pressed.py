"""
plugs > special > pressed

Contains the definition for the press plugin

Authors:
* Miguel Guthridge [hdsq@outlook.com.au]
"""

from typing import Any
from common.types import Color
from common.extensionmanager import ExtensionManager
from common.util.apifixes import UnsafeIndex
from controlsurfaces import (
    DrumPad,
    Button,
    Note,
    Knob,
    Fader,
    Encoder,
    ModWheel,
    PitchWheel,
)
from controlsurfaces import ControlShadowEvent
from devices import DeviceShadow
from plugs import SpecialPlugin


OFF = Color()
ON = Color.fromInteger(0xFFFFFF)


class Press(SpecialPlugin):
    """
    Used to add colours to each control surface when it is pressed or recently
    tweaked.
    """

    def __init__(self, shadow: DeviceShadow) -> None:
        shadow.setMinimal(True)
        shadow.setTransparent(True)
        self._velocities = (
            shadow.bindMatches(DrumPad, self.any, raise_on_failure=False)
            + shadow.bindMatches(Note, self.any, raise_on_failure=False)
        )
        self._buttons = (
            shadow.bindMatches(Button, self.any, raise_on_failure=False)
        )
        self._others = (
            shadow.bindMatches(Knob, self.any, raise_on_failure=False)
            + shadow.bindMatches(Fader, self.any, raise_on_failure=False)
            + shadow.bindMatches(Encoder, self.any, raise_on_failure=False)
            + shadow.bindMatches(ModWheel, self.any, raise_on_failure=False)
            + shadow.bindMatches(PitchWheel, self.any, raise_on_failure=False)
        )
        super().__init__(shadow, [])

    @staticmethod
    def shouldBeActive() -> bool:
        return True

    @classmethod
    def create(cls, shadow: DeviceShadow) -> 'SpecialPlugin':
        return cls(shadow)

    def any(
        self,
        control: ControlShadowEvent,
        index: UnsafeIndex,
        *args: Any
    ) -> bool:
        return False

    def tick(self):
        self.tickVelocities()
        self.tickButtons()

    def tickVelocities(self):
        for c in self._velocities:
            c.color = Color.fade(OFF, ON, c.getControl().value)

    def tickButtons(self):
        for c in self._buttons:
            c.color = ON if c.getControl().value else OFF


ExtensionManager.registerSpecialPlugin(Press)
