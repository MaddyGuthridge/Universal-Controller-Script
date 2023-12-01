from typing import Protocol, TypeVar, Generic


TIn = TypeVar('TIn', contravariant=True)
TOut = TypeVar('TOut', covariant=True)


class Decorator(Protocol, Generic[TIn, TOut]):
    """
    Represents a decorated value, used to simplify type definitions.

    ### Usage

    For functions that return a decorator function, annotate the return type as
    `Decorator[InputType, OutputType]`

    ### Example

    If we have the following type alias:

    ```py
    IntFunction = Callable[[int, int], int]
    ```

    And the following function that matches its definition:

    ```py
    def add(a: int, b: int) -> int:
        return a + b
    ```

    We can type a decorator function as follows:

    ```py
    def register_operator(op: str) -> Decorator[IntFunction, IntFunction]:
        def inner(value: IntFunction) -> IntFunction:
            # register the function or whatever
            return value
        return inner
    ```
    """
    def __call__(self, value: TIn) -> TOut:
        ...
