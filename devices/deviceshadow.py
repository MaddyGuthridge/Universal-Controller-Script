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
        target_num: int = None
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
            try:
                # Find the lowest value above the allowed amount
                highest = lowestValueGrEqTarget(num_group_matches, target_num)
            except ValueError:
                # If that fails, just use the highest value available
                highest = greatestKey(num_group_matches)
        
        return group_matches[highest]
    
    def getControlMatches(
        self,
        control: type[ControlSurface],
        allow_substitution: bool = False,
        target_num: int = None,
        trim: bool = True,
        exact: bool = True
    ) -> list[ControlShadow]:
        """
        Returns a list of matching controls.

        ### Args:
        * `control` (`type[ControlSurface]`): Type of control to try to match.
        * `allow_substitution` (`bool`, optional): Whether substitutable
          controls should be allowed to be used if a better number of them are
          available. Defaults to `False`.
        * `target_num` (`int`, optional): Number of matches to look for, to
          ensure we don't waste controls that can support more space. If not
          provided, the maximum sized group will be given, and the `trim` and
          `exact` parameters will be ignored. Defaults to `None`.
        * `trim` (`bool`, optional): whether extra control surface results
          should be trimmed off. This may prevent errors when trying to assign a
          specific number of controls, but if many controls are wanted, then it
          can be disabled. Defaults to `True`.
        * `exact` (`bool`, optional): whether an exact number of controls should
          be required for the function call to be successful. If this is
          disabled, the function could potentially return fewer controls than
          was requested. If this is enabled, then fewer results than the
          requested amount will raise an error, and if `trim` is disabled, then
          more results than the requested amount will raise an error as well.
          Defaults to `True`.
        
        ### Raises:
        * `ValueError`: Not enough matching controls found, when `exact` is 
          `True`.
        * `ValueError`: Too many matching controls, when `exact` is `True` and
          `trim` is `False`.

        ### Returns:
        * `list[ControlShadow]`: List of matches
        """
        
        # Determine what lambda to use depending on if we are allowing control
        # substitution
        if allow_substitution:
            l = lambda x: isinstance(x, control.getControlAssignmentPriorities())
        else:
            l = lambda x: isinstance(x, control)
        
        # Use algorithm for getting matching controls
        ret = self._getMatches(
            l,
            target_num
        )
        
        # If we have no target, ignore exact and trim parameters
        if target_num is None:
            return ret
        
        if exact:
            if len(ret) < target_num:
                raise ValueError("Not enough matching controls found")
            elif trim:
                return ret[:target_num]
            else:
                if len(ret) > target_num:
                    raise ValueError("Too many matching controls found. Ensure "
                                     "you are using the trim flag correctly.")
                return ret
        else:
            return ret
    
    def getNumControlMatches(
        self,
        control: type[ControlSurface],
        allow_substitution: bool = False
    ) -> int:
        """
        Returns the number of controls matching the required type.

        A matching control is defined as inheriting from the given type, being a
        member of the same group as other matches, and which isn't already 
        assigned.

        ### Args:
        * `control` (`type`): Type of control to match
        * `allow_substitution` (`bool`, optional): Whether substitutable
          controls should be allowed to be used if a better number of them are
          available. Defaults to `False`.

        ### Returns:
        * `int`: number of types that match
        """
        return len(self.getControlMatches(
            control,
            allow_substitution
        ))

    def bindControl(
        self,
        control: ControlShadow,
        bind_to: EventCallback,
        args: 'tuple|ellipsis' = ...
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
        # TODO: Allow the use of a generator to get arguments
        args_list: 'list[tuple]|ellipsis' = None
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
            * `None` (default): no arguments will be given.
            * `...`: indices of the controls (ie the first control in
              the list will cause the callback to be given the argument `0`).
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
        args: 'tuple|ellipsis' = ...,
        allow_substitution: bool = False,
        raise_on_failure: bool = True
    ) -> bool:
        """
        Finds the first control of a matching type and binds it to the given
        function.

        ### Args:
        * `control` (`ControlSurface`): control type to bind
        * `bind_to` (`EventCallback`): function to bind to
        * `args` (`tuple`, optional): args to give to callback. 
          Defaults to `...`.
        * `allow_substitution` (`bool`, optional): whether the control can be
          substituted for a similar control. Defaults to `False`.
        * `raise_on_failure` (`bool`, optional): whether failure to assign the
          control should result in a `ValueError` being raised. When this is 
          `False`, a `False` boolean will be returned instead. Defaults to
          `True`.

        ### Raises:
        * `ValueError`: No controls were found to bind to (when 
          `raise_on_failure` is `True`)
        
        ### Returns
        * `bool` whether the control was successfully assigned (note that when
          `raise_on_failure` is set to `True`, it will)
        """
        try:
            match = self.getControlMatches(
                control,
                allow_substitution,
                target_num=1
            )[0]
        except ValueError:
            if raise_on_failure:
                raise ValueError("No controls found to bind to")
            else:
                return False
        self.bindControl(match, bind_to, args)
        return True
    
    def bindMatches(
        self,
        control: type[ControlSurface],
        bind_to: EventCallback,
        args_list:'list[tuple]|ellipsis'=None,
        allow_substitution: bool = False,
        target_num: int = None,
        trim: bool = True,
        exact: bool = True,
        raise_on_failure: bool = True
    ) -> int:
        """
        Finds all controls of a matching type and binds them to the given
        function.

        ### Args:
        * `control` (`ControlSurface`): control type to bind.
        * `bind_to` (`EventCallback`): function to bind to.
        * `args_list` (`Optional[list[tuple]]`, optional): List of arguments to
          pass to the function:
                * `None` (default): no arguments will be given.
                * `...`: indices of the controls (ie the first control in
                  the list will cause the callback to be given the argument `0`).
                * `list[tuple]`: The arguments provided in the tuple at the index
                  corresponding to the event that was called will be given to the
                  function as arguments.
        * `target_num` (`int`, optional): Number of matches to look for, to
          ensure we don't waste controls that can support more space. If not
          provided, the maximum sized group will be used. Note that fewer
          controls could be bound if not enough are available. To ensure an
          exact number, use bindMatchesExact(). Defaults to `None`.
        * `trim` (`bool`, optional): whether extra control surface results
          should be trimmed off. This may prevent errors when trying to assign a
          specific number of controls, but if many controls are wanted, then it
          can be disabled. Defaults to `True`.
        * `exact` (`bool`, optional): whether an exact number of controls should
          be required for the function call to be successful. If this is
          disabled, the function could potentially return fewer controls than
          was requested. If this is enabled, then fewer results than the
          requested amount will raise an error, and if `trim` is disabled, then
          more results than the requested amount will raise an error as well.
          Defaults to `True`.
        * `raise_on_failure` (`bool`, optional): whether failure to assign the
          control should result in a `ValueError` being raised. When this is 
          `False`, `0` will be returned instead. Defaults to `True`.

        ### Raises:
        * `ValueError`: No controls were found to bind to (when 
          `raise_on_failure` is `True`)
        
        ### Returns:
        * `int`: Number of controls bound successfully
        """
        try:
            matches = self.getControlMatches(
                control,
                allow_substitution,
                target_num,
                trim,
                exact
            )
        except ValueError as e:
            if raise_on_failure:
                raise ValueError("Error binding controls") from e
            else:
                return 0
        self.bindControls(matches, bind_to, args_list)
        return len(matches)
    
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
