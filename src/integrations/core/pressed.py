"""
integrations > core > pressed

Contains the definition for the pressed controls integration, which is
responsible for coloring control surfaces when they are pressed

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""

from typing import Any
from time import time
from common.types import Color
from common.extension_manager import ExtensionManager
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
from control_surfaces import ControlShadow
from devices import DeviceShadow
from integrations import CoreIntegration

# How much time to fade buttons to black
FADE_TIME = 1.0


def fadeOverTime(control: ControlSurface) -> float:
    """Fade to black over time"""
    # The longer it's been since we tweaked this control, the
    # more faded it should be
    return max(1.0 - (time() - control.last_tweaked) / FADE_TIME, 0)


class Press(CoreIntegration):
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
        super().__init__(shadow)

    @classmethod
    def shouldBeActive(cls) -> bool:
        return True

    @classmethod
    def create(cls, shadow: DeviceShadow) -> 'CoreIntegration':
        return cls(shadow)

    def any(
        self,
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
            if c.value:
                c.connected = True
                c.color = Color.fade(
                    Color.BLACK, Color.WHITE, control.value
                    # * fadeOverTime(control)
                )
            else:
                c.connected = False

    def tickButtons(self):
        for c in self._buttons:
            control = c.getControl()
            if control.value:
                c.connected = True
                c.color = Color.WHITE
                # Color.fade(Color.BLACK, Color.WHITE, fadeOverTime(control))
            else:
                c.connected = False

    def tickOthers(self):
        for c in self._others:
            control = c.getControl()
            fade = fadeOverTime(control)
            if fade:
                c.connected = True
                c.color = Color.fade(Color.BLACK, Color.WHITE, fade)
            else:
                c.connected = False


ExtensionManager.super_special.register(Press)
