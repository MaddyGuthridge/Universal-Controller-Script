"""
controlsurfaces > macrobutton

Defines control surfaces used for macros, such as save, undo, etc

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]
"""
from .controlsurface import ControlSurface
from controlsurfaces import Button

class MacroButton(Button):
    """
    Macro buttons are buttons that should be assigned to a particular function
    in FL Studio.
    """

class SaveButton(Button):
    """
    Defines a save button, which will be mapped to the save command in FL Studio
    """

class UndoRedoButton(Button):
    """
    Defines an undo-redo button, which will be mapped to FL Studio's undo-redo
    command.

    If there is nothing to redo, this will trigger an undo. Otherwise, it will
    trigger a redo (much like the default Ctrl+Z behaviour in FL Studio).
    """

class UndoButton(Button):
    """
    Defines an undo button, which will be mapped to FL Studio's undo command.

    This moves one step back in the undo history.
    """

class RedoButton(Button):
    """
    Defines a redo button, which will be mapped to FL Studio's redo command.

    This moves one step forward in the undo history.
    """

class QuantizeButton(Button):
    """
    Defines a quantize button, which should be mapped to FL Studio's snapping
    control.
    """

class SwitchActiveButton(Button):
    """
    Defines a switch active button, which is handled internally to switch
    event handling between the active plugin and the active window.

    Using this type of control will cause an error unless the device calls
    `getContext().activity.setSplitWindowsPlugins(self, value: bool)`
    in order to inform the script context that windows and plugins should be
    addressed independently.

    This is the abstract base class: to implement this, use
    * `SwitchActivePluginButton` for a button to switch to plugins
    * `SwitchActiveWindowButton` for a button to switch to windows
    * `SwitchActiveToggleButton` for a button to toggle between windows and
      plugins
    """

class SwitchActivePluginButton(SwitchActiveButton):
    """
    A switch active button that make generator and effects plugins be actively
    processed by the script
    """

class SwitchActiveWindowButton(SwitchActiveButton):
    """
    A switch active button that make FL Studio windows be actively
    processed by the script
    """

class SwitchActiveToggleButton(SwitchActiveButton):
    """
    A switch active button that toggles between plugins and FL Studio windows
    being actively processed by the script
    """
