"""
tests > test_util

Basic tests for utility functions of the script

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""

from common.util.dict_tools import (
    recursiveMergeDictionaries,
    expandDictShorthand
)
from common.util.snap import snap


def test_expand_dict_shorthand():
    t = {
        "a.b": 1,
        "a.c": 2,
        "b.a": 3,
        "b.c": 4
    }
    exp = {
        "a": {
            "b": 1,
            "c": 2
        },
        "b": {
            "a": 3,
            "c": 4
        }
    }
    assert expandDictShorthand(t) == exp


def test_expand_dict_shorthand_complex():
    t = {
        "a.b": 1,
        "a.c": 2,
        "b.a.d": 3,
        "b.a.e": 5,
        "b.c": 4
    }
    exp = {
        "a": {
            "b": 1,
            "c": 2
        },
        "b": {
            "a": {
                "d": 3,
                "e": 5
            },
            "c": 4
        }
    }
    assert expandDictShorthand(t) == exp


def test_recursive_merge_simple():
    ref = {
        "a": {
            "b": 1,
            "c": 2
        },
        "d": 3
    }
    over = {
        "a": {
            "b": 3
        },
        "d": 4
    }
    exp = {
        "a": {
            "b": 3,
            "c": 2
        },
        "d": 4
    }
    assert recursiveMergeDictionaries(ref, over) == exp


def test_snap():
    # TODO: Use contexts to set settings
    assert snap(0.1, 0.2) == 0.1
    assert snap(0.181, 0.2) == 0.2
