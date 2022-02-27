"""
common > profiler > manager

Contains the profiler manager
"""

from typing import Optional
import time

class ProfileNode:
    """
    A node in the profiler

    Manages our position in the profile
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

    def __str__(self) -> str:
        total_time = '<running>' if self._time is None else f"{self._time} ns"
        children = ', '.join([str(c) for c in self._children])
        return f"\"'{self.name}' ({total_time})\":[{children}]"

class ProfilerManager:
    """
    Class for managing profiles
    """
    def __init__(self) -> None:
        self._current: Optional[ProfileNode] = None
    
    def openProfile(self, name: str):
        n = ProfileNode(self._current, name)
        if self._current is not None:
            self._current.addChild(n)
        self._current = n
    
    def closeProfile(self):
        self._current.close()
        if self._current is None:
            raise ValueError("No profile to close")
        parent = self._current.parent
        if parent is None:
            print(self._current)
        self._current = parent
