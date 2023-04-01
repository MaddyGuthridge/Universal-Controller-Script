"""
common > exceptions

Contains definitions for custom exceptions used by the script.

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""


class UcsException(Exception):
    """Base exception type for exceptions within the universal controller
    script
    """


class UcsError(UcsException):
    """Base type for critical errors within the universal controller script
    """


class EventForwardError(UcsError):
    """Errors to do with forwarding events"""


class EventEncodeError(EventForwardError):
    """Failed to encode event"""


class EventDecodeError(EventForwardError):
    """Failed to decode event"""


class EventDispatchError(EventForwardError):
    """Failed to dispatch event"""


class EventInspectError(EventForwardError):
    """Insufficient or incorrect information to inspect event"""


class DeviceRecognizeError(UcsError):
    """Failed to recognize device"""


class DeviceInitializeError(UcsError):
    """Failed to initialise device"""


class InvalidConfigError(UcsError):
    """Errors in configuration"""
