"""
integrations > plugin > basic_faders

Contains the definition for the basic faders class builder.

FIXME: This is almost definitely not the best place for this code

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""
from typing import Union
from common.types import Color
from common.extension_manager import ExtensionManager
from devices import DeviceShadow
from integrations import PluginIntegration
from integrations.mapping_strategies import (
    SimpleFaders,
    PresetNavigationStrategy,
)


def basicPluginBuilder(
    plugin_names: tuple[str],
    params: list[int],
    color: Union[Color, list[Color]],
    uses_presets: bool = False,
):
    """
    Build and register a basic fader integration

    ### Args:
    * `plugin_names` (`tuple[str]`): the plugin names should be matched

    * `params` (`list[int]`): list of parameter indexes

    * `color` (`Union[Color, list[Color]]`): color or list of colors to use for
      the parameters

    * `uses_presets` (`bool`, optional): whether the plugin uses presets
      (displayed in the top right of the plugin window). Defaults to `False`.
    """
    class BuiltPlugin(PluginIntegration):
        """
        An integration constructed to interact with a certain plugin using the
        given properties
        """

        def __init__(self, shadow: DeviceShadow) -> None:
            SimpleFaders(shadow, params, colors=color)
            if uses_presets:
                PresetNavigationStrategy(shadow)
            super().__init__(shadow)

        @classmethod
        def create(cls, shadow: DeviceShadow) -> 'PluginIntegration':
            return cls(shadow)

        @classmethod
        def getPlugIds(cls) -> tuple[str, ...]:
            return plugin_names

    ExtensionManager.plugins.register(BuiltPlugin)
