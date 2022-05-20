"""
common > extensionmanager

Contains the static class for registering extensions to the script,
including device and plugin definitions.

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]
"""

from typing import TYPE_CHECKING, Optional, overload

from common.exceptions import DeviceRecogniseError
from common.types.eventdata import EventData
from common.util.consolehelpers import printReturn

if TYPE_CHECKING:
    from devices import Device
    from plugs import Plugin

from .standardplugs import StandardPluginCollection
from .specialplugs import SpecialPluginCollection
from .windowplugs import WindowPluginCollection


# TODO: Clean up this awfulness - so much repeated code
class ExtensionManager:
    """
    Manages all extensions registered with the script, allowing for extensions
    to be used for plugins or devices as required.

    WARNING: Plugins assume that device definitions don't change over time.
    If the active device changes, or the available controls change, the
    function `resetPlugins()` should be called so that plugins are
    reset to their default state and control bindings are removed.
    """

    # Standard plugins
    plugins = StandardPluginCollection()

    # Window plugins
    windows = WindowPluginCollection()

    # Special plugins
    special = SpecialPluginCollection()

    # Final special plugins
    final = SpecialPluginCollection()

    _devices: list[type['Device']] = []

    def __init__(self) -> None:
        raise TypeError(
            "ExtensionManager is a static class and cannot be instantiated."
        )

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
    def getDevice(cls, arg: EventData) -> 'Device':
        ...

    @overload
    @classmethod
    def getDevice(cls, arg: str) -> 'Device':
        ...

    @classmethod
    def getDevice(cls, arg: 'EventData | str') -> 'Device':
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
        raise DeviceRecogniseError("Device not recognised")

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
            if device.__name__ == id:
                return device.create(None)
        raise DeviceRecogniseError(f"Device with ID {id} not found")

    @classmethod
    def getAllDevices(cls) -> list[type['Device']]:
        """
        Returns a list of all devices that have been registered
        """
        return cls._devices

    @classmethod
    def resetPlugins(cls) -> None:
        """
        Resets all active plugins (standard and special) which can account for
        a device change.
        """
        cls.plugins.reset()
        cls.windows.reset()
        cls.special.reset()
        cls.final.reset()

    @classmethod
    def getInfo(cls) -> str:
        """
        Returns more detailed info about the devices and plugins registered
        with the extension manager

        ### Returns:
        * `str`: info
        """
        def plural(obj) -> str:
            return 's' if len(obj) != 1 else ''

        def instantiated(obj) -> str:
            return f" ({len(obj)} instantiated)" if len(obj) else ""

        # Number of devices
        n_dev = f"{len(cls._devices)} device{plural(cls._devices)}"
        # Number of plugins
        n_plug = f"{len(cls.plugins)} plugin{plural(cls.plugins)}"
        # Number of instantiated plugins
        ni_plug = instantiated(cls.plugins.instantiated())
        # Number of windows
        n_wind = f"{len(cls.windows)} window plugin{plural(cls.windows)}"
        # Number of instantiated windows
        ni_wind = instantiated(cls.windows.instantiated())
        # Number of special plugins
        ns_plug = f"{len(cls.special)} "\
            f"special plugin{plural(cls.special)}"
        # Number of instantiated special plugins
        nis_plug = instantiated(cls.special.instantiated())
        # Number of final special plugins
        nfs_plug = f"{len(cls.final)} "\
            f"final special plugin{plural(cls.final)}"
        # Number of instantiated final special plugins
        nifs_plug = instantiated(cls.final)
        # Compile all that info into one string
        return (
            f"{n_dev}, "
            f"{n_plug}{ni_plug}, "
            f"{n_wind}{ni_wind}, "
            f"{ns_plug}{nis_plug}, "
            f"{nfs_plug}{nifs_plug}"
        )

    @classmethod
    def getBasicInfo(cls) -> str:
        """
        Returns basic info about the devices and plugins registered with the
        extension manager

        ### Returns:
        * `str`: info
        """
        def plural(obj) -> str:
            return 's' if len(obj) != 1 else ''

        def instantiated(obj) -> str:
            return f" ({len(obj)} instantiated)" if len(obj) else ""

        # Number of devices
        n_dev = f"{len(cls._devices)} device{plural(cls._devices)}"
        # Number of plugins
        n_plug = (
            len(cls.plugins) + len(cls.windows)
            + len(cls.special) + len(cls.final)
        )
        # Number of instantiated plugins
        n_inst = (
            len(cls.plugins.instantiated()) + len(cls.windows.instantiated())
            + len(cls.special.instantiated()) + len(cls.final.instantiated())
        )
        return (
            f"{n_dev} devices, "
            f"{n_plug} plugins ({n_inst} instantiated)"
        )

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
    def _inspectDevice(cls, dev: type['Device']) -> str:
        """
        Returns info about a device

        ### Args:
        * `dev` (`type[Device]`): device to inspect

        ### Returns:
        * `str`: device info
        """
        if dev in cls._devices:
            return f"{dev} (registered)"
        else:
            return f"{dev} (not registered)"

    @classmethod
    @printReturn
    def inspect(cls, ext: 'type[Device] | type[Plugin] | str') -> str:
        """
        Returns info about an extension, which can be a device or a plugin of
        any kind

        ### Args:
        * `ext` (`type[Plugin] | type[Plugin] | str`): device, plugin or
          plugin ID to inspect

        ### Returns:
        * `str`: extension info
        """
        import devices
        import plugs
        if isinstance(ext, str):
            return cls.plugins.inspect(ext)
        elif issubclass(ext, devices.Device):
            return cls._inspectDevice(ext)
        elif issubclass(ext, plugs.StandardPlugin):
            return cls.plugins.inspect(ext)
        elif issubclass(ext, plugs.WindowPlugin):
            return cls.windows.inspect(ext)
        elif issubclass(ext, plugs.SpecialPlugin):
            # FIXME: Final plugins can't be inspected
            return cls.special.inspect(ext)
        else:
            return f"{ext} isn't a Plugin class or plugin ID"
