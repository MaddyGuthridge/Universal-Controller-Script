
from typing import Any, Callable, Optional, Protocol

from common.util.dicttools import lowestValueGrEqTarget, greatestKey
from controlsurfaces import ControlSurface
from . import Device

from controlsurfaces import ControlShadow, ControlMapping

class EventCallback(Protocol):
    """
    Type definition for a callback function, which accepts a control mapping, as
    well as any other unspecified arguments
    
    ### Args:
    * `control` (`ControlSurface`): control associated with the event
    * `*args` (`Any`): any other arguments, as defined when binding the function
    
    ### Returns:
    * `bool`: Whether the event has been handled or not
    """
    def __call__(self, control: ControlShadow, *args: Any) -> bool:
        ...

class DeviceShadow:
    
    def __init__(self, device: Device) -> None:
        self.__device = device
        self.__all_controls = device.getControlShadows()
        self.__free_controls = self.__all_controls.copy()
        self.__assigned_controls: dict[
                ControlMapping,
                tuple[ControlShadow, EventCallback, tuple]
            ] = {}
    
    def _getMatches(
        self, 
        expr: Callable[[ControlSurface], bool], 
        target_num:int=...
    ) -> list[ControlShadow]:
        """
        Returns a list of control matches for a give condition lambda

        This function is called by getControlMatches and getSubsControlMatches
        to remove repeated code. Calling this function from outside this class
        is not recommended.

        ### Args:
        * `expr` (`Callable[[ControlSurface], bool]`): Expression to check types
        * `target_num` (`int`, optional): Target number to get, so that we don't
        use more space than necessary. Defaults to `...`.

        ### Returns:
        * `list[ControlShadow]`: List of available controls
        """
        num_group_matches = dict.fromkeys(self.__device.getGroups(), 0)
        group_matches: dict[str, list] = dict()
        for c in self.__free_controls:
            if expr(c.getControl()):
                num_group_matches[c.group] += 1
                if c.group in group_matches:
                    group_matches[c.group].append(c)
                else:
                    group_matches[c.group] = [c]
        
        if target_num is Ellipsis:
            highest = greatestKey(num_group_matches)
        else:
            highest = lowestValueGrEqTarget(num_group_matches, target_num)
        
        return group_matches[highest]
    
    def getControlMatches(self, control: type[ControlSurface], target_num:int=...) -> list[ControlShadow]:
        """
        Returns a list of matching controls

        A matching control is defined as inheriting from the given type, is a
        member of the same group, and which isn't already assigned.

        ### Args:
        * `control` (`type`): Type of control to match
        * `target_num` (`int`): Number of matches to look for, to ensure we
          don't waste controls that can support more space. If not provided, the
          maximum sized group will be given.

        ### Returns:
        * `list[ControlShadow]`: List of matches
        """
        return self._getMatches(
            lambda x: isinstance(x, control),
            target_num
        )
    
    def getNumControlMatches(self, control: type[ControlSurface]) -> int:
        """
        Returns the number of controls matching the required type.

        A matching control is defined as inheriting from the given type, being a
        member of the same group as other matches, and which isn't already 
        assigned.

        ### Args:
        * `control` (`type`): Type of control to match

        ### Returns:
        * `int`: number of types that match
        """
        return len(self.getControlMatches(control))
        
    def getSubsControlMatches(self, control: type[ControlSurface], target_num:int=...) -> list[ControlShadow]:
        """
        Returns a list of matching controls

        A matching control is defined as a control inheriting from the given 
        type or a substituted type, is a member of the same group as other 
        matches, and which isn't already assigned.

        ### Args:
        * `control` (`type`): Type of control to match
        * `target_num` (`int`): Number of matches to look for, to ensure we
          don't waste controls that can support more space. If not provided, the
          maximum sized group will be given.

        ### Returns:
        * `list[ControlShadow]`: List of matches
        """
        return self._getMatches(
            lambda x: isinstance(x, control.getControlAssignmentPriorities()),
            target_num
        )
    
    def getNumSubsControlMatches(self, control: type[ControlSurface]) -> int:
        """
        Returns the number of substituted controls matching the required type.

        A matching control is defined as a control inheriting from the given 
        type or a substituted type, is a member of the same group as other 
        matches, and which isn't already assigned.

        ### Args:
        * `control` (`type`): Type of control to match

        ### Returns:
        * `int`: number of types that match
        """
        return len(self.getSubsControlMatches(control))

    def bindControl(
        self,
        control: ControlShadow,
        bind_to: EventCallback,
        args:tuple=...
    ) -> None:
        """
        Binds a callback function to a control, so the function will be called
        whenever that control is tweaked.

        ### Args:
        * `control` (`ControlShadow`): control to bind
        * `bind_to` (`EventCallback`): callback function to bind. Refer to
          EventCallback documentation for how this should be structured.
        * `args` (`tuple`, optional): args for the callback function. Defaults to `...`.

        ### Raises:
        * `ValueError`: Control isn't free to bind to. This indicates a logic
          error in the code assigning controls
        """
        if control not in self.__free_controls:
            raise ValueError("Control must be free to bind to")
        
        # Remove from free controls
        self.__free_controls.remove(control)
        
        # Bind to callable
        self.__assigned_controls[control.getMapping()] = (control, bind_to, args)

    def bindControls(
        self,
        controls: list[ControlShadow],
        bind_to: EventCallback,
        args_list: Optional[list[tuple]]=...
    ) -> None:
        """
        Binds a single function all controls in a list.

        This can be used for bulk assignment of controls.

        ### Args:
        * `controls` (`list[ControlShadow]`): List of controls to bind to
        * `bind_to` (`EventCallback`): callback function to bind. Refer to
          EventCallback documentation for how this should be structured.
        * `args_list` (`Optional[list[tuple]]`, optional): List of arguments to
          pass to the function:
            * `...` (default): indices of the controls (ie the first control in
              the list will cause the callback to be given the argument `0`).
            * `None`: no arguments will be given.
            * `list[tuple]`: The arguments provided in the tuple at the index
              corresponding to the event that was called will be given to the
              function as arguments.

        ### Raises:
        * `ValueError`: Args list length not equal to controls list length
        * `ValueError`: Not all controls in controls list are free to bind to
        """
        # If no callback args given, generate index numbers
        if args_list is Ellipsis:
            args_list = [(i,) for i in range(len(controls))]
        # If explicitly set to None, use empty args
        elif args_list is None:
            args_list = [tuple() for _ in range(len(controls))]
        # Otherwise, check length
        else:
            if not len(args_list) == len(controls):
                raise ValueError("Args list must be of the same length as "
                                 "controls list")
        
        # Ensure all controls are assignable
        if not all(c in self.__free_controls for c in controls):
            raise ValueError("All controls must be free to bind to")
        
        # Bind each control, using the index of it as the argument
        for c, a in zip(controls, args_list):
            self.bindControl(c, bind_to, a)
    
    def processEvent(self, control: ControlMapping) -> bool:
        """
        Process an event by calling the bound callback function associated with
        it if applicable.

        ### Args:
        * `control` (`ControlMapping`): Control associated with the event
        
        ### Returns:
        * `bool`: Whether the event has been handled
        """
        # Get control's mapping if it's assigned
        try:
            control_shadow, fn, args = self.__assigned_controls[control]
        except KeyError:
            # If we get a KeyError, the control isn't assigned and we should do
            # nothing
            return False
        # Call the bound function with any extra required args
        return fn(control_shadow, *args)

    def apply(self) -> None:
        """
        Apply the configuration of the device shadow to the control it represents
        """
        for c in self.__all_controls:
            c.apply()
