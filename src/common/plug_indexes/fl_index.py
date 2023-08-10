"""
common > plug_indexes > fl_index

Definition for FlIndex abstract base class

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""
from abc import abstractmethod
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from .window import WindowIndex
    from .plugin import PluginIndex


class FlIndex:
    """
    Represents an index to a plugin or window in FL Studio
    """
    @abstractmethod
    def getName(self) -> str:
        """
        Returns the name of the plugin/window at the given index
        """
        ...

    @abstractmethod
    def focus(self) -> None:
        """
        Focus the plugin or window, bringing its UI to the front.
        """
        ...

    def asWindowIndex(self) -> 'WindowIndex':
        """
        Cast this to a WindowIndex

        Raises an error if the index was not a WindowIndex

        ### Raises:
        * `TypeError`: type cast failed

        ### Returns:
        * `WindowIndex`: this index, but now guaranteed to be a WindowIndex
        """
        from .window import WindowIndex
        if isinstance(self, WindowIndex):
            return self
        raise TypeError(f'Cannot cast to WindowIndex, type is {self}')

    def asPluginIndex(self) -> 'PluginIndex':
        """
        Cast this to a PluginIndex

        Raises an error if the index was not a PluginIndex

        ### Raises:
        * `TypeError`: type cast failed

        ### Returns:
        * `PluginIndex`: this index, but now guaranteed to be a PluginIndex
        """
        from .plugin import PluginIndex
        if isinstance(self, PluginIndex):
            return self
        raise TypeError(f'Cannot cast to PluginIndex, type is {self}')
