"""
common > profiler > manager

Contains the profiler manager

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""

from typing import Optional
import time

from common.util.console_helpers import NoneNoPrintout

MAX_NAME = 48


class ProfileNode:
    """
    A node in the profiler

    Manages our position in the profile by allowing us to build a stack of
    profiler nodes.
    """
    def __init__(self, parent: Optional['ProfileNode'], name: str):
        """
        Create a profile node

        ### Args:
        * `parent` (`Optional[ProfileNode]`): parent node
        * `name` (`str`): name of this node
        """
        self.parent = parent
        self.name = name
        self._children: list[ProfileNode] = []
        self._opened = time.time_ns()
        self._time: Optional[int] = None

    def close(self):
        """
        Close this profile node
        """
        self._time = time.time_ns() - self._opened

    def addChild(self, child: 'ProfileNode'):
        """
        Add a child node to this node

        ### Args:
        * `child` (`ProfileNode`): node to add
        """
        self._children.append(child)

    def getTime(self) -> int:
        """
        Return the time this node took

        ### Raises:
        * `ValueError`: not closed yet

        ### Returns:
        * `int`: time in nanoseconds
        """
        if self._time is None:
            raise ValueError("Not closed")
        return self._time

    def __str__(self) -> str:
        total_time = '<running>' if self._time is None else f"{self._time} ns"
        children = ', '.join([str(c) for c in self._children])
        return f"\"'{self.name}' ({total_time})\":[{children}]"


class ProfilerManager:
    """
    Class for managing profiles.

    It is called upon by profiler context managers in order to manage
    profiling.
    """
    @staticmethod
    def _getProfileName(n: ProfileNode) -> str:
        if n.parent is None:
            return n.name
        else:
            return ProfilerManager._getProfileName(n.parent) + "." + n.name

    def __init__(self, print_traces: bool) -> None:
        """
        Create a ProfilerManager

        ### Args:
        * `print_traces` (`bool`): whether to print the trace of which profiles
          are entered and exited. This has a massive performance impact, but
          can be helpful when debugging crashes in FL Studio's API.
        """
        self._print = print_traces
        # Current profiler node
        self._current: Optional[ProfileNode] = None
        # Current depth of the profiler
        self._depth = 0
        # Name of the longest category
        self._max_name = 0
        # Total times from each profiler
        self._totals: dict[str, float] = {}
        # Number of samples from each profiler
        self._number: dict[str, float] = {}
        # Max times from each profiler
        self._maxes: dict[str, float] = {}

    def __repr__(self) -> str:
        if not len(self._totals):
            return "Profiler (inactive)"
        else:
            total = sum(self._number.values())
            return f"Profiler ({total} profiles taken)"

    def openProfile(self, name: str):
        """
        Open a new profile

        ### Args:
        * `name` (`str`): name of profile to open
        """
        self._depth += 1
        if self._print:
            print("+"*self._depth + name)
        n = ProfileNode(self._current, name)
        if self._current is not None:
            self._current.addChild(n)
        self._current = n

    def closeProfile(self):
        """
        Close the current profile

        ### Raises:
        * `ValueError`: no profile to close
        """
        if self._current is None:
            raise ValueError("No profile to close")
        if self._print:
            print("-"*self._depth + self._current.name)
        self._depth -= 1
        self._current.close()
        parent = self._current.parent
        name = self._getProfileName(self._current)
        t = self._current.getTime() / 1_000_000
        if len(name) > self._max_name:
            self._max_name = len(name)
        if name in self._totals:
            self._totals[name] += t
            self._number[name] += 1
            if self._maxes[name] < t:
                self._maxes[name] = t
        else:
            self._totals[name] = t
            self._number[name] = 1
            self._maxes[name] = t
        self._current = parent

    def inspect(self):
        """
        Inspect details about the profiler
        """
        header = (
            f" {'Name'.ljust(self._max_name)} | Total (ms)     "
            f"| Samples | Ave (ms)   | Max (ms)"
        )
        print()
        print(header)
        print('=' * len(header))
        for (name, total), number, max in zip(
            self._totals.items(), self._number.values(), self._maxes.values()
        ):
            ave = total / number
            print(
                f" {name.ljust(self._max_name)} | {total: 14.5f} | {number:7} "
                f"| {ave: 10.5f} | {max: 10.5f}"
            )
        print()
        return NoneNoPrintout

    def getTotals(self):
        """
        Return a dictionary with the total times for each category
        """
        return self._totals

    def getNumbers(self):
        """
        Return a dictionary with the total times for each category
        """
        return self._number

    def getMaxes(self):
        """
        Return a dictionary with the total times for each category
        """
        return self._maxes
