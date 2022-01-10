
from __future__ import annotations
from typing import TYPE_CHECKING

from common.types.eventdata import eventData

if TYPE_CHECKING:
    from common import IEventPattern
    from devices import Device

class ExtensionManager:
    
    _plugins: dict[str, type] = dict()
    _devices: list[tuple[IEventPattern, type[Device]]] = []
    
    def __init__(self) -> None:
        raise TypeError("ExtensionManager is a static class and cannot be instantiated.")

    @classmethod
    def registerPlugin(cls, plugin) -> None:
        pass

    @classmethod
    def registerDevice(cls, device: type[Device]) -> None:
        key = device.getUniversalEnquiryResponsePattern()
        if key in cls._devices:
            raise ValueError("A device matching this pattern already exists")
        cls._devices.append((key, device))

    @classmethod
    def getDevice(cls, event: eventData) -> Device:
        for pattern, device in cls._devices:
            if pattern.matchEvent(event):
                # All devices
                return device.create(event)
        raise ValueError("Device not recognised")
