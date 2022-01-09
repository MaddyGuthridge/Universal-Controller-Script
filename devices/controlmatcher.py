
from typing import Optional
from common.types import eventData
from controlsurfaces import ControlMapping, ControlSurface

class IControlMatcher:
    
    def matchEvent(self, event: eventData) -> Optional[ControlMapping]:
        raise NotImplementedError("This function should be implemented by "
                                  "child classes")
    
    def getGroups(self) -> set[str]:
        raise NotImplementedError("This function should be implemented by "
                                  "child classes")
    
    def getControls(self, group:str=None) -> list[ControlSurface]:
        raise NotImplementedError("This function should be implemented by "
                                  "child classes")

class BasicControlMatcher(IControlMatcher):
    def __init__(self) -> None:
        self.__controls: list[ControlSurface] = []
        self.__groups: set[str] = set()
    
    def addControl(self, control: ControlSurface) -> None:
        self.__controls.append(control)
        self.__groups.add(control.group)
    
    def matchEvent(self, event: eventData) -> Optional[ControlMapping]:
        for c in self.__controls:
            m = c.match(event)
            if m is not None:
                return m
        return None
    
    def getGroups(self) -> set[str]:
        return self.__groups
    
    def getControls(self, group: str = None) -> list[ControlSurface]:
        if group is None:
            return self.__controls
        else:
            ret = []
            for c in self.__controls:
                if c.group == group:
                    ret.append(c)
            return ret
