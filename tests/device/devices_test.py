"""
tests > test_devices

Test to ensure device objects are behaving correctly
"""

import pytest
from common import ExtensionManager
from devices import Device


@pytest.mark.parametrize(
    'dev',
    ExtensionManager.devices.all()
)
def test_create_from_id(dev: Device):
    for id in dev.getSupportedIds():
        dev.create(id=id)


@pytest.mark.parametrize(
    'dev',
    ExtensionManager.devices.all()
)
def test_create_from_response(dev: Device):
    pattern = dev.getUniversalEnquiryResponsePattern()
    if pattern is not None:
        dev.create(pattern.fulfil())
    else:
        dev.create(None)
