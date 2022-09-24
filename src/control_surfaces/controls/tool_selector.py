"""
control_surfaces > controls > tool_selector

Contains definition for tool selector button. Used to choose from a selection
of tools or pages (eg on the playlist).
"""

from .control_surface import ControlSurface
from .button import Button
from .drum_pad import DrumPad


class ToolSelector(Button):
    """
    A button used to choose from a selection of tools. The script expects a
    number of these to be defined, preferably as a row. Each tool selector
    button can then be mapped to a single tool or page.

    Falls back to:
    * `DrumPad`
    """

    @staticmethod
    def getControlAssignmentPriorities() -> tuple[type[ControlSurface], ...]:
        return (DrumPad,)
