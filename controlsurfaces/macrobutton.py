"""
controlsurfaces > macrobutton

Defines control surfaces used for macros, such as save, undo, etc

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]
"""

__all__ = [
    'MacroButton',
    'SaveButton',
    'UndoRedoButton',
    'UndoButton',
    'RedoButton',
    'QuantizeButton',
    'ControlSwitchButton',
]

from common.eventpattern.ieventpattern import IEventPattern
from controlsurfaces.valuestrategies.ivaluestrategy import IValueStrategy
from controlsurfaces import Button


class MacroButton(Button):
    """
    Macro buttons are buttons that should be assigned to a particular function
    in FL Studio.
    """


class SaveButton(MacroButton):
    """
    Defines a save button, which will be mapped to the save command in FL
    Studio
    """


class UndoRedoButton(MacroButton):
    """
    Defines an undo-redo button, which will be mapped to FL Studio's undo-redo
    command.

    If there is nothing to redo, this will trigger an undo. Otherwise, it will
    trigger a redo (much like the default Ctrl+Z behaviour in FL Studio).
    """


class UndoButton(MacroButton):
    """
    Defines an undo button, which will be mapped to FL Studio's undo command.

    This moves one step back in the undo history.
    """


class RedoButton(MacroButton):
    """
    Defines a redo button, which will be mapped to FL Studio's redo command.

    This moves one step forward in the undo history.
    """


class QuantizeButton(MacroButton):
    """
    Defines a quantize button, which should be mapped to FL Studio's snapping
    control.
    """


class ControlSwitchButton(MacroButton):
    """
    A button that is used to switch modes in some plugins (for example when
    changing between views). In order to get full control of the script,
    devices should implement this button somewhere.
    """
    def __init__(
        self,
        event_pattern: IEventPattern,
        value_strategy: IValueStrategy
    ) -> None:
        super().__init__(event_pattern, value_strategy, "control_switch")
