"""
tests > test_devices

Test to ensure device objects are behaving correctly
"""

from common import ExtensionManager


def test_create():
    for dev in ExtensionManager.getAllDevices():
        dev.create(None)


def test_getId():
    for dev in ExtensionManager.getAllDevices():
        d = dev.create(None)
        # It should have dots in it somewhere
        assert "." in d.getId()


def test_getUniversalEnquiryResponsePattern():
    for dev in ExtensionManager.getAllDevices():
        d = dev.create(None)
        d.getUniversalEnquiryResponsePattern()
