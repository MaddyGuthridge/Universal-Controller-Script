"""
common > types > bool_s

Contains the BoolS type as well as TrueS and FalseS types, which can be used in
place of boolean types when a description is required.

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""


class BoolS:
    """
    A boolean-like class that allows a string description to explain the value
    whilst still implementing truthiness properties that function independently
    of the string contents.
    """
    def __init__(self, value: bool, description: str) -> None:
        self.__value = value
        self.__description = description

    def __repr__(self) -> str:
        return self.__description

    def __bool__(self) -> bool:
        return self.__value


class TrueS(BoolS):
    """
    A literal True, but with a string description
    """
    def __init__(self, description: str) -> None:
        super().__init__(True, description)


class FalseS(BoolS):
    """
    A literal False, but with a string description
    """
    def __init__(self, description: str) -> None:
        super().__init__(False, description)
