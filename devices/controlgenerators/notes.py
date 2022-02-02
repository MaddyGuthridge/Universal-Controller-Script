
from controlsurfaces import ControlSurface, Note

def getNotesSingleChannel(channel: int = 0) -> list[ControlSurface]:
    return [Note(i, channel) for i in range(128)]

def getNotesAllChannels() -> list[ControlSurface]:
    r = []
    for i in range(16):
        r += getNotesSingleChannel(i)
    return r
