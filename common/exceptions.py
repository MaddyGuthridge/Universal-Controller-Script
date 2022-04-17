"""
common > exceptions

Contains definitions for custom exceptions used by the script.
"""


class UcsException(Exception):
    """Base exception type for exceptions within the universal controller
    script
    """


class EventForwardError(UcsException):
    """Errors to do with forwarding events
    """


class EventEncodeError(EventForwardError):
    """Failed to encode event"""


class EventDecodeError(EventForwardError):
    """Failed to decode event"""


class EventDispatchError(EventForwardError):
    """Failed to dispatch event"""


class EventInspectError(EventForwardError):
    """Insufficient or incorrect information to inspect event"""

class DeviceRecogniseError(UcsException):
    """Failed to recognise device"""
