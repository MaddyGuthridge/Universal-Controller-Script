import channels

from common.context_manager import getContext
from control_surfaces import ControlShadow, DrumPad

INDEX = 1


def coordToIndex(control: ControlShadow) -> int:
    """Return the global index of a channel given a drum pad coordinate

    If the drum pad maps to nothing, -1 is returned.
    """
    assert isinstance(control.getControl(), DrumPad)
    drums_width = getContext().getDevice().getDrumPadSize()[1]
    row, col = control.getControl().coordinate
    index = drums_width * row + col
    if index >= channels.channelCount(1):
        return -1
    return index
