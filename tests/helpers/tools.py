"""
tests > helpers > tools

Helper code for testing

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""
from typing import TypeVar, Generator

T = TypeVar("T")


def floatApproxEq(expected: float, actual: float) -> bool:
    """
    Return whether there is less than a 5% error between the expected
    and actual values, or if the expected value is zero, whether the actual
    value is within 0.001 of it.
    """
    if expected == 0:
        return abs(actual) < 0.001
    return abs(expected - actual) / abs(expected) < 0.05


def combinations(
    p: list[T],
    number: int
) -> Generator[tuple[T, ...], None, None]:
    """
    Generates a set of combinations

    ### Args:
    * `p` (`list[T]`): list to get combinations from
    * `number` (`int`): number of combinations to return on each iteration

    ### Raises:
    * `ValueError`: number must be >= 1

    ### Yields:
    * `Iterator[tuple[T, ...]]`: combinations
    """
    if number <= 0:
        raise ValueError("Expecting more combinations")
    if number == 1:
        for item in p:
            yield (item,)
    else:
        for item in p:
            for others in combinations(p, number-1):
                yield item, *others
