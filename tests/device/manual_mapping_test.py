"""
tests > device > manual_mapping

Tests that devices can be manually mapped through the configuration
"""

import pytest
from fl_context import FlContext
from common import getContext, ExtensionManager, unsafeResetContext
from common.states import WaitingForDevice, DeviceState
from common.types import EventData
from devices import Device


class DummyState(DeviceState):
    @classmethod
    def create(cls, device: 'Device') -> 'DeviceState':
        getContext().registerDevice(device)
        return cls()

    def initialize(self) -> None:
        pass

    def deinitialize(self) -> None:
        pass

    def tick(self) -> None:
        pass

    def processEvent(self, event: EventData) -> None:
        pass


@pytest.mark.parametrize(
    "dev", ExtensionManager.devices.all()
)
def test_manual_mapping(dev: Device):
    for id in dev.getSupportedIds():
        unsafeResetContext()
        getContext().settings.set("bootstrap.name_associations", [(id, id)])
        with FlContext({"device_name": id}):
            getContext().initialize(WaitingForDevice(DummyState))
            assert getContext().getDeviceId() == id
