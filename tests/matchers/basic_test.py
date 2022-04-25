from common.types import EventData
from common.eventpattern import BasicPattern
from controlsurfaces.valuestrategies import Data2Strategy
from devices.matchers import BasicControlMatcher

from controlsurfaces import ControlSurface


class SimpleControl(ControlSurface):
    """A simple control surface for testing

    It matches any event with a status of 0 and a data1 of i
    """
    def __init__(self, i: int) -> None:
        super().__init__(
            BasicPattern(0, i, ...),
            Data2Strategy(),
            "group",
        )


class SimplerControl(ControlSurface):
    """Another simple control surface for testing

    It matches any event with a status of 0, a data1 of i and a data2 of 0
    """
    def __init__(self, i: int) -> None:
        super().__init__(
            BasicPattern(0, i, 0),
            Data2Strategy(),
            "group",
        )


def test_match():
    """Test we can match things with a BasicControlMatcher"""
    matcher = BasicControlMatcher()
    c1 = SimpleControl(1)
    matcher.addControl(c1)
    c2 = SimpleControl(2)
    matcher.addControl(c2)

    assert matcher.matchEvent(EventData(0, 1, 0)).getControl() == c1

    assert matcher.matchEvent(EventData(0, 2, 0)).getControl() == c2

    assert matcher.matchEvent(EventData(0, 3, 0)) is None


def test_submatchers():
    """Test we can match things in sub matchers"""
    main = BasicControlMatcher()
    sub = BasicControlMatcher()
    c1 = SimpleControl(1)
    sub.addControl(c1)
    main.addSubMatcher(sub)

    match = main.matchEvent(EventData(0, 1, 0))
    assert match.getControl() == c1


def test_priorities():
    """Test control surfaces with higher priorities are matched first"""
    matcher = BasicControlMatcher()
    c1 = SimpleControl(1)
    matcher.addControl(c1, priority=1)
    c2 = SimplerControl(1)
    matcher.addControl(c2, priority=2)

    assert matcher.matchEvent(EventData(0, 1, 0)).getControl() == c2
    assert matcher.matchEvent(EventData(0, 1, 1)).getControl() == c1
