"""
common > activity_state

Contains the definition for the ActivityState class which manages what plugin
or window should be active.

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""

from typing import Optional
import ui
from common.profiler import profilerDecoration
from common.plug_indexes import (
    PluginIndex,
    GeneratorIndex,
    EffectIndex,
    WindowIndex,
    FlIndex,
)
from common.util.api_fixes import (
    getFocusedPluginIndex,
    getFocusedWindowIndex,
)
from common.types.bool_s import BoolS
import plugins


class ActivityState:
    """
    Maintains the currently selected plugin or window
    """

    def __init__(self) -> None:
        """
        Create an ActivityState object
        """
        self._do_update = True
        self._split = False
        self._window = WindowIndex(0)
        self._generator: GeneratorIndex = GeneratorIndex(0)
        self._effect: EffectIndex = EffectIndex(0, 0)
        self._plugin: PluginIndex = self._generator
        self._plugin_name = ""
        self._plug_active = True if self._plugin is not None else False
        self._changed = False
        self._plug_unsafe = False
        self._history: list[FlIndex] = []
        self._ignore_next_history = False

    def __repr__(self) -> str:
        return (
            f"ActivityState("
            f"updating: {self._do_update}, "
            f"split: {self._split}, "
            f"active: {self.getActive()}"
            f")"
        )

    def inspect(self) -> str:
        """
        Inspect details about the activity state.
        """
        print(f"Window: {self._window}, Plugin: {self._plugin}")
        print(f"Active: {'plugin' if self._plug_active else 'window'}")
        print(f"Updating: {self._do_update}")
        print(f"Split: {self._split}")
        return ''

    def _forcePlugUpdate(self) -> None:
        """
        Update the active plugin when other things are active (eg windows).
        Used so that split windows and plugins behaves correctly.
        """
        plugin = getFocusedPluginIndex(force=True)
        if plugin is None:
            raise TypeError("Wait this shouldn't be possible")
        if self._plugin != plugin:
            self._plugin = plugin
        try:
            self._plugin_name = plugins.getPluginName(*plugin)
        except TypeError:
            self._plugin_name = ""
        if isinstance(plugin, GeneratorIndex):
            self._generator = plugin
        else:
            self._effect = plugin

    @profilerDecoration("activity.tick")
    def tick(self) -> None:
        """
        Called frequently when we need to update the current window
        """
        from common.context_manager import getContext
        self._changed = False
        # If the current plugin name has changed, we should unpause the updates
        if self._plug_active and not self._do_update:
            try:
                if self._plugin_name != self._plugin.getName():
                    self._do_update = True
            except TypeError:
                pass
        if self._do_update:
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
                try:
                    self._plugin_name = plugin.getName()
                except TypeError:
                    self._plugin_name = ""
                if isinstance(plugin, GeneratorIndex):
                    self._generator = plugin
                else:
                    assert isinstance(plugin, EffectIndex)
                    self._effect = plugin
                if not self._split:
                    if not self._plug_active:
                        self._changed = True
                    self._plug_active = True
            else:
                self._forcePlugUpdate()
            # Add to history
            if self._changed:
                if self._ignore_next_history:
                    self._ignore_next_history = False
                else:
                    self._history.insert(0, self.getActive())
            # If there are too many things in the history
            hist_len = \
                getContext().settings.get("advanced.activity_history_length")
            if len(self._history) >= hist_len:
                self._history = self._history[:hist_len]

    def hasChanged(self) -> bool:
        """
        Returns whether the active plugin has changed in the last tick

        ### Returns:
        * `bool`: whether the active plugin changed
        """
        return self._changed

    def getActive(self) -> FlIndex:
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

    def getHistoryActivity(self, index: int) -> FlIndex:
        """
        Returns the activity entry at the given index, where 0 is the current
        activity.

        ### Args:
        * `index` (`int`): index

        ### Returns:
        * `SafeIndex`: activity
        """
        return self._history[index]

    def ignoreNextHistory(self) -> None:
        """
        Don't add the next activity change to the history
        """
        self._ignore_next_history = True

    def playPause(self, value: Optional[bool] = None) -> BoolS:
        """
        Pause or resume updating the active plugin

        ### Args:
        * `value` (`bool`, optional): Whether the updating should happen or
          not. Defaults to `None` (toggle).

        ### Returns:
        * `BoolS`: whether updating will happen
        """
        self._do_update = not self._do_update if value is None else value
        if self._do_update:
            msg = "Updating active plugin"
        else:
            if self._plug_active:
                name = self._plugin_name
            else:
                name = self._window.getName()
            msg = f"Paused active plugin on {name}"
        ui.setHintMsg(msg)
        return BoolS(self._do_update, msg)

    def isUpdating(self) -> bool:
        """
        Returns whether the plugin state is actively updating (or paused)
        """
        return self._do_update

    def setSplitWindowsPlugins(self, value: bool) -> None:
        """
        Sets whether windows and plugins should be addressed independently.

        This should be set by the device object during initialization if that
        device has a way to toggle between plugin and DAW controls.
        """
        self._split = value

    def toggleWindowsPlugins(self, value: Optional[bool] = None) -> bool:
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
