"""
plugs > standard > basic_faders

Contains the definition for the basic faders class builder

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""
from typing import Union
from common.types import Color
from common.extension_manager import ExtensionManager
from devices import DeviceShadow
from plugs import StandardPlugin
from plugs.mapping_strategies import SimpleFaders


def basicPluginBuilder(
    plugin_names: tuple[str],
    params: list[int],
    color: Union[Color, list[Color]],
):
    """
    Build and register a basic fader plugin

    ### Args:
    * `plugin_names` (`tuple[str]`): the plugin names should be matched

    * `params` (`list[int]`): list of parameter indexes

    * `color` (`Union[Color, list[Color]]`): color or list of colors to use for
      the parameters
    """
    class BuiltPlugin(StandardPlugin):
        """
        A plugin constructed to interact with a certain plugin using the given
        properties
        """

        def __init__(self, shadow: DeviceShadow) -> None:
            faders = SimpleFaders(params, colors=color)
            super().__init__(shadow, [faders])

        @classmethod
        def create(cls, shadow: DeviceShadow) -> 'StandardPlugin':
            return cls(shadow)

        @classmethod
        def getPlugIds(cls) -> tuple[str, ...]:
            return plugin_names

    ExtensionManager.plugins.register(BuiltPlugin)
