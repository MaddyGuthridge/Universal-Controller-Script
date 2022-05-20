"""
tests > test_devices

Test to ensure device objects are behaving correctly
"""

import pytest
from common import ExtensionManager


@pytest.mark.parametrize(
    'dev',
    ExtensionManager.devices.all()
)
def test_create(dev):
    dev.create(None)


def test_getId():
    for dev in ExtensionManager.devices.all():
        d = dev.create(None)
        # It should have dots in it somewhere
        assert "." in d.getId()


def test_getUniversalEnquiryResponsePattern():
    for dev in ExtensionManager.devices.all():
        d = dev.create(None)
        d.getUniversalEnquiryResponsePattern()
