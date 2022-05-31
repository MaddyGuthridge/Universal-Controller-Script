"""
common > util > abstract_method_error

Contains the definition for an AbstractMethodError which can be used as a way
to quickly raise an exception when an abstract method of an interface should
have been implemented

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""


class AbstractMethodError(NotImplementedError):
    """Raised when an abstract method should have been implemented by a class
    """
    def __init__(self, container: 'type | object | None' = None) -> None:
        if isinstance(container, type):
            cls = str(container)
        elif container is None:
            cls = "<not provided>"
        else:
            cls = str(type(container))
        super().__init__(f"Abstract method not implemented by class {cls}")
