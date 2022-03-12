"""
devices > deviceshadow

Contains the DeviceShadow class, representing a shadow of the device which can
be manipulated without modifying the original device.

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]
"""
# from __future__ import annotations

from typing import TYPE_CHECKING, Any, Callable, Optional, Protocol, Union
from common.util.apifixes import UnsafeIndex

from common.util.dicttools import lowestValueGrEqTarget, greatestKey
from controlsurfaces import ControlSurface
from . import Device

from controlsurfaces import ControlShadow, IControlHash, ControlEvent, ControlShadowEvent

if TYPE_CHECKING:
    from collections.abc import Iterable, Generator

# class EventCallback(Protocol):
#     """
#     Type definition for a callback function, which accepts a control mapping, as
#     well as any other unspecified arguments
#
#     ### Args:
#     * `control` (`ControlSurface`): control associated with the event
#     * `*args` (`Any`): any other arguments, as defined when binding the function
#
#     ### Returns:
#     * `bool`: Whether the event has been handled or not
#     """
#     def __call__(self, control: ControlShadow, index: PluginIndex, *args: tuple[Any]) -> bool:
#         ...

# I'm so sorry about this horrendous piece of type hinting
# There is no other way to do this that I've found
# HELP WANTED: Can someone please fix this awfulness in a way that doesn't cause
# MyPy to have a temper tantrum?
StandardEventCallback = Union[
    Callable[[ControlShadowEvent, UnsafeIndex], bool],
    Callable[[ControlShadowEvent, UnsafeIndex, Any], bool],
    Callable[[ControlShadowEvent, UnsafeIndex, Any, Any], bool],
    Callable[[ControlShadowEvent, UnsafeIndex, Any, Any, Any], bool],
    Callable[[ControlShadowEvent, UnsafeIndex, Any, Any, Any, Any], bool],
    Callable[[ControlShadowEvent, UnsafeIndex, Any, Any, Any, Any, Any], bool],
    Callable[[ControlShadowEvent, UnsafeIndex, Any, Any, Any, Any, Any, Any], bool],
    Callable[[ControlShadowEvent, UnsafeIndex, Any, Any, Any, Any, Any, Any, Any], bool],
    Callable[[ControlShadowEvent, UnsafeIndex, Any, Any, Any, Any, Any, Any, Any, Any], bool],
    Callable[[ControlShadowEvent, UnsafeIndex, Any, Any, Any, Any, Any, Any, Any, Any, Any], bool],
]

