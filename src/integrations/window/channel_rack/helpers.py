"""
integrations > window > channel_rack > helpers

Helper functions for working with the channel rack

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""

import channels

from common.context_manager import getContext
from common.plug_indexes import WindowIndex
from common.tracks import Channel
from control_surfaces import ControlShadow, DrumPad

INDEX = WindowIndex.CHANNEL_RACK


def getNumDrumCols() -> int:
    """Returns the number of columns that the are supported by the controller
    """
    return getContext().getDevice().getDrumPadSize()[1]


def coordToIndex(control: ControlShadow) -> int:
    """Return the global index of a channel given a drum pad coordinate

    If the drum pad maps to nothing, -1 is returned.
    """
    assert isinstance(control.getControl(), DrumPad)
    num_cols = getNumDrumCols()
    row, col = control.getControl().coordinate
    index = num_cols * row + col
    if index >= channels.channelCount(False):
        return -1
    return index


def getChannelRows() -> list[Channel]:
    """
    Returns the rows which should be used by the channel rack, when using the
    drum pad as a step sequencer

    ## Actual behavior:

    Channels from the first selection onwards

    ## Preferred behavior:

    Initially this is selected channels, but if we run out of those, it's
    all channels after the last selection

    This isn't implemented as there is no way to multi-select on the
    channel rack
    """
    num_cols = getNumDrumCols()
    s = channels.selectedChannel(False)
    ret = []
    for i in range(s, channels.channelCount(False)):
        ret.append(Channel(i))
    return ret[:num_cols]

    # s = getSelectedChannels(global_mode=False)
    # if s == []:
    #     s = [0]
    # num_ch = channels.channelCount(True)
    # height = num_cols - len(s)
    # ch_select = s[-1] + 1
    # for _ in range(height):
    #     if ch_select >= num_ch:
    #         break
    #     s.append(ch_select)
    #     ch_select += 1
    # return s[:num_cols]
