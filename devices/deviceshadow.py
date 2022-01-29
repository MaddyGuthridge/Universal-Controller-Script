"""
devices > deviceshadow

Contains the DeviceShadow class, representing a shadow of the device which can
be manipulated without modifying the original device.

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]
"""
# from __future__ import annotations

from typing import TYPE_CHECKING, Any, Callable, Optional, Protocol
from common.util.apifixes import PluginIndex

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
    def __call__(self, control: ControlShadow, index: PluginIndex, *args: Any) -> bool:
        ...

class DeviceShadow:
    """
    Represents the "shadow" of a device, allowing plugins to bind parameters to
    the device's control surfaces independently of other plugins, and without
    affecting the actual device unless the script chooses to apply this shadow.
    """
    def __init__(self, device: Device) -> None:
        """
        Create a device shadow

        ### Args:
        * `device` (`Device`): device to shadow
        """
        self._device = device
        self._all_controls = device.getControlShadows()
        self._free_controls = self._all_controls.copy()
        self._assigned_controls: dict[
                ControlMapping,
                tuple[ControlShadow, EventCallback, tuple]
            ] = {}
    
    def _getMatches(
        self, 
        expr: Callable[[ControlSurface], bool], 
        target_num:int=None
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
        num_group_matches = dict.fromkeys(self._device.getGroups(), 0)
        group_matches: dict[str, list] = dict()
        for c in self._free_controls:
            if expr(c.getControl()):
                num_group_matches[c.group] += 1
                if c.group in group_matches:
                    group_matches[c.group].append(c)
                else:
                    group_matches[c.group] = [c]
        
        if target_num is None:
            highest = greatestKey(num_group_matches)
        else:
            highest = lowestValueGrEqTarget(num_group_matches, target_num)
        
        return group_matches[highest]
    
    def getControlMatches(self, control: type[ControlSurface], target_num:int=None) -> list[ControlShadow]:
        """
        Returns a list of matching controls

        A matching control is defined as inheriting from the given type, is a
        member of the same group, and which isn't already assigned.

        ### Args:
        * `control` (`type`): Type of control to match
        * `target_num` (`int`, optional): Number of matches to look for, to ensure we
          don't waste controls that can support more space. If not provided, the
          maximum sized group will be given. Note that fewer controls could be
          returned if not enough are available. To ensure an exact number, use
          getControlMatchesExact(). Defaults to `None`.

        ### Returns:
        * `list[ControlShadow]`: List of matches
        """
        return self._getMatches(
            lambda x: isinstance(x, control),
            target_num
        )
    
    def getControlMatchesExact(self, control: type[ControlSurface], target_num:int) -> list[ControlShadow]:
        """
        Returns a list of matching controls

        A matching control is defined as inheriting from the given type, is a
        member of the same group, and which isn't already assigned.

        ### Args:
        * `control` (`type`): Type of control to match
        * `target_num` (`int`): Number of matches to look for. If not enough are
          found, a ValueError is raised.
        
        ### Raises:
        * `ValueError`: Not enough matching controls found

        ### Returns:
        * `list[ControlShadow]`: List of matches
        """
        ret = self.getControlMatches(control, target_num)
        if len(ret) == target_num:
            return ret
        else:
            raise ValueError("Not enough controls of specified type found")
        
    
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
        
    def getSubsControlMatches(self, control: type[ControlSurface], target_num:int=None) -> list[ControlShadow]:
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
    
    def getSubsControlMatchesExact(self, control: type[ControlSurface], target_num:int) -> list[ControlShadow]:
        """
        Returns a list of matching controls including substitutes

        A matching control is defined as a control inheriting from the given 
        type or a substituted type, is a member of the same group as other 
        matches, and which isn't already assigned.

        ### Args:
        * `control` (`type`): Type of control to match
        * `target_num` (`int`): Number of matches to look for. If not enough are
          found, a ValueError is raised.
        
        ### Raises:
        * `ValueError`: Not enough matching controls found

        ### Returns:
        * `list[ControlShadow]`: List of matches
        """
        ret = self.getSubsControlMatches(control, target_num)
        if len(ret) == target_num:
            return ret
        else:
            raise ValueError("Not enough controls of specified type found")
    
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
        args:'tuple|ellipsis'=...
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
        if control not in self._free_controls:
            raise ValueError("Control must be free to bind to")
        
        if args is Ellipsis:
            args_: tuple = tuple()
        else:
            if TYPE_CHECKING:
                assert not isinstance(args, ellipsis)
            args_ = args
        
        
        # Remove from free controls
        self._free_controls.remove(control)
        
        # Bind to callable
        self._assigned_controls[control.getMapping()] = (control, bind_to, args_)

    def bindControls(
        self,
        controls: list[ControlShadow],
        bind_to: EventCallback,
        args_list: 'Optional[list[tuple]]|ellipsis'=...
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
            if TYPE_CHECKING:
                assert isinstance(args_list, list)
            if not len(args_list) == len(controls):
                raise ValueError("Args list must be of the same length as "
                                 "controls list")
        
        # Ensure all controls are assignable
        if not all(c in self._free_controls for c in controls):
            raise ValueError("All controls must be free to bind to")
        
        # Bind each control, using the index of it as the argument
        for c, a in zip(controls, args_list):
            self.bindControl(c, bind_to, a)
    
    def bindFirstMatch(
        self,
        control: type[ControlSurface],
        bind_to: EventCallback,
        args:'tuple|ellipsis'=...
    ) -> None:
        """
        Finds the first control of a matching type and binds it to the given
        function.

        ### Args:
        * `control` (`ControlSurface`): control type to bind
        * `bind_to` (`EventCallback`): function to bind to
        * `args` (`tuple`, optional): args to give to callback. 
          Defaults to `...`.

        ### Raises:
        * `ValueError`: No controls were found to bind to
        """
        try:
            match = self.getControlMatches(control, 1)[0]
        except IndexError:
            raise ValueError("No controls found to bind to")
        self.bindControl(match, bind_to, args)
    
    def bindFirstMatchSafe(
        self,
        control: type[ControlSurface],
        bind_to: EventCallback,
        args:'tuple|ellipsis'=...
    ) -> bool:
        """
        Finds the first control of a matching type and binds it to the given
        function, if one can be found.

        ### Args:
        * `control` (`ControlSurface`): control type to bind
        * `bind_to` (`EventCallback`): function to bind to
        * `args` (`tuple`, optional): args to give to callback. 
          Defaults to `...`.
        
        ### Returns:
        * `bool`: whether the assignment was successful
        """
        try:
            self.bindFirstMatch(control, bind_to, args)
        except ValueError:
            return False
        else:
            return True
        
    def bindFirstSubsMatch(
        self,
        control: type[ControlSurface],
        bind_to: EventCallback,
        args:'tuple|ellipsis'=...
    ) -> None:
        """
        Finds the first control of a matching type, or a substitutable type,
        and binds it to the given function.

        ### Args:
        * `control` (`ControlSurface`): control type to bind
        * `bind_to` (`EventCallback`): function to bind to
        * `args` (`tuple`, optional): args to give to callback. 
          Defaults to `...`.

        ### Raises:
        * `ValueError`: No controls were found to bind to
        """
        try:
            match = self.getSubsControlMatches(control, 1)[0]
        except IndexError:
            raise ValueError("No controls found to bind to")
        self.bindControl(match, bind_to, args)
    
    def bindFirstSubsMatchSafe(
        self,
        control: type[ControlSurface],
        bind_to: EventCallback,
        args:'tuple|ellipsis'=...
    ) -> bool:
        """
        Finds the first control of a matching type, or a substitutable type,
        and binds it to the given function.

        ### Args:
        * `control` (`ControlSurface`): control type to bind
        * `bind_to` (`EventCallback`): function to bind to
        * `args` (`tuple`, optional): args to give to callback. 
          Defaults to `...`.

        ### Raises:
        * `ValueError`: No controls were found to bind to
        """
        try:
            self.bindFirstSubsMatch(control, bind_to, args)
        except ValueError:
            return False
        else:
            return True
    
    def bindMatches(
        self,
        control: type[ControlSurface],
        bind_to: EventCallback,
        target_num: int=None,
        args:'Optional[list[tuple]]|ellipsis'=...
    ) -> int:
        """
        Finds all controls of a matching type and binds them to the given
        function.

        ### Args:
        * `control` (`ControlSurface`): control type to bind
        * `bind_to` (`EventCallback`): function to bind to
        * `target_num` (`int`, optional): Number of matches to look for, to
          ensure we don't waste controls that can support more space. If not
          provided, the maximum sized group will be used. Note that fewer
          controls could be bound if not enough are available. To ensure an
          exact number, use bindMatchesExact(). Defaults to `None`.
        * `args` (`tuple`, optional): args to give to callback. 
          Defaults to `...`.
        
        ### Returns:
        * `int`: Number of controls bound successfully
        """
        matches = self.getControlMatches(control, target_num)
        self.bindControls(matches, bind_to, args)
        return len(matches)
    
    def bindSubsMatches(
        self,
        control: type[ControlSurface],
        bind_to: EventCallback,
        target_num: int=None,
        args:'Optional[list[tuple]]|ellipsis'=...
    ) -> int:
        """
        Finds all controls of a matching type, or a substitutable type, and
        binds them to the given function.

        ### Args:
        * `control` (`ControlSurface`): control type to bind
        * `bind_to` (`EventCallback`): function to bind to
        * `target_num` (`int`, optional): Number of matches to look for, to
          ensure we don't waste controls that can support more space. If not
          provided, the maximum sized group will be used. Note that fewer
          controls could be bound if not enough are available. To ensure an
          exact number, use bindSubsMatchesExact(). Defaults to `None`.
        * `args` (`tuple`, optional): args to give to callback. 
          Defaults to `...`.
        
        ### Returns:
        * `int`: Number of controls bound successfully
        """
        matches = self.getSubsControlMatches(control, target_num)
        self.bindControls(matches, bind_to, args)
        return len(matches)
    
    def bindMatchesExact(
        self,
        control: type[ControlSurface],
        bind_to: EventCallback,
        target_num: int,
        args:'Optional[list[tuple]]|ellipsis'=...
    ) -> None:
        """
        Finds all controls of a matching type and binds them to the given
        function.

        ### Args:
        * `control` (`ControlSurface`): control type to bind
        * `bind_to` (`EventCallback`): function to bind to
        * `target_num` (`int`): Number of matches to look for. If not enough are
          found, a ValueError is raised.
        * `args` (`tuple`, optional): args to give to callback. 
          Defaults to `...`.
        """
        matches = self.getControlMatchesExact(control, target_num)
        self.bindControls(matches, bind_to, args)
    
    def bindMatchesExactSafe(
        self,
        control: type[ControlSurface],
        bind_to: EventCallback,
        target_num: int,
        args:'Optional[list[tuple]]|ellipsis'=...
    ) -> bool:
        """
        Finds all controls of a matching type and binds them to the given
        function.

        ### Args:
        * `control` (`ControlSurface`): control type to bind
        * `bind_to` (`EventCallback`): function to bind to
        * `target_num` (`int`): Number of matches to look for. If not enough are
          found, a ValueError is raised.
        * `args` (`tuple`, optional): args to give to callback. 
          Defaults to `...`.
        """
        try:
            self.bindMatchesExact(control, bind_to, target_num, args)
        except ValueError:
            return False
        else:
            return True
    
    def bindSubsMatchesExact(
        self,
        control: type[ControlSurface],
        bind_to: EventCallback,
        target_num: int,
        args:'Optional[list[tuple]]|ellipsis'=...
    ) -> None:
        """
        Finds all controls of a matching type, or a substitutable type, and
        binds them to the given function.

        ### Args:
        * `control` (`ControlSurface`): control type to bind
        * `bind_to` (`EventCallback`): function to bind to
        * `target_num` (`int`): Number of matches to look for. If not enough are
          found, a ValueError is raised.
        * `args` (`tuple`, optional): args to give to callback. 
          Defaults to `...`.
        """
        matches = self.getSubsControlMatchesExact(control, target_num)
        self.bindControls(matches, bind_to, args)
    
    def bindSubsMatchesExactSafe(
        self,
        control: type[ControlSurface],
        bind_to: EventCallback,
        target_num: int,
        args:'Optional[list[tuple]]|ellipsis'=...
    ) -> bool:
        """
        Finds all controls of a matching type, or a substitutable type, and
        binds them to the given function.

        ### Args:
        * `control` (`ControlSurface`): control type to bind
        * `bind_to` (`EventCallback`): function to bind to
        * `target_num` (`int`): Number of matches to look for. If not enough are
          found, a ValueError is raised.
        * `args` (`tuple`, optional): args to give to callback. 
          Defaults to `...`.
        """
        try:
            self.bindSubsMatchesExact(control, bind_to, target_num, args)
        except ValueError:
            return False
        else:
            return True
    
    def processEvent(self, control: ControlMapping, index: PluginIndex) -> bool:
        """
        Process an event by calling the bound callback function associated with
        it if applicable.

        ### Args:
        * `control` (`ControlMapping`): Control associated with the event
        * `index` (`PluginIndex`): Index of channel or track/slot of the
          selected plugin
        
        ### Returns:
        * `bool`: Whether the event has been handled
        """
        # Get control's mapping if it's assigned
        try:
            control_shadow, fn, args = self._assigned_controls[control]
        except KeyError:
            # If we get a KeyError, the control isn't assigned and we should do
            # nothing
            return False
        # Call the bound function with any extra required args
        return fn(control_shadow, index, *args)

    def apply(self) -> None:
        """
        Apply the configuration of the device shadow to the control it represents
        """
        for c in self._all_controls:
            c.apply()
