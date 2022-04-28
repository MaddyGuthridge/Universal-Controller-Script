"""
controlsurfaces > activity

Defines control surfaces used for managing the active plugin

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]
"""

__all__ = [
    'ActivityButton',
    'SwitchActiveButton',
    'SwitchActivePluginButton',
    'SwitchActiveWindowButton',
    'SwitchActiveToggleButton',
    'PauseActiveButton',
]

from common.eventpattern.ieventpattern import IEventPattern
from controlsurfaces.valuestrategies.ivaluestrategy import IValueStrategy
from controlsurfaces import Button


class ActivityButton(Button):
    """
    Macro buttons are buttons that should be assigned to a particular function
    in FL Studio.
    """


class SwitchActiveButton(ActivityButton):
    """
    Defines a switch active button, which is handled internally to switch
    event handling between the active plugin and the active window.

    Using this type of control will cause an error unless the device calls
    `getContext().activity.setSplitWindowsPlugins(self, value: bool)`
    in order to inform the script context that windows and plugins should be
    addressed independently.

    This is the abstract base class: to implement this, use
    * `SwitchActivePluginButton` for a button to switch to plugins
    * `SwitchActiveWindowButton` for a button to switch to windows
    * `SwitchActiveToggleButton` for a button to toggle between windows and
      plugins
    """

    def __init__(
        self,
        event_pattern: IEventPattern,
        value_strategy: IValueStrategy
    ) -> None:
        super().__init__(event_pattern, value_strategy)


class SwitchActivePluginButton(SwitchActiveButton):
    """
    A switch active button that makes generator and effects plugins be actively
    processed by the script.
    """


class SwitchActiveWindowButton(SwitchActiveButton):
    """
    A switch active button that makes FL Studio windows be actively
    processed by the script.
    """


class SwitchActiveToggleButton(SwitchActiveButton):
    """
    A switch active button that toggles between plugins and FL Studio windows
    being actively processed by the script.
    """


class PauseActiveButton(ActivityButton):
    """
    A pause active button that pauses the updating of the active plugin,
    allowing users to keep their parameters mapped to the currently selected
    plugin, even if they choose a new plugin.
    """
    def __init__(
        self,
        event_pattern: IEventPattern,
        value_strategy: IValueStrategy
    ) -> None:
        super().__init__(event_pattern, value_strategy)
