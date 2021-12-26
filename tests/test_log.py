"""
tests > test_log

Tests for the logger
"""

import pytest

from logger import log
from logger import verbosity

def test_log_too_verbose(capsys: pytest.CaptureFixture):
    log("", "test")
    
    captured = capsys.readouterr()
    
    assert captured.out == ""

def test_log_verbosity(capsys: pytest.CaptureFixture):
    log("", "test", verbosity.ERROR)
    
    captured = capsys.readouterr()
    
    assert captured.out == "test\n"

def test_log_category(capsys: pytest.CaptureFixture):
    log("general", "test")
    
    captured = capsys.readouterr()
    
    assert captured.out == "test\n"
