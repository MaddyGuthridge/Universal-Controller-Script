
from controlsurfaces import ControlSurface, Note, NoteAfterTouch, ChannelAfterTouch

def getNotesSingleChannel(channel: int = 0) -> list[ControlSurface]:
    return [Note(i, channel) for i in range(128)]

def getNotesAllChannels() -> list[ControlSurface]:
    r = []
    for i in range(16):
        r += getNotesSingleChannel(i)
    return r

def getNoteAfterTouchSingleChannel(channel: int = 0) -> list[ControlSurface]:
    return [NoteAfterTouch(n, channel) for n in range(128)]

def getNoteAfterTouchAllChannels() -> list[ControlSurface]:
    r = []
    for i in range(16):
        r += getNoteAfterTouchSingleChannel(i)
    return r

def getChannelAftertouchAllChannels() -> list[ControlSurface]:
    return [ChannelAfterTouch(i) for i in range(16)]
