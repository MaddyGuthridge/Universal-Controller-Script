"""
integrations > mapping_strategies > jog_strategy

Strategy for mapping jog wheels

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""

import ui

from typing import Any
from control_surfaces import consts

from control_surfaces import (
    JogWheel,
    StandardJogWheel,
    ShiftedJogWheel,
    MoveJogWheel,
)
from control_surfaces import ControlShadowEvent
from devices import DeviceShadow


class JogStrategy:
    """
    Maps jog wheels to forwards/backwards navigation
    """
    def __init__(self, shadow: DeviceShadow) -> None:
        """
        Maps jog wheels to forwards/backwards navigation

        ### Args:
        * `shadow` (`DeviceShadow`): device shadow to bind on
        """
        shadow.bindMatches(
            JogWheel,
            self.jogWheel,
            one_type=False,
        )

    def jogWheel(
        self,
        control: ControlShadowEvent,
        *args: Any
    ) -> bool:
        if control.value == consts.JOG_NEXT:
            increment = 1
        elif control.value == consts.JOG_PREV:
            increment = -1
        elif control.value == consts.JOG_SELECT:
            ui.enter()
            return True
        else:
            return True

        if isinstance(control.getControl(), StandardJogWheel):
            ui.jog(increment)
        elif isinstance(control.getControl(), ShiftedJogWheel):
            ui.jog(increment)
        elif isinstance(control.getControl(), MoveJogWheel):
            ui.moveJog(increment)
        return True
