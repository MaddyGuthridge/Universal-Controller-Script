"""
common > activitystate

Contains the definition for the ActivityState class which manages what plugin or
window should be active.

Authors:
* Miguel Guthridge [hdsq@outlook.com, HDSQ#2154]
"""

from common.util.apifixes import UnsafeIndex
from common.util.apifixes import getFocusedPluginIndex, getFocusedWindowIndex

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
        self._window = getFocusedWindowIndex()
        self._plugin = getFocusedPluginIndex()
        self._plug_active = True if self._plugin is not None else False
    
    def tick(self) -> None:
        """
        Called frequently when we need to update the current window
        """
        if self._doUpdate:
            if (window := getFocusedWindowIndex()) is not None:
                self._window = window
                if not self._split:
                    self._plug_active = True
            elif (plugin := getFocusedPluginIndex()) is not None:
                self._plugin = plugin
                if not self._split:
                    self._plug_active = False

    def getActive(self) -> UnsafeIndex:
        """
        Returns the currently active window or plugin
        """
        if self._plug_active:
            return self._plugin
        else:
            return self._window
        

    def playPause(self, value: bool = None) -> bool:
        """
        Pause or resume updating the active plugin

        ### Args:
        * `value` (`bool`, optional): Whether the updating should happen or not.
          Defaults to `None` (toggle).

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
        
        This should be set by the device object during initialisation if that
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
        plugin (True) or a window (False), or toggled (None). Defaults to `None`.

        ### Raises:
        * `ValueError`: setSplitWindowsPlugins() hasn't been called

        ### Returns:
        * `bool`: whether plugins (True) or windows (False) are being addressed
        """
        if not self._split:
            raise ValueError("Can't toggle between windows and plugins unless "
                             "they are being addressed independently")
        else:
            self._plug_active = not self._plug_active if value is None else value
            return self._plug_active
