"""
common > activitystate

Contains the definition for the ActivityState class which manages what plugin
or window should be active.

Authors:
* Miguel Guthridge [hdsq@outlook.com, HDSQ#2154]
"""

from common.profiler import profilerDecoration
from common.logger import log, verbosity
from common.plug_indexes import (
    PluginIndex,
    UnsafeIndex,
    GeneratorIndex,
    EffectIndex,
    WindowIndex,
)
from common.util.api_fixes import (
    getFocusedPluginIndex,
    getFocusedWindowIndex,
    reset_generator_active,
)


class ActivityState:
    """
    Maintains the currently selected plugin or window
    """

    def __init__(self) -> None:
        """
        Create an ActivityState object
        """
        self._doUpdate = True
        self._split = False
        self._window: WindowIndex = 0
        self._generator: GeneratorIndex = (0,)
        self._effect: EffectIndex = (0, 0)
        self._plugin: PluginIndex = self._generator
        self._plug_active = True if self._plugin is not None else False
        self._changed = False
        self._plug_unsafe = False

    def inspect(self):
        """
        Inspect details about the activity state.
        """
        print(f"Window: {self._window}, Plugin: {self._plugin}")
        print(f"Active: {'plugin' if self._plug_active else 'window'}")
        print(f"Updating: {self._doUpdate}")
        print(f"Split: {self._split}")
        return ''

    def _forcePlugUpdate(self) -> None:
        """
        Update the active plugin when other things are active (eg windows).
        Used so that split windows and plugins behaves correctly.
        """
        plugin = getFocusedPluginIndex(force=True)
        if plugin is None:
            if not self._plug_unsafe:
                log(
                    "state.active",
                    "Using plugin not from selected channel rack group",
                    verbosity.WARNING
                )
                self._plug_unsafe = True
                self._plugin = (-1,)
                self._generator = (-1,)
            return
        self._plugin = plugin
        if len(plugin) == 1:
            self._generator = plugin  # type: ignore
        else:
            self._effect = plugin  # type: ignore

    @profilerDecoration("activity.tick")
    def tick(self) -> None:
        """
        Called frequently when we need to update the current window
        """
        # HACK: Fix FL Studio bugs
        reset_generator_active()
        self._changed = False
        if self._doUpdate:
            # Manually update plugin using selection
            if (window := getFocusedWindowIndex()) is not None:
                if window != self._window:
                    self._changed = True
                self._window = window
                if not self._split:
                    if self._plug_active:
                        self._changed = True
                    self._plug_active = False
                self._forcePlugUpdate()
            elif (plugin := getFocusedPluginIndex()) is not None:
                self._plug_unsafe = False
                if plugin != self._plugin:
                    self._changed = True
                self._plugin = plugin
                # Ignore typing because len(plugin) doesn't narrow types in
                # mypy
                if len(plugin) == 1:
                    self._generator = plugin  # type: ignore
                else:
                    self._effect = plugin  # type: ignore
                if not self._split:
                    if not self._plug_active:
                        self._changed = True
                    self._plug_active = True
            else:
                self._forcePlugUpdate()

    def hasChanged(self) -> bool:
        """
        Returns whether the active plugin has changed in the last tick

        ### Returns:
        * `bool`: whether the active plugin changed
        """
        return self._changed

    def getActive(self) -> UnsafeIndex:
        """
        Returns the currently active window or plugin
        """
        if self._plug_active:
            return self._plugin
        else:
            return self._window

    def getGenerator(self) -> GeneratorIndex:
        """
        Returns the currently active generator plugin

        ### Returns:
        * `GeneratorIndex`: active generator
        """
        return self._generator

    def getEffect(self) -> EffectIndex:
        """
        Returns the currently active effect plugin

        ### Returns:
        * `GeneratorIndex`: active generator
        """
        return self._effect

    def getPlugin(self) -> PluginIndex:
        """
        Returns the currently active plugin

        ### Returns:
        * `UnsafePluginIndex`: active plugin
        """
        return self._plugin

    def getWindow(self) -> WindowIndex:
        """
        Returns the currently active window

        ### Returns:
        * `UnsafeWindowIndex`: active window
        """
        return self._window

    def playPause(self, value: bool = None) -> bool:
        """
        Pause or resume updating the active plugin

        ### Args:
        * `value` (`bool`, optional): Whether the updating should happen or
          not. Defaults to `None` (toggle).

        ### Returns:
        * `bool`: whether updating will happen
        """
        self._doUpdate = not self._doUpdate if value is None else value
        return self._doUpdate

    def isUpdating(self) -> bool:
        """
        Returns whether the plugin state is actively updating (or paused)
        """
        return self._doUpdate

    def setSplitWindowsPlugins(self, value: bool) -> None:
        """
        Sets whether windows and plugins should be addressed independently.

        This should be set by the device object during initialization if that
        device has a way to toggle between plugin and DAW controls.
        """
        self._split = value

    def toggleWindowsPlugins(self, value: bool = None) -> bool:
        """
        Toggles whether we are currently addressing windows or plugins.

        This should be triggered by the script when a [type] event is detected
        from the plugin.
        TODO: type

        ### Args:
        * `value` (`bool`, optional): whether the active plugin should be a
          plugin (True) or a window (False), or toggled (None). Defaults to
          `None`.

        ### Raises:
        * `ValueError`: setSplitWindowsPlugins() hasn't been called

        ### Returns:
        * `bool`: whether plugins (True) or windows (False) are being addressed
        """
        if not self._split:
            raise ValueError("Can't toggle between windows and plugins unless "
                             "they are being addressed independently")
        else:
            self._changed = True
            self._plug_active = \
                not self._plug_active if value is None else value
            return self._plug_active

    def isPlugActive(self) -> bool:
        """
        Returns whether plugins are focused (as opposed to windows), when split
        plugins are active.

        ### Returns:
        * `bool`: whether plugins are focused
        """
        if not self._split:
            raise ValueError("Can't toggle between windows and plugins unless "
                             "they are being addressed independently")
        return self._plug_active
