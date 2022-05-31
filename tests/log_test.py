"""
tests > test_log

Tests for the logger

Authors:
* Miguel Guthridge [hdsq@outlook.com.au]

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""

import pytest

from common.logger import log
from common.logger import verbosity


def test_log_too_verbose(capsys: pytest.CaptureFixture):
    log("", "test")

    captured = capsys.readouterr()

    assert captured.out == ""


def test_log_verbosity(capsys: pytest.CaptureFixture):
    log("", "test", verbosity.ERROR)

    captured = capsys.readouterr()

    out: str = captured.out
    assert out.find("test\n") != -1

# def test_log_category(capsys: pytest.CaptureFixture):
#     log("general", "test")
#
#     captured = capsys.readouterr()
#
#     out: str = captured.out
#     assert out.find("test\n") != -1
