"""
include > typing

A basic stand-in for the typing module, to prevent crashes during runtime
"""
print("I'm being imported")
TYPE_CHECKING = False

class TypeVar:
    def __init__(self, *args, **kwargs) -> None:
        pass

class NewType:
    def __init__(self, *args, **kwargs) -> None:
        pass
    
    def __call__(self, arg):
        return arg

Any = 'Any'
NoReturn = 'NoReturn'
Optional = 'Optional'
Callable = 'Callable'
Union = 'Union'
Type = 'Type'
Generic = 'Generic'

class Protocol:
    pass

def overload(func):
    return func
