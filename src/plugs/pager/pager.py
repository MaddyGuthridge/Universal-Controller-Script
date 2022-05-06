
from typing import Any
from common.types import Color
from common.util.apifixes import UnsafeIndex
from controlsurfaces import ControlEvent, ControlSwitchButton
from controlsurfaces.controlmapping import ControlShadowEvent
from devices import DeviceShadow
from plugs import Plugin
from plugs.eventfilters.filters import filterButtonLift


class PluginPager:
    """
    A class that facilitates creating multiple pages for plugins, each with
    different behaviour.

    To implement a PluginPager, you should use multiple inheritance, with this
    being the first class to inherit from.

    TODO: Example usage

    Note that the central plugin will always be transparent, so that it won't
    interfere with how values are applied from various pages.
    """

    def __init__(self, shadow: DeviceShadow) -> None:
        # PluginPagers are always transparent, so that they won't interfere
        # with the pages
        shadow.setTransparent(True)
        self.__shadow = shadow
        self.__controlSwitch = shadow.bindMatch(ControlSwitchButton,
                                                self.controlSwitch)
        self.__pages: list[Plugin] = []
        self.__page_colors: list[Color] = []
        self.__index: int = 0
        self.__needs_update = True

    def addPage(self, new: Plugin, color: Color) -> None:
        """
        Add a page to this plugin

        ### Args:
        * `new` (`Page`): page to add
        """
        self.__pages.append(new)
        self.__page_colors.append(color)

    def nextPage(self) -> None:
        """
        Jump to the next page of the plugin pager
        """
        self.__index += 1
        if self.__index == len(self.__pages):
            self.__index = 0
        self.__needs_update = True

    def processEvent(self, mapping: ControlEvent, index: UnsafeIndex) -> bool:
        """Secret override of the processEvent method for the Plugin class
        """
        # Process events for the main plugin first
        if self.__shadow.processEvent(mapping, index):
            return True

        if not len(self.__pages):
            raise ValueError(f"No pages added for PluginPager {type(self)}")
        # Process the event in the required page
        return self.__pages[self.__index].processEvent(mapping, index)

    @filterButtonLift
    def controlSwitch(
        self,
        control: ControlShadowEvent,
        index: UnsafeIndex,
        *args: Any
    ) -> bool:
        """Switch between pages"""
        if control.value:
            self.nextPage()
        return True

    def tick(self, *args, **kwargs) -> None:
        """Secret override of the tick method for the Plugin class
        Since different types of plugins take different arguments for the
        method, we need to use generic args and kwargs.
        """
        if not len(self.__pages):
            raise ValueError(f"No pages added for PluginPager {type(self)}")

        # Set color of the control switch to the color of the current page
        if self.__controlSwitch is not None:
            self.__controlSwitch.color = self.__page_colors[self.__index]

        # Now tick the page
        # Ignore type since this function does exist for all subclasses
        self.__pages[self.__index].tick(*args, **kwargs)  # type: ignore

    def apply(self, thorough: bool) -> None:
        """Secret override of the apply method for the Plugin class
        """
        if not self.__needs_update:
            self.__pages[self.__index].apply(thorough)
        else:
            self.__pages[self.__index].apply(True)
            self.__needs_update = False
        # Apply the main one last so that it overrides any other controls
        self.__shadow.apply(thorough)
