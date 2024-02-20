"""
integrations > core > final_transport

Fallback mappings for transport controls that can be overridden by other
plugins.

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""

from common.extension_manager import ExtensionManager
from devices import DeviceShadow
from integrations import CoreIntegration
from integrations.mapping_strategies import (
    CcForwardStrategy,
    DirectionStrategy,
    JogStrategy,
    NoteStrategy,
    WheelStrategy,
    PedalStrategy,
)


class FinalTransport(CoreIntegration):
    """
    The transport plugin manages basic transport commands, such as play/pause
    commands and navigation commands.
    """

    def __init__(self, shadow: DeviceShadow) -> None:
        shadow.setMinimal(True)
        DirectionStrategy(shadow),
        JogStrategy(shadow),
        NoteStrategy(shadow),
        WheelStrategy(shadow),
        PedalStrategy(shadow),
        CcForwardStrategy(shadow),

        super().__init__(shadow)

    @classmethod
    def create(cls, shadow: DeviceShadow) -> 'CoreIntegration':
        return cls(shadow)

    @classmethod
    def shouldBeActive(cls) -> bool:
        return True


ExtensionManager.special.register(FinalTransport)
