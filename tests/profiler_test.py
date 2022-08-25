"""
tests > profiler_test

Tests for the profiler system

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""
import time
from common import getContext, unsafeResetContext
from common.profiler import ProfilerContext, profilerDecoration
from tests.helpers import floatApproxEqMagnitude


def test_timing_context():
    unsafeResetContext()
    getContext().enableProfiler()
    with ProfilerContext("test"):
        time.sleep(0.01)
    res = getContext().profiler.getTotals()
    assert floatApproxEqMagnitude(10.0, res["test"])


def test_timing_decorator():
    unsafeResetContext()
    getContext().enableProfiler()

    @profilerDecoration("test")
    def slowFunction():
        time.sleep(0.01)
    slowFunction()
    res = getContext().profiler.getTotals()
    assert floatApproxEqMagnitude(10.0, res["test"], 1)


def test_total_repeated():
    unsafeResetContext()
    getContext().enableProfiler()
    for _ in range(10):
        with ProfilerContext("test"):
            time.sleep(0.01)
    res = getContext().profiler.getTotals()
    assert floatApproxEqMagnitude(100.0, res["test"], 5)


def test_nested_profiles():
    unsafeResetContext()
    getContext().enableProfiler()
    with ProfilerContext("test1"):
        time.sleep(0.01)
        with ProfilerContext("test2"):
            time.sleep(0.01)
    res = getContext().profiler.getTotals()
    assert floatApproxEqMagnitude(20.0, res["test1"], 1)
    assert floatApproxEqMagnitude(10.0, res["test1.test2"], 1)


def test_numbers():
    unsafeResetContext()
    getContext().enableProfiler()
    for _ in range(10):
        with ProfilerContext("test"):
            pass
    assert getContext().profiler.getNumbers() == {
        "test": 10
    }


def test_maxes():
    times = [0.01, 0.03, 0.05, 0.02]
    unsafeResetContext()
    getContext().enableProfiler()
    for t in times:
        with ProfilerContext("test"):
            time.sleep(t)
    res = getContext().profiler.getMaxes()
    assert floatApproxEqMagnitude(50.0, res["test"], 0.5)
