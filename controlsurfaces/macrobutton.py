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

class UndoRdoButton(Button):
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

    TODO: Does FL have an easily addressible quantize feature? If so map to that
    instead
    """

class SwitchActiveButton(Button):
    """
    Defines a switch active button, which is handled internally to switch
    event handling between the active plugin and the active window.

    Using this control will cause an error unless the device calls
    `getContext().activity.setSplitWindowsPlugins(self, value: bool)`
    in order to inform the script context that windows and plugins should be
    addressed independently.
    """
