
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from plugs import SpecialPlugin
    from devices import Device


class SpecialPluginCollection:
    def __init__(self) -> None:
        self.__types: list[type['SpecialPlugin']] = []
        self.__instantiated: dict[type['SpecialPlugin'], 'SpecialPlugin'] = {}

    def register(self, plug: type['SpecialPlugin']) -> None:
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

    def get(self, device: 'Device') -> list['SpecialPlugin']:
        """Get a list of all the active special plugins
        """
        from devices.deviceshadow import DeviceShadow
        ret: list[SpecialPlugin] = []
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

    def all(self) -> list[type['SpecialPlugin']]:
        return list(self.__types)

    def instantiated(self) -> list['SpecialPlugin']:
        return list(self.__instantiated.values())

    def __len__(self) -> int:
        return len(self.__types)

    def __contains__(self, other: type['SpecialPlugin']) -> bool:
        return other in self.__types

    def inspect(self, plug: type['SpecialPlugin']) -> str:
        if plug in self.__instantiated.keys():
            return str(self.__instantiated[plug])
        elif plug in self.__types:
            return f"{plug} (Not instantiated)"
        else:
            return f"{plug} isn't registered"