EventCallback = StandardEventCallback

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
                IControlHash,
                tuple[ControlShadow, EventCallback, tuple]
            ] = {}
        self._transparent = False

    def __repr__(self) -> str:
        """
        Returns simplified representation of shadow, excluding mappings

        ### Returns:
        * `str`: shorter representation
        """
        return f"Device shadow for {type(self._device)}. "\
               f"{len(self._assigned_controls)} assigned controls"

    def __str__(self) -> str:
        """
        Return representation of shadow, including mappings to functions

        This should be used for debugging purposes

        ### Returns:
        * `str`: info on mappings
        """
        header = f"Shadow of device: {type(self._device)}"

        assigned = "Assigned controls:\n" + "\n".join([
            f" * {repr(control.getControl())} -> {call}{args} | "
            f"value={shadow.value}, color={shadow.color}, annotaion='{shadow.annotation}'"
            for control, (shadow, call, args) in self._assigned_controls.items()
        ])

        # unassigned = "Unassigned controls:\n" + "\n".join([
        #     f" * {control.getControl()}"
        #     for control in self._free_controls
        # ])

        unassigned = f"{len(self._free_controls)} free controls"

        return f"{header}\n\n{assigned}\n\n{unassigned}"

    def getDevice(self) -> Device:
        """
        Returns a reference to the device this shadow represents

        ### Returns:
        * `Device`: device
        """
        return self._device

    def setTransparent(self, value: bool) -> None:
        """
        Control whether this device shadow is "transparent"

        If it is, then all unassigned controls will be ignored, such that they
        can be modified and processed from other plugins. This should be used
        by special plugins to ensure that they don't send unnecessary MIDI
        signals to the device.

        ### Args:
        * `value` (`bool`): new transparency value
        """
        self._transparent = value

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
        group_matches: dict[str, list] = {g: [] for g in self._device.getGroups()}
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
        exact: bool = True,
        raise_on_zero: bool = False
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
        * `raise_on_zero`  (`bool`, optional): Whether to raise an error if no
          matching controls are found. This is to prevent errors when attempting
          to bind to a control when there aren't any matches at all.

        ### Raises:
        * `ValueError`: Not enough matching controls found, when `exact` is
          `True`.
        * `ValueError`: Too many matching controls, when `exact` is `True` and
          `trim` is `False`.
        * `ValueError`: No matching controls found (when `raise_on_zero` is
          True)

        ### Returns:
        * `list[ControlShadow]`: List of matches
        """

        # Determine what lambda to use depending on if we are allowing control
        # substitution
        no_subs = lambda x: isinstance(x, control)
        subs = lambda x: isinstance(x, control.getControlAssignmentPriorities()) or isinstance(x, control)
        if allow_substitution:
            ret = self._getMatches(
                no_subs,
                target_num
            )
            t = target_num if target_num is not None else 1
            # If we didn't get enough matches, then we should try substitution
            # TODO: Improve this
            if len(ret) < t:
                ret = self._getMatches(
                    subs,
                    target_num
                )

        else:
            ret = self._getMatches(
                no_subs,
                target_num
            )

        # Sort the matches based on coordinate
        sort_key = lambda c : c.coordinate
        ret.sort(key=sort_key)

        # Make sure we have results
        if raise_on_zero and len(ret) == 0:
            raise ValueError("No matching controls found")

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
            allow_substitution,
            raise_on_zero=False
        ))

    def bindControl(
        self,
        control: ControlShadow,
        bind_to: EventCallback,
        args: tuple = None
    ) -> None:
        """
        Binds a callback function to a control, so the function will be called
        whenever that control is tweaked.

        ### Args:
        * `control` (`ControlShadow`): control to bind
        * `bind_to` (`EventCallback`): callback function to bind. Refer to
          EventCallback documentation for how this should be structured.
        * `args` (`tuple`, optional): arguments to give to the callback
          function. Defaults to `None` (no arguments).

        ### Raises:
        * `ValueError`: Control isn't free to bind to. This indicates a logic
          error in the code assigning controls
        """
        if control not in self._free_controls:
            raise ValueError("Control must be free to bind to")

        if args is None:
            args_: tuple = tuple()
        else:
            args_ = args

        # Remove from free controls
        self._free_controls.remove(control)

        # Bind to callable
        self._assigned_controls[control.getMapping()] = (control, bind_to, args_)

    def bindControls(
        self,
        controls: list[ControlShadow],
        bind_to: EventCallback,
        args_iterable: 'Optional[Iterable[tuple[Any, ...]] | ellipsis]' = None
    ) -> None:
        """
        Binds a single function all controls in a list.

        This can be used for bulk assignment of controls.

        ### Args:
        * `controls` (`list[ControlShadow]`): List of controls to bind to
        * `bind_to` (`EventCallback`): callback function to bind. Refer to
          EventCallback documentation for how this should be structured.
        * `args_iterable` (`Iterable[tuple] | ellipsis`, optional): Iterable of
          arguments to pass to the function:
                * `None` (default): no arguments will be given.
                * `...`: indices of the controls (ie the first control in
                  the list will cause the callback to be given the argument
                  `0`).
                * `list[tuple]`: each control will be associated with the tuple
                  of arguments with the same index. Note that the list of
                  argument tuples will need to be at least of the same length as
                  the list of controls to bind. Any excess arguments will be
                  ignored.
                * `Generator[tuple, None, None]`: the generator will be iterated
                  over in order to generate tuples of arguments for each
                  control. Note that this refers to a generator object, not a
                  generator function.

        ### Raises:
        * `ValueError`: Args list length not equal to controls list length
        * `ValueError`: Not all controls in controls list are free to bind to
        """
        # If ellipsis given for args iterable, generate index numbers
        if args_iterable is Ellipsis:
            args_iter: 'Iterable[tuple[Any, ...]]' = ((i,) for i in range(len(controls)))
        # If args iterable is None, use empty args
        elif args_iterable is None:
            args_iter = (tuple() for _ in range(len(controls)))
        # Otherwise, check length
        else:
            try:
                # Ignore type checking, since we're in a try-except to avoid the
                # error anyway
                if len(args_iterable) < len(controls): # type: ignore
                    raise ValueError("Args list must be of the same length as "
                                    "controls list")

                # Get rid of incorrect flag for ellipsis
                if TYPE_CHECKING:
                    assert not isinstance(args_iterable, ellipsis)
                args_iter = (a for a in args_iterable)
            except TypeError:
                # Iterable doesn't support len, assume it's infinite (ie a
                # generator)
                if TYPE_CHECKING:
                    assert isinstance(args_iterable, Generator)
                args_iter = args_iterable

        # Ensure all controls are assignable
        if not all(c in self._free_controls for c in controls):
            raise ValueError("All controls must be free to bind to")

        # Bind each control, using the index of it as the argument
        for c, a in zip(controls, args_iter):
            self.bindControl(c, bind_to, a)

    def bindMatch(
        self,
        control: type[ControlSurface],
        bind_to: EventCallback,
        args: tuple = None,
        allow_substitution: bool = False,
        raise_on_failure: bool = True
    ) -> Optional[ControlShadow]:
        """
        Finds the first control of a matching type and binds it to the given
        function.

        ### Args:
        * `control` (`ControlSurface`): control type to bind
        * `bind_to` (`EventCallback`): function to bind to
        * `args` (`tuple`, optional): arguments to give to the callback
          function. Defaults to `None` (no arguments).
        * `allow_substitution` (`bool`, optional): whether the control can be
          substituted for a similar control. Defaults to `False`.
        * `raise_on_failure` (`bool`, optional): whether failure to assign the
          control should result in a `ValueError` being raised. When this is
          `False`, `None` will be returned instead or a control surface.
          Defaults to `True`.

        ### Raises:
        * `ValueError`: No controls were found to bind to (when
          `raise_on_failure` is `True`)

        ### Returns
        * `ControlSurface`: The control surface that was bound to, so that
          properties of it can be set.
        * `None`: if binding failed and `raise_on_failure` is `False`
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
                return None
        self.bindControl(match, bind_to, args)
        return match

    def bindMatches(
        self,
        control: type[ControlSurface],
        bind_to: EventCallback,
        args_iter_gen: 'list[tuple] | Callable[[list[ControlShadow]], Generator[tuple, None, None]] | ellipsis | None'\
            = None,
        allow_substitution: bool = False,
        target_num: int = None,
        trim: bool = True,
        exact: bool = True,
        raise_on_failure: bool = True
    ) -> list[ControlShadow]:
        """
        Finds all controls of a matching type and binds them to the given
        function.

        ### Args:
        * `control` (`ControlSurface`): control type to bind.
        * `bind_to` (`EventCallback`): function to bind to.
        * `args_iterable`: Iterable of arguments to pass to the function:
                * `None` (default): no arguments will be given.
                * `...`: indices of the controls (ie the first control in
                  the list will cause the callback to be given the argument
                  `0`).
                * `list[tuple]`: each control will be associated with the tuple
                  of arguments with the same index. Note that the list of
                  argument tuples will need to be at least of the same length as
                  the list of controls to bind. Any excess arguments will be
                  ignored.
                * `GeneratorFunction (list[ControlShadow]) -> Generator ->
                  tuple`: the generator will be iterated
                  over in order to generate tuples of arguments for each
                  control. Note that if the number of matches isn't guaranteed,
                  a generator should be used to get callback arguments.
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
          `False`, an empty list will be returned instead. Defaults to `True`.

        ### Raises:
        * `TypeError`: Potential bad number of callback arguments due to unknown
          number of controls being bound (ie. `exact` is `False`).
        * `ValueError`: No controls were found to bind to (when
          `raise_on_failure` is `True`)

        ### Returns:
        * `list[ControlSurface]`: List of controls bound successfully
        """

        # Ensure we don't risk having too few arguments to bind to
        if isinstance(args_iter_gen, list) and not exact:
            raise TypeError(f"A generator function should be used to create "
                            f"callback arguments if the number of controls to "
                            f"be bound is unknown (ie. when {exact=})")

        # Try to get a list of matching controls
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
                return []

        # Check for generator functions
        if not isinstance(args_iter_gen, (list, type(...), type(None))):
            if TYPE_CHECKING:
                assert not isinstance(args_iter_gen, ellipsis)
                assert args_iter_gen is not None
            # Turn the generator function into a generator (which is iterable)
            iterable: 'Iterable[tuple[Any, ...]] | ellipsis | None'\
                = args_iter_gen(matches)
        else:
            # Otherwise it's already iterable (or will be made so by the
            # bindControls() method)
            iterable = args_iter_gen
        # Finally, bind all the controls
        self.bindControls(matches, bind_to, iterable)
        return matches

    def processEvent(self, control: ControlEvent, index: UnsafeIndex) -> bool:
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

        # Generate a control shadow mapping to send to the device
        mapping = ControlShadowEvent(control, control_shadow)
        # Call the bound function with any extra required args
        return fn(mapping, index, *args)

    def apply(self, thorough: bool) -> None:
        """
        Apply the configuration of the device shadow to the control it represents
        """
        if self._transparent or not thorough:
            controls = (c for c, _, _ in self._assigned_controls.values())
        else:
            controls = (c for c in self._all_controls)
        for c in controls:
            c.apply(thorough)
