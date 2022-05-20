"""
common > util > abstractmethoderror

Contains the definition for an AbstractMethodError which can be used as a way
to quickly raise an exception when an abstract method of an interface should
have been implemented
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
