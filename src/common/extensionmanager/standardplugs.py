
from typing import TYPE_CHECKING, Optional


if TYPE_CHECKING:
    from plugs import StandardPlugin
    from devices import Device


class StandardPluginCollection:
    def __init__(self) -> None:
        self.__mappings: dict[str, type['StandardPlugin']] = {}
        self.__instantiated: dict[str, 'StandardPlugin'] = {}

    def register(self, plug: type['StandardPlugin']) -> None:
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

    def get(self, id: str, device: 'Device') -> Optional['StandardPlugin']:
        """Get an instance of the plugin matching this plugin id
        """
        from devices.deviceshadow import DeviceShadow
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

    def all(self) -> list[type['StandardPlugin']]:
        return list(self.__mappings.values())

    def instantiated(self) -> list['StandardPlugin']:
        return list(self.__instantiated.values())

    def __len__(self) -> int:
        return len(self.__mappings)

    def _formatPlugin(cls, plug: Optional['StandardPlugin']) -> str:
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

    def inspect(self, plug: 'type[StandardPlugin] | str') -> str:
        if isinstance(plug, str):
            return self._inspect_id(plug)
        else:
            return self._inspect_plug(plug)

    def _inspect_plug(self, plug: 'type[StandardPlugin]') -> str:
        matches: list[tuple[str, Optional['StandardPlugin']]] = []

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
