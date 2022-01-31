"""
common > extensionmanager

Contains the static class for registering extensions to the script,
including device and plugin definitions.

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]
"""

from typing import TYPE_CHECKING, Optional, overload

from common.types.eventdata import eventData
from common.util.consolehelpers import printReturn

if TYPE_CHECKING:
    from devices import Device
    from plugs import StandardPlugin, SpecialPlugin, Plugin

class ExtensionManager:
    """
    Manages all extensions registered with the script, allowing for extensions
    to be used for plugins or devices as required.
    """
    
    # Standard plugins
    _plugins: 'dict[str, type[StandardPlugin]]' = {}
    _instantiated_plugins: 'dict[str, StandardPlugin]' = {}
    
    # Special plugins
    _special_plugins: 'list[type[SpecialPlugin]]' = []
    # Map types to their instance
    _instantiated_special_plugins: 'dict[type[SpecialPlugin], SpecialPlugin]' = {}
    
    _devices: list[type['Device']] = []
    
    def __init__(self) -> None:
        raise TypeError("ExtensionManager is a static class and cannot be instantiated.")

    @classmethod
    def registerPlugin(cls, plugin: type['StandardPlugin']) -> None:
        """
        Register a plugin type

        This should be called after defining the class object for a plugin, so
        that the class can be instantiated if the plugin is in use.

        ### Args:
        * `plugin` (`StandardPlugin`): plugin to register
        
        ### Example Usage
        ```py
        # Create a plugin
        class MyPlugin(StandardPlugin):
            ...
        # Register it
        ExtensionManager.registerPlugin(MyPlugin)
        ```
        
        WARNING: Plugins assume that device definitions don't change over time.
        If the active device changes, or the available controls change, the
        function `resetPlugins()` should be called so that plugins are
        reset to their default state and control bindings are removed.
        """
        cls._plugins[plugin.getPlugId()] = plugin
    
    @classmethod
    def registerSpecialPlugin(cls, plugin: type['SpecialPlugin']) -> None:
        """
        Register a plugin type

        This should be called after defining the class object for a plugin, so
        that the class can be instantiated if the plugin is in use.

        ### Args:
        * `plugin` (`StandardPlugin`): plugin to register
        
        ### Example Usage
        ```py
        # Create a plugin
        class MyPlugin(SpecialPlugin):
            ...
        # Register it
        ExtensionManager.registerPlugin(MyPlugin)
        ```
        
        WARNING: Plugins assume that device definitions don't change over time.
        If the active device changes, or the available controls change, the
        function `resetPlugins()` should be called so that plugins are
        reset to their default state and control bindings are removed.
        """
        cls._special_plugins.append(plugin)

    @classmethod
    def registerDevice(cls, device: type['Device']) -> None:
        """
        Register a device type

        This should be called after defining the class object for a device, so
        that the class can be instantiated if the device is recognised.

        ### Args:
        * `device` (`type`, extends `device`): class to register
        
        ### Example Usage
        ```py
        # Create a device
        class MyDevice(Device):
            ...
        # Register it
        ExtensionManager.registerDevice(MyDevice)
        ```
        """
        cls._devices.append(device)

    @overload
    @classmethod
    def getDevice(cls, arg: eventData) -> 'Device':
        ...
    @overload
    @classmethod
    def getDevice(cls, arg: str) -> 'Device':
        ...
    @classmethod
    def getDevice(cls, arg: 'eventData | str') -> 'Device':
        """
        Returns a new instance of a device, given a universal device enquiry
        response or a device identifier (as a fallback)

        ### Args:
        * `arg` (``eventData | str`): event to match with devices

        ### Raises:
        * `ValueError`: Device not recognised

        ### Returns:
        * `Device`: device object instance
        """
        # Device name
        if isinstance(arg, str):
            for device in cls._devices:
                if device.matchDeviceName(arg):
                    # If it matches the pattern, then we found the right device
                    # create an instance and return it
                    return device.create(None)
        # Sysex event
        # elif isinstance(arg, eventData):
        # Can't runtime type check for MIDI events
        else:
            for device in cls._devices:
                pattern = device.getUniversalEnquiryResponsePattern()
                if pattern is None:
                    pass
                elif pattern.matchEvent(arg):
                    # If it matches the pattern, then we found the right device
                    # create an instance and return it
                    return device.create(arg)
        raise ValueError("Device not recognised")
    
    @classmethod
    def getDeviceById(cls, id: str) -> 'Device':
        """
        Returns a new instance of a device, given a device ID, which should
        match a return value of Device.getId()

        ### Raises:
        * `ValueError`: Device not found

        ### Returns:
        * `Device`: matching device
        """
        for device in cls._devices:
            if device.getId() == id:
                return device.create(None)
        raise ValueError(f"Device with ID {id} not found")

    @classmethod
    def getAllDevices(cls) -> list[type['Device']]:
        return cls._devices
    
    @classmethod
    def getPluginById(cls, id: str, device: 'Device') -> Optional['StandardPlugin']:
        """
        Returns an instance of the standard plugin matching the ID provided.

        If that plugin hasn't been instantiated, the device object will be used
        to create one, enabling lazy loading of plugins to save resources and
        CPU.

        ### Args:
        * `id` (`str`): plugin ID
        * `device` (`Device`): current device

        ### Returns:
        * `StandardPlugin`: plugin associated with ID
        """
        # Plugin already instantiated
        if id in cls._instantiated_plugins.keys():
            return cls._instantiated_plugins[id]
        # Plugin exists but isn't instantiated
        elif id in cls._plugins.keys():
            cls._instantiated_plugins[id] \
                = cls._plugins[id].create(DeviceShadow(device))
            return cls._instantiated_plugins[id]
        # Plugin doesn't exist
        else:
            return None

    @classmethod
    def getSpecialPlugins(cls, device: 'Device') -> list['SpecialPlugin']:
        """
        Returns a list of the special plugins that are currently active and
        should process the event

        If an active plugin hasn't been instantiated, the device object will be
        used to create one.

        ### Args:
        * `device` (`Device`): current device

        ### Returns:
        * `list[SpecialPlugin]`: list of active plugins
        """
        ret: list[SpecialPlugin] = []
        for p in cls._special_plugins:
            # If plugin should be active
            if p.shouldBeActive():
                # If it hasn't been instantiated yet, instantiate it
                if p not in cls._instantiated_special_plugins.keys():
                    cls._instantiated_special_plugins[p] \
                        = p.create(DeviceShadow(device))
                ret.append(cls._instantiated_special_plugins[p])
        
        return ret
    
    @classmethod
    def resetPlugins(cls) -> None:
        """
        Resets all active plugins (standard and special) which can account for
        a device change.
        """
        cls._instantiated_plugins = {}
        cls._instantiated_special_plugins = {}
    
    @classmethod
    def getAllPlugins(cls) -> list[type]:
        return list(cls._plugins.values())
    
    @classmethod
    def getAllSpecialPlugins(cls) -> list[type]:
        return cls._special_plugins
    
    @classmethod
    def getInfo(cls) -> str:
        """
        Returns basic info about the devices and plugins registered with the 
        extension manager

        ### Returns:
        * `str`: info
        """
        num_devs = f"{len(cls._devices)} device{'s' if len(cls._devices) != 1 else ''}"
        num_plugs = f"{len(cls._plugins)} plugin{'s' if len(cls._plugins) != 1 else ''}"
        num_inst_plugs = f" ({len(cls._instantiated_plugins)} instantiated)" if len(cls._instantiated_plugins) else ""
        num_special_plugs =f"{len(cls._special_plugins)} special plugin{'s' if len(cls._special_plugins) != 1 else ''}"
        num_inst_special_plugs = f" ({len(cls._instantiated_special_plugins)} instantiated)" if len(cls._instantiated_special_plugins) else ""
        return f"{num_devs}, {num_plugs}{num_inst_plugs}, {num_special_plugs}{num_inst_special_plugs}"

    @classmethod
    def _formatPlugin(cls, plug: Optional['Plugin']) -> str:
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

    @classmethod
    def _inspectStandardPlugin(cls, plug: type['StandardPlugin']) -> str:
        """
        Returns info about a standard plugin

        ### Args:
        * `plug` (`type[StandardPlugin]`): plugin to inspect

        ### Returns:
        * `str`: plugin info
        """
        matches: list[tuple[str, Optional['StandardPlugin']]] = []
        
        for id, p in cls._plugins.items():
            if p == plug:
                if id in cls._instantiated_plugins.keys():
                    matches.append((id, cls._instantiated_plugins[id]))
                else:
                    matches.append((id, None))

        if len(matches) == 0:
            return f"Plugin {plug} isn't associated with any plugins"
        elif len(matches) == 1:
            id, inst_p = matches[0]
            return f"{plug} associated with:\n{id}\n{cls._formatPlugin(inst_p)}"
        else:
            return f"{plug}:" + f"\n\n".join([
                f"> {id}:\n{cls._formatPlugin(inst_p)}" for id, inst_p in matches
            ])

    @classmethod
    def _inspectPluginId(cls, id: str) -> str:
        """
        Returns info about a standard plugin associated with a plugin ID

        ### Args:
        * `id` (`str`): plugin ID

        ### Returns:
        * `str`: plugin info
        """
        if id in cls._instantiated_plugins.keys():
            return f"{id} associated with:\n\n{repr(cls._instantiated_plugins[id])}"
        elif id in cls._plugins.keys():
            return f"{id} associated with: {cls._plugins[id]} (not instantiated)"
        else:
            return f"ID {id} not associated with any plugins"
    
    @classmethod
    def _inspectSpecialPlugin(cls, plug: type['SpecialPlugin']) -> str:
        """
        Returns info about a special plugin

        ### Args:
        * `plug` (`type[SpecialPlugin]`): plugin to inspect

        ### Returns:
        * `str`: plugin info
        """
        if plug in cls._instantiated_special_plugins.keys():
            return str(cls._instantiated_special_plugins[plug])
        elif plug in cls._special_plugins:
            return f"{plug} is registered but not instantiated"
        else:
            return f"{plug} isn't registered"

    @classmethod
    @printReturn
    def inspectPlugin(cls, plug: 'type["Plugin"] | str') -> str:
        """
        Returns info about a plugin (standard or special)

        ### Args:
        * `plug` (`type[Plugin] | str`): plugin or ID of plugin to inspect

        ### Returns:
        * `str`: plugin info
        """
        if isinstance(plug, str):
            return cls._inspectPluginId(plug)
        elif issubclass(plug, plugs.StandardPlugin):
            return cls._inspectStandardPlugin(plug)
        elif issubclass(plug, plugs.SpecialPlugin):
            return cls._inspectSpecialPlugin(plug)
        else:
            return f"{plug} isn't a Plugin class or plugin ID"

# Import devices
from devices.deviceshadow import DeviceShadow
# Import plugins
import plugs
