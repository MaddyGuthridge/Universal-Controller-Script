"""
common > extension_manager > standard_plugs

Contains the definition for the StandardPluginCollection class

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""

from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from integrations import PluginIntegration
    from devices import Device


class StandardPluginCollection:
    """Collection of standard plugins registered to the script
    """
    def __init__(self) -> None:
        self.__mappings: dict[str, type['PluginIntegration']] = {}
        self.__instantiated: dict[str, 'PluginIntegration'] = {}
        self.__fallback: Optional[type['PluginIntegration']] = None
        self.__fallback_inst: Optional['PluginIntegration'] = None

    def register(self, plug: type['PluginIntegration']) -> None:
        """
        Register a standard plugin

        This should be called after defining the class object for a plugin, so
        that the class can be instantiated if the plugin is in use.

        ### Args:
        * `plug` (`type[StandardPlugin]`): plugin to register

        ### Example Usage
        ```py
        # Create a plugin
        class MyPlugin(StandardPlugin):
            ...
        # Register it
        ExtensionManager.plugins.register(MyPlugin)
        ```
        """
        for plug_id in plug.getPlugIds():
            self.__mappings[plug_id] = plug

    def registerFallback(self, plug: type['PluginIntegration']) -> None:
        """
        Register a plugin to be used as a fallback when the default bindings
        fail

        If a matching plugin isn't found, the fallback plugin is returned.

        ### Args:
        * `plug` (`type[StandardPlugin]`): plugin to register
        """
        self.__fallback = plug

    def get(self, id: str, device: 'Device') -> Optional['PluginIntegration']:
        """Get an instance of the plugin matching this plugin id
        """
        from devices.device_shadow import DeviceShadow
        # Plugin already instantiated
        if id in self.__instantiated.keys():
            return self.__instantiated[id]
        # Plugin exists but isn't instantiated
        elif id in self.__mappings.keys():
            self.__instantiated[id] \
                = self.__mappings[id].create(DeviceShadow(device))
            return self.__instantiated[id]
        # Plugin doesn't exist
        else:
            if self.__fallback_inst is None:
                if self.__fallback is None:
                    return None
                else:
                    self.__fallback_inst \
                        = self.__fallback.create(DeviceShadow(device))
            return self.__fallback_inst

    def getFallback(self) -> Optional['PluginIntegration']:
        """Return the fallback plugin if registered
        """
        return self.__fallback_inst

    def reset(self) -> None:
        self.__instantiated = {}
        self.__fallback_inst = None

    def all(self) -> list[type['PluginIntegration']]:
        return list(self.__mappings.values())

    def instantiated(self) -> list['PluginIntegration']:
        return list(self.__instantiated.values())

    def __len__(self) -> int:
        return len(self.__mappings)

    def _formatPlugin(cls, plug: Optional['PluginIntegration']) -> str:
        """
        Format info about a plugin instance

        ### Args:
        * `plug` (`Optional[Plugin]`): plugin instance or None

        ### Returns:
        * `str`: formatted info
        """
        if plug is None:
            return "(Not instantiated)"
        else:
            return repr(plug)

    def inspect(self, plug: 'type[PluginIntegration] | str') -> str:
        if isinstance(plug, str):
            return self._inspect_id(plug)
        else:
            return self._inspect_plug(plug)

    def _inspect_plug(self, plug: 'type[PluginIntegration]') -> str:
        matches: list[tuple[str, Optional['PluginIntegration']]] = []

        for id, p in self.__mappings.items():
            if p == plug:
                if id in self.__instantiated.keys():
                    matches.append((id, self.__instantiated[id]))
                else:
                    matches.append((id, None))

        if len(matches) == 0:
            return f"Plugin {plug} isn't associated with any plugins"
        elif len(matches) == 1:
            id, inst_p = matches[0]
            return (
                f"{plug} associated with:\n{id}\n"
                f"{self._formatPlugin(inst_p)}"
            )
        else:
            return f"{plug}:" + "\n\n".join([
                f"> {id}:\n{self._formatPlugin(inst_p)}"
                for id, inst_p in matches
            ])

    def _inspect_id(self, id: str) -> str:
        if id in self.__instantiated.keys():
            return f"{id} associated with:\n\n{self.__instantiated[id]}"
        elif id in self.__mappings.keys():
            return f"{id} associated with: {self.__mappings[id]} "\
                    "(not instantiated)"
        else:
            return f"ID {id} not associated with any plugins"
