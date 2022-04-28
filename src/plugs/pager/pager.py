
from common.util.apifixes import UnsafeIndex
from controlsurfaces import ControlEvent, ControlSwitchButton
from plugs import Plugin


class PluginPager:
    """
    A class that facilitates creating multiple pages for plugins, each with
    different behaviour.

    To implement a PluginPager, you should use multiple inheritance, with this
    being the first class to inherit from.

    TODO: Example usage
    """

    def __init__(self) -> None:
        self.__pages: list[Plugin] = []
        self.__index: int = 0

    def addPage(self, new: Plugin) -> None:
        """
        Add a page to this plugin

        ### Args:
        * `new` (`Page`): page to add
        """
        self.__pages.append(new)

    def nextPage(self) -> None:
        """
        Jump to the next page of the plugin pager
        """
        self.__index += 1
        if self.__index == len(self.__pages):
            self.__index = 0

    def processEvent(self, mapping: ControlEvent, index: UnsafeIndex) -> bool:
        """Secret override of the processEvent method for the Plugin class
        """
        if not len(self.__pages):
            raise ValueError(f"No pages added for PluginPager {type(self)}")
        # Check to see if we need to switch to the next page
        if isinstance(mapping.getControl(), ControlSwitchButton):
            if mapping.value:
                self.nextPage()
            return True
        # Process the event in the required page
        return self.__pages[self.__index].processEvent(mapping, index)

    def tick(self, *args, **kwargs) -> None:
        """Secret override of the tick method for the Plugin class
        Since different types of plugins take different arguments for the
        method, we need to use generic args and kwargs.
        """
        if not len(self.__pages):
            raise ValueError(f"No pages added for PluginPager {type(self)}")
        # Ignore type since this function does exist for all subclasses
        self.__pages[self.__index].tick(*args, **kwargs)  # type: ignore

    def apply(self, thorough: bool) -> None:
        """Secret override of the apply method for the Plugin class
        """
        self.__pages[self.__index].apply(thorough)
