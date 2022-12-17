"""
tests > profiler_test

Tests for the profiler system.

If these tests fail, it is likely due to PC performance, and the leeways may
need to be increased.

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""
import pytest
import time
from common import getContext, unsafeResetContext
from common.profiler import ProfilerContext, profilerDecoration
from tests.helpers import floatApproxEqMagnitude
from tests.helpers.performance import perfTestsSkipped


@pytest.mark.skipif(**perfTestsSkipped())
def test_timing_context():
    unsafeResetContext()
    getContext().enableProfiler()
    with ProfilerContext("test"):
        time.sleep(0.01)
    res = getContext().profiler.getTotals()  # type: ignore
    assert floatApproxEqMagnitude(10.0, res["test"], 0.6)


@pytest.mark.skipif(**perfTestsSkipped())
def test_timing_decorator():
    unsafeResetContext()
    getContext().enableProfiler()

    @profilerDecoration("test")
    def slowFunction():
        time.sleep(0.01)
    slowFunction()
    res = getContext().profiler.getTotals()  # type: ignore
    assert floatApproxEqMagnitude(10.0, res["test"], 1)


@pytest.mark.skipif(**perfTestsSkipped())
def test_total_repeated():
    unsafeResetContext()
    getContext().enableProfiler()
    for _ in range(10):
        with ProfilerContext("test"):
            time.sleep(0.01)
    res = getContext().profiler.getTotals()  # type: ignore
    assert floatApproxEqMagnitude(100.0, res["test"], 5)


@pytest.mark.skipif(**perfTestsSkipped())
def test_nested_profiles():
    unsafeResetContext()
    getContext().enableProfiler()
    with ProfilerContext("test1"):
        time.sleep(0.01)
        with ProfilerContext("test2"):
            time.sleep(0.01)
    res = getContext().profiler.getTotals()  # type: ignore
    assert floatApproxEqMagnitude(20.0, res["test1"], 2)
    assert floatApproxEqMagnitude(10.0, res["test1.test2"], 1)


def test_numbers():
    unsafeResetContext()
    getContext().enableProfiler()
    for _ in range(10):
        with ProfilerContext("test"):
            pass
    assert getContext().profiler.getNumbers() == {  # type: ignore
        "test": 10
    }


@pytest.mark.skipif(**perfTestsSkipped())
def test_maxes():
    times = [0.01, 0.03, 0.05, 0.02]
    unsafeResetContext()
    getContext().enableProfiler()
    for t in times:
        with ProfilerContext("test"):
            time.sleep(t)
    res = getContext().profiler.getMaxes()  # type: ignore
    assert floatApproxEqMagnitude(50.0, res["test"], 1)
