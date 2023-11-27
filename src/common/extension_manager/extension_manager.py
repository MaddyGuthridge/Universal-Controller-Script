"""
common > extension_manager > extension_manager

Contains the static class for registering extensions to the script, including
device and plugin definitions.

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""

from typing import TYPE_CHECKING
from common.util.console_helpers import printReturn

if TYPE_CHECKING:
    from devices import Device
    from integrations import Integration

from .standard_plugs import StandardPluginCollection
from .special_plugs import SpecialPluginCollection
from .window_plugs import WindowPluginCollection
from .devices import DeviceCollection


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
    """Contains standard plugins
    """

    # Window plugins
    windows = WindowPluginCollection()
    """Contains plugins that handle FL Studio windows
    """

    # Special plugins
    special = SpecialPluginCollection()
    """Special plugins are plugins that can be active at any time they specify
    """

    # Final special plugins
    super_special = SpecialPluginCollection()
    """Super special plugins process events first and draw lights last, meaning
    that they get the first opportunity to process events, and the final say on
    lighting behavior.
    """

    # Devices
    devices = DeviceCollection()
    """Hardware device definitions
    """

    def __init__(self) -> None:
        raise TypeError(
            "ExtensionManager is a static class and cannot be instantiated."
        )

    @classmethod
    def resetPlugins(cls) -> None:
        """
        Resets all active plugins (standard and special) which can account for
        a device change.
        """
        cls.plugins.reset()
        cls.windows.reset()
        cls.special.reset()
        cls.super_special.reset()

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
        n_dev = f"{len(cls.devices)} device{plural(cls.devices)}"
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
        nfs_plug = f"{len(cls.super_special)} "\
            f"final special plugin{plural(cls.super_special)}"
        # Number of instantiated final special plugins
        nifs_plug = instantiated(cls.super_special)
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

        # Number of devices
        n_dev = len(cls.devices)
        # Number of plugins
        n_plug = (
            len(cls.plugins) + len(cls.windows)
            + len(cls.special) + len(cls.super_special)
        )
        return (
            f"{n_dev} devices, {n_plug} plugins"
        )

    @classmethod
    @printReturn
    def inspect(cls, ext: 'type[Device] | type[Integration] | str') -> str:
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
        import integrations
        if isinstance(ext, str):
            return cls.plugins.inspect(ext)
        elif issubclass(ext, devices.Device):
            return cls.devices.inspect(ext)
        elif issubclass(ext, integrations.PluginIntegration):
            return cls.plugins.inspect(ext)
        elif issubclass(ext, integrations.WindowIntegration):
            return cls.windows.inspect(ext)
        elif issubclass(ext, integrations.CoreIntegration):
            # FIXME: Final plugins can't be inspected
            return cls.special.inspect(ext)
        else:
            return f"{ext} isn't a Plugin class or plugin ID"
