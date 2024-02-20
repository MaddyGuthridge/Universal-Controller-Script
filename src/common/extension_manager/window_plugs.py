"""
common > extension_manager > window_plugs

Contains the definition for the WindowPluginCollection class

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""

from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from integrations import WindowIntegration
    from devices import Device
    from common.plug_indexes.fl_index import WindowIndex


class WindowPluginCollection:
    """Collection of window plugins registered to the script
    """
    def __init__(self) -> None:
        self.__mappings: dict[WindowIndex, type['WindowIntegration']] = {}
        self.__instantiated: dict[WindowIndex, 'WindowIntegration'] = {}

    def register(self, plug: type['WindowIntegration']) -> None:
        """
        Register a window plugin

        This should be called after defining the class object for a plugin, so
        that the class can be instantiated if the plugin is in use.

        ### Args:
        * `plug` (`type[WindowPlugin]`): plugin to register

        ### Example Usage
        ```py
        # Create a plugin
        class MyPlugin(WindowPlugin):
            ...
        # Register it
        ExtensionManager.windows.register(MyPlugin)
        ```
        """
        self.__mappings[plug.getWindowId()] = plug

    def get(
        self,
        id: 'WindowIndex',
        device: 'Device'
    ) -> Optional['WindowIntegration']:
        """Get an instance of the plugin matching this window index
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
            # log(
            #     "extensions.manager",
            #     f"No plugins associated with plugin ID '{id}'",
            #     verbosity=verbosity.NOTE
            # )
            return None

    def reset(self) -> None:
        self.__instantiated = {}

    def all(self) -> list[type['WindowIntegration']]:
        return list(self.__mappings.values())

    def instantiated(self) -> list['WindowIntegration']:
        return list(self.__instantiated.values())

    def __len__(self) -> int:
        return len(self.__mappings)

    def _formatPlugin(cls, plug: Optional['WindowIntegration']) -> str:
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

    def inspect(self, plug: type['WindowIntegration']) -> str:
        """
        Returns info about a window plugin

        ### Args:
        * `plug` (`type[WindowPlugin]`): plugin to inspect

        ### Returns:
        * `str`: plugin info
        """
        matches: list[tuple['WindowIndex', Optional['WindowIntegration']]] = []

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
