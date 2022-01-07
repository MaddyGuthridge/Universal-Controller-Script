
from typing import Callable

from . import Device

from controlsurfaces import ControlShadow, ControlMapping

class DeviceShadow:
    
    def __init__(self, device: Device) -> None:
        self.__device = device
        self.__all_controls = device.getControlShadows()
        self.__free_controls = self.__all_controls.copy()
        self.__assigned_controls: dict[ControlMapping, tuple] = {}
    
    def getControlMatches(self, control: type, target_num:int=-1) -> list[ControlShadow]:
        """
        Returns a list of matching controls

        A matching control is defined as inheriting from the given type, is a
        member of the same group, and which isn't already assigned.

        ### Args:
        * `control` (`type`): Type of control to match

        ### Returns:
        * `list[ControlShadow]`: List of matches
        """
        num_group_matches = dict.fromkeys(self.__device.getGroups(), 0)
        for c in self.__free_controls:
            if isinstance(c, control):
                num_group_matches[c.group] += 1
        
    
    def getNumControlMatches(self, control: type) -> int:
        """
        Returns the number of controls matching the required type.

        A matching control is defined as inheriting from the given type, and
        which isn't already assigned

        ### Args:
        * `control` (`type`): Type of control to match

        ### Returns:
        * `int`: number of types that match
        """
        return len(self.getControlMatches(control))
        
    def getNumSubsControlMatches(self, control: type) -> int:
        """
        Returns the number of substituted controls matching the required type.

        A matching substituted control is defined as inheriting from the given
        type, or from a substituted type.

        ### Args:
        * `control` (`type`): Type of control to match

        ### Returns:
        * `int`: number of types that match
        """
        return 0

    def bindControl(self, control: ControlShadow, bind_to: Callable, args:tuple=tuple()):
        if control not in self.__free_controls:
            raise ValueError("Control must be free to bind to")
        
        # Remove from free controls
        self.__free_controls.remove(control)
        
        # Bind to callable
        self.__assigned_controls[control.getMapping()] = (control, bind_to, args)

    def bindControls(self, controls: list[ControlShadow], bind_to: Callable):
        
        # Ensure all controls are assignable
        if not all(c in self.__free_controls for c in controls):
            raise ValueError("All controls must be free to bind to")
        
        # Bind each control, using the index of it as the argument
        for i, c in enumerate(controls):
            self.bindControl(c, bind_to, (i,))
    
    def processEvent(self, control: ControlMapping):
        
        # Get control's mapping if it's assigned
        try:
            control, fn, args = self.__assigned_controls[control]
        except KeyError:
            # If we get a KeyError, the control isn't assigned and we should do
            # nothing
            return
        # Call the bound function with any extra required args
        fn(control, *args)

    def apply(self) -> None:
        """
        Apply the configuration of the device shadow to the control it represents
        """
        for c in self.__all_controls:
            c.apply()
