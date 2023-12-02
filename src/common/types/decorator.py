from typing import Protocol, TypeVar, Generic


# Hopefully in the future, we can specify that TOut defaults to TIn, but this
# requires the acceptance of PEP 696: https://peps.python.org/pep-0696/
# Instead, we'll just have to accept a more yucky subclassing system as per
# https://stackoverflow.com/a/77586364/6335363
TIn = TypeVar('TIn', contravariant=True)
TOut = TypeVar('TOut', covariant=True)
TSym = TypeVar('TSym')


class Decorator(Protocol, Generic[TIn, TOut]):
    """
    Represents a decorated value, used to simplify type definitions.

    If the input type matches the output type, consider using
    `SymmetricDecorator` for a simpler type defintion.

    ### Usage

    For functions that return a decorator function, annotate the return type as
    `Decorator[InputType, OutputType]`

    ### Example

    If we have the following type aliases:

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
    TFunction = Callable[[T, T], T]

    def int_fn_to_t_fn(t: type[T]) -> Decorator[IntFunction, TFunction]:
        def inner(fn: IntFunction) -> TFunction:
            def wrapper(a: T, b: T) -> T:
                a_int = int(a)
                b_int = int(b)
                return t(fn(a, b))
            return wrapper
        return inner
    ```
    """
    def __call__(self, value: TIn, /) -> TOut:
        ...


class SymmetricDecorator(Decorator[TSym, TSym], Generic[TSym], Protocol):
    """
    Represents a decorated value, used to simplify type definitions.

    `SymmetricDecorator` is used if the input type matches the output type.

    ### Usage

    For functions that return a decorator function, annotate the return type as
    `Decorator[ArgumentType]`

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
    def register_operator(op: str) -> SymmetricDecorator[IntFunction]:
        def inner(value: IntFunction) -> IntFunction:
            # register the function or whatever
            return value
        return inner
    ```
    """
