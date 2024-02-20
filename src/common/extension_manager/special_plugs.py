"""
common > extension_manager > special_plugs

Contains the definition for the SpecialPluginCollection class

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from integrations import CoreIntegration
    from devices import Device


class SpecialPluginCollection:
    """Collection of special plugins registered to the script.
    """
    def __init__(self) -> None:
        self.__types: list[type['CoreIntegration']] = []
        self.__instantiated: dict[type['CoreIntegration'], 'CoreIntegration']\
            = {}

    def register(self, plug: type['CoreIntegration']) -> None:
        """
        Register a special plugin

        This should be called after defining the class object for a plugin, so
        that the class can be instantiated if the plugin is in use.

        ### Args:
        * `plug` (`type[SpecialPlugin]`): plugin to register

        ### Example Usage
        ```py
        # Create a plugin
        class MyPlugin(SpecialPlugin):
            ...
        # Register it
        ExtensionManager.special.register(MyPlugin)
        # Or register it as a final processor
        ExtensionManager.final.register(MyPlugin)
        ```
        """
        self.__types.append(plug)

    def get(self, device: 'Device') -> list['CoreIntegration']:
        """Get a list of all the active special plugins
        """
        from devices.device_shadow import DeviceShadow
        ret: list[CoreIntegration] = []
        for p in self.__types:
            # If plugin should be active
            if p.shouldBeActive():
                # If it hasn't been instantiated yet, instantiate it
                if p not in self.__instantiated.keys():
                    self.__instantiated[p] = p.create(DeviceShadow(device))
                ret.append(self.__instantiated[p])
        return ret

    def reset(self) -> None:
        self.__instantiated = {}

    def all(self) -> list[type['CoreIntegration']]:
        return list(self.__types)

    def instantiated(self) -> list['CoreIntegration']:
        return list(self.__instantiated.values())

    def __len__(self) -> int:
        return len(self.__types)

    def __contains__(self, other: type['CoreIntegration']) -> bool:
        return other in self.__types

    def inspect(self, plug: type['CoreIntegration']) -> str:
        if plug in self.__instantiated.keys():
            return str(self.__instantiated[plug])
        elif plug in self.__types:
            return f"{plug} (Not instantiated)"
        else:
            return f"{plug} isn't registered"
