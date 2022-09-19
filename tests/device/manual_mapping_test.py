"""
tests > device > manual_mapping_test

Tests that devices can be manually mapped through the configuration

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""

import pytest
from fl_model import FlContext
from common import getContext, ExtensionManager, unsafeResetContext
from common.states import WaitingForDevice, DeviceState
from fl_classes import FlMidiMsg
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

    def processEvent(self, event: FlMidiMsg) -> None:
        pass


@pytest.mark.parametrize(
    "dev", ExtensionManager.devices.all()
)
def test_manual_mapping(dev: Device):
    for id in dev.getSupportedIds():
        unsafeResetContext()
        getContext().settings.set("bootstrap.name_associations", [(id, id)])
        with FlContext() as fl:
            fl.device.name = id
            getContext().initialize(WaitingForDevice(DummyState))
            assert getContext().getDeviceId() == id
