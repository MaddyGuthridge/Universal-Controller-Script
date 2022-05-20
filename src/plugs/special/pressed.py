"""
plugs > special > pressed

Contains the definition for the press plugin

Authors:
* Miguel Guthridge [hdsq@outlook.com.au]
"""

from typing import Any
from time import time
from common.types import Color
from common.extension_manager import ExtensionManager
from common.util.api_fixes import UnsafeIndex
from control_surfaces import (
    DrumPad,
    Button,
    Note,
    Knob,
    Fader,
    Encoder,
    ModWheel,
    PitchWheel,
    ControlSurface,
)
from control_surfaces import ControlShadow, ControlShadowEvent
from devices import DeviceShadow
from plugs import SpecialPlugin

# How much time to fade buttons to black
FADE_TIME = 1.0

OFF = Color()
ON = Color.fromInteger(0xFFFFFF)


def fadeOverTime(control: ControlSurface) -> float:
    """Fade to black over time"""
    # The longer it's been since we tweaked this control, the
    # more faded it should be
    return max(1.0 - (time() - control.last_tweaked) / FADE_TIME, 0)


class Press(SpecialPlugin):
    """
    Used to add colors to each control surface when it is pressed or recently
    tweaked.
    """

    def bind_all(
        self,
        shadow: DeviceShadow,
        t: type[ControlSurface]
    ) -> list[ControlShadow]:
        """Continually bind all the controls"""
        ret: list[ControlShadow] = []
        while True:
            len_ret = len(ret)
            ret += shadow.bindMatches(t, self.any)
            if len_ret == len(ret):
                break
        return ret

    def __init__(self, shadow: DeviceShadow) -> None:
        shadow.setMinimal(True)
        shadow.setTransparent(True)
        self._velocities = (
            self.bind_all(shadow, DrumPad)
            + self.bind_all(shadow, Note)
        )
        self._buttons = self.bind_all(shadow, Button)
        self._others = (
            self.bind_all(shadow, Knob)
            + self.bind_all(shadow, Fader)
            + self.bind_all(shadow, Encoder)
            + self.bind_all(shadow, ModWheel)
            + self.bind_all(shadow, PitchWheel)
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

    def tick(self, *args):
        self.tickVelocities()
        self.tickButtons()
        self.tickOthers()

    def tickVelocities(self):
        for c in self._velocities:
            control = c.getControl()
            c.color = Color.fade(
                OFF, ON, control.value  # * fadeOverTime(control)
            )

    def tickButtons(self):
        for c in self._buttons:
            control = c.getControl()
            if control.value:
                c.color = ON  # Color.fade(OFF, ON, fadeOverTime(control))
            else:
                c.color = OFF

    def tickOthers(self):
        for c in self._others:
            control = c.getControl()
            c.color = Color.fade(OFF, ON, fadeOverTime(control))


ExtensionManager.final.register(Press)
