"""
tests > devices_test

Tests to ensure device objects are behaving correctly

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
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
