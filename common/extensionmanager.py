"""
common > extensionmanager

Contains the static class for registering extensions to the script,
including device and plugin definitions.

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]
"""

from typing import TYPE_CHECKING, Optional, overload

from common.types.eventdata import eventData

if TYPE_CHECKING:
    from devices import Device
    from plugs import StandardPlugin, SpecialPlugin

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

# Import devices
from devices.deviceshadow import DeviceShadow
# Import plugins
import plugs
