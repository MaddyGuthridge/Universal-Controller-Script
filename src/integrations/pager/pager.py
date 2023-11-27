"""
integrations > pager > pager

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""
from typing import Any
from common.types import Color
from common.plug_indexes.fl_index import FlIndex
from control_surfaces import ControlEvent, ControlSwitchButton
from control_surfaces.control_mapping import ControlShadowEvent
from devices import DeviceShadow
from integrations import Integration
from integrations.event_filters.filters import filterButtonLift


class IntegrationPager:
    """
    A class that facilitates creating multiple pages for plugins, each with
    different behavior.

    To implement a PluginPager, you should use multiple inheritance, with this
    being the first class to inherit from.

    Note that the central plugin will always be transparent, so that it won't
    interfere with how values are applied from various pages.

    ## Methods

    * `addPage(self, page: Plugin) -> None`: add a page to the pager

    * `nextPage(self) -> None`: jump to the next page

    ## Example Usage

    ```py
    # Define pages
    class MyPage1(StandardPlugin):
        # Each page is created exactly like a standard plugin
        ...
    class MyPage2(StandardPlugin):
        ...

    # Create our pager plugin
    # We use multiple inheritance to add the pager properties to our plugin
    class MyPlugin(PluginPager, StandardPlugin):
        def __init__(self, shadow: DeviceShadow) -> None:
            # Initialize the pager
            PluginPager.__init__(self, shadow)

            # Add pages to the pager
            # We should create a copy of the device shadow to give to each
            # page, and register a color to use with the page, which will be
            # displayed on the control switch button
            self.addPage(MyPage1(shadow.copy()), Color.fromInteger(0xFF00AA))
            self.addPage(MyPage2(shadow.copy()), Color.fromInteger(0xAA00FF))

            # Add any other required controls that should be bound universally
            shadow.bindMatches(...)

            # Initialize the main plugin
            StandardPlugin.__init__(self, shadow, [])
    ```
    """

    def __init__(self, shadow: DeviceShadow) -> None:
        """
        Create a PluginPager

        ### Args:
        * `shadow` (`DeviceShadow`): device shadow to work with
        """
        self.__shadow = shadow
        self.__controlSwitch = shadow.bindMatch(ControlSwitchButton,
                                                self.controlSwitch)
        self.__pages: list[Integration] = []
        self.__page_colors: list[Color] = []
        self.__index: int = 0
        self.__needs_update = True

    def addPage(self, new: Integration, color: Color) -> None:
        """
        Add a page to this plugin

        ### Args:
        * `new` (`Plugin`): page to add. This should be a plugin of the same
          type as the plugin providing the page.
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

    def processEvent(self, mapping: ControlEvent, index: FlIndex) -> bool:
        """Secret override of the processEvent method for the Plugin class
        """
        # Process events for the main plugin first
        if self.__shadow.processEvent(mapping, index):
            return True

        if not len(self.__pages):
            raise ValueError(f"No pages added for PluginPager {type(self)}")
        # Process the event in the required page
        return self.__pages[self.__index].processEvent(mapping, index)

    @filterButtonLift()
    def controlSwitch(
        self,
        control: ControlShadowEvent,
        index: FlIndex,
        *args: Any
    ) -> bool:
        """Switch between pages"""
        if control.value:
            self.nextPage()
        return True

    def tick(self, index: FlIndex) -> None:
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
        self.__pages[self.__index].doTick(index)

        # Tick the main one last so that it overrides any other controls
        self.__shadow.tick(index)

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
