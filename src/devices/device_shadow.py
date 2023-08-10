"""
devices > device_shadow

Contains the DeviceShadow class, representing a shadow of the device which can
be manipulated without modifying the original device.

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""

from typing import TYPE_CHECKING, Any, Callable, Optional, Union
from typing_extensions import TypeAlias
from common.plug_indexes import FlIndex

from common.util.dict_tools import lowestValueGrEqTarget, greatestKey
from control_surfaces import ControlSurface
from . import Device

from control_surfaces import (
    IControlShadow,
    ControlShadow,
    NullControlShadow,
    IControlHash,
    ControlEvent,
    ControlShadowEvent,
    ControlShadowList,
)

if TYPE_CHECKING:
    from collections.abc import Iterable, Generator

# I'm so sorry about this horrendous piece of type hinting
# There is no other way to do this that I've found
# HELP WANTED: Can someone please fix this awfulness in a way that doesn't
# cause MyPy to have a temper tantrum?
EventCallback = Union[
    Callable[[ControlShadowEvent, FlIndex], bool],
    Callable[[ControlShadowEvent, FlIndex, Any], bool],
    Callable[[ControlShadowEvent, FlIndex, Any, Any], bool],
    Callable[[ControlShadowEvent, FlIndex, Any, Any, Any], bool],
    Callable[[ControlShadowEvent, FlIndex, Any, Any, Any, Any], bool],
    Callable[[ControlShadowEvent, FlIndex, Any, Any, Any, Any, Any], bool],
    Callable[[ControlShadowEvent, FlIndex,
              Any, Any, Any, Any, Any, Any], bool],
    Callable[[ControlShadowEvent, FlIndex,
              Any, Any, Any, Any, Any, Any, Any], bool],
    Callable[[ControlShadowEvent, FlIndex, Any,
              Any, Any, Any, Any, Any, Any, Any], bool],
    Callable[[ControlShadowEvent, FlIndex, Any,
              Any, Any, Any, Any, Any, Any, Any, Any], bool],
]
TickCallback = Union[
    None,
    Callable[[ControlShadow, FlIndex], bool],
    Callable[[ControlShadow, FlIndex, Any], bool],
    Callable[[ControlShadow, FlIndex, Any, Any], bool],
    Callable[[ControlShadow, FlIndex, Any, Any, Any], bool],
    Callable[[ControlShadow, FlIndex, Any, Any, Any, Any], bool],
    Callable[[ControlShadow, FlIndex, Any, Any, Any, Any, Any], bool],
    Callable[[ControlShadow, FlIndex,
              Any, Any, Any, Any, Any, Any], bool],
    Callable[[ControlShadow, FlIndex,
              Any, Any, Any, Any, Any, Any, Any], bool],
    Callable[[ControlShadow, FlIndex, Any,
              Any, Any, Any, Any, Any, Any, Any], bool],
    Callable[[ControlShadow, FlIndex, Any,
              Any, Any, Any, Any, Any, Any, Any, Any], bool],
]

if TYPE_CHECKING:
    ArgGenerator: TypeAlias = Union[
        list[Any],
        Callable[[ControlShadowList], Generator[tuple, None, None]],
        ellipsis,  # noqa: F821
        None
    ]
else:
    ArgGenerator: TypeAlias = Any


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
            tuple[ControlShadow, Optional[EventCallback], TickCallback, tuple]
        ] = {}
        self._minimal = False
        self._debug: Optional[str] = None

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
            f" * {repr(control.getControl())} -> {call}{args}, {tick}{args} | "
            f"value={shadow.value}, color={shadow.color}, "
            + f"annotation='{shadow.annotation}'"
            for control, (shadow, call, tick, args)
            in self._assigned_controls.items()
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

    def copy(self) -> 'DeviceShadow':
        """
        Make a copy of this device shadow

        This returns a new DeviceShadow that maps to the same device

        ### Returns:
        * `DeviceShadow`: copy
        """
        return DeviceShadow(self.getDevice())

    def setMinimal(self, value: bool) -> None:
        """
        Control whether this device shadow is "minimal"

        If it is, then all unassigned controls will be ignored, such that they
        can be modified and processed from other plugins. This should be used
        by special plugins to ensure that they don't send unnecessary MIDI
        signals to the device.

        ### Args:
        * `value` (`bool`): new minimal value
        """
        self._minimal = value

    def setDebug(self, value: Optional[str]) -> None:
        """
        Control whether this device shadow is in debug mode

        If it is, then information will be printed when a control is processed.

        ### Args:
        * `value` (`str`, optional): new debug name. Defaults to `None`.
        """
        self._debug = value

    def _getMatches(
        self,
        expr: Callable[[ControlSurface], bool],
        target_num: Optional[int] = None,
        one_type: bool = True,
    ) -> list[ControlShadow]:
        """
        Returns a list of control matches for a give condition lambda

        This function is called by getControlMatches to reduce complexity.
        Calling this function from outside this class is not recommended.

        ### Args:
        * `expr` (`Callable[[ControlSurface], bool]`): Expression to check
          types
        * `target_num` (`int`, optional): Target number to get, so that we
          don't use more space than necessary. Defaults to `None`.
        * `one_type` (`bool`, optional): Whether controls should be separated
          based on subclasses. Defaults to `True`.

        ### Returns:
        * `list[ControlShadow]`: List of available controls
        """
        type_matches: dict[type[ControlSurface], list[ControlShadow]] = {}
        num_type_matches: dict[type[ControlSurface], int] = {}
        for c in self._free_controls:
            if one_type:
                t = type(c.getControl())
            else:
                t = ControlSurface  # type: ignore
            # If we want to assign this control
            if expr(c.getControl()):
                num_type_matches[t] = \
                    num_type_matches.get(t, 0) + 1
                if t in type_matches:
                    type_matches[t].append(c)
                else:
                    type_matches[t] = [c]

        try:
            if target_num is None:
                highest = greatestKey(num_type_matches)
            else:
                try:
                    # Find the lowest value above the allowed amount
                    highest = lowestValueGrEqTarget(
                        num_type_matches,
                        target_num
                    )
                except ValueError:
                    # If that fails, just use the highest value available
                    highest = greatestKey(num_type_matches)
        except ValueError:
            # No matches causes greatestKey() to fail since there's no keys
            return []
        return type_matches[highest]

    def getControlMatches(
        self,
        control: type[ControlSurface],
        allow_substitution: bool = True,
        target_num: Optional[int] = None,
        trim: bool = True,
        exact: bool = True,
        raise_on_zero: bool = False,
        one_type: bool = True,
    ) -> ControlShadowList:
        """
        Returns a list of matching controls.

        ### Args:
        * `control` (`type[ControlSurface]`): Type of control to try to match.
        * `allow_substitution` (`bool`, optional): Whether substitutable
          controls should be allowed to be used if a better number of them are
          available. Defaults to `True`.
        * `target_num` (`int`, optional): Number of matches to look for, to
          ensure we don't waste controls that can support more space. If not
          provided, the maximum sized group will be given, and the `trim` and
          `exact` parameters will be ignored. Defaults to `None`.
        * `trim` (`bool`, optional): whether extra control surface results
          should be trimmed off. This may prevent errors when trying to assign
          a specific number of controls, but if many controls are wanted, then
          it can be disabled. Defaults to `True`.
        * `exact` (`bool`, optional): whether an exact number of controls
          should be required for the function call to be successful. If this is
          disabled, the function could potentially return fewer controls than
          was requested. If this is enabled, then fewer results than the
          requested amount will raise an error, and if `trim` is disabled, then
          more results than the requested amount will raise an error as well.
          Defaults to `True`.
        * `raise_on_zero`  (`bool`, optional): Whether to raise an error if no
          matching controls are found. This is to prevent errors when
          attempting to bind to a control when there aren't any matches at all.
          Defaults to `False`.
        * `one_type` (`bool`, optional): Whether the matches should be
          restricted so that they can only be from one subclass. This helps
          prevent mixing of different control groups if a controller has
          multiple controls of the same overarching type that should be
          addressed independently. Defaults to `True`.

        ### Raises:
        * `ValueError`: Not enough matching controls found, when `exact` is
          `True`.
        * `ValueError`: Too many matching controls, when `exact` is `True` and
          `trim` is `False`.
        * `ValueError`: No matching controls found (when `raise_on_zero` is
          True)

        ### Returns:
        * `ControlShadowList`: List of matches
        """
        # If we allow substitution, then search through all available types in
        # order
        if allow_substitution:
            sub_types = (control, *control.getControlAssignmentPriorities())
        else:
            sub_types = (control,)

        # List of the returned control surfaces
        ret: list[ControlShadow] = []
        # Final all the matches for each type one by one
        for t in sub_types:
            matches = self._getMatches(
                lambda x: isinstance(x, t),
                target_num,
                one_type,
            )
            # If this is the most matches we've found so far, set it as such
            if len(matches) > len(ret):
                ret = matches
            # And if we reached our target
            if target_num is not None and len(matches) >= target_num:
                break

        # Sort the matches based on coordinate
        def sort_key(c): return c.coordinate
        ret.sort(key=sort_key)

        # Make sure we have results
        if raise_on_zero and len(ret) == 0:
            raise ValueError(f"No matching controls found for type {control}")

        # If we have no target, ignore exact and trim parameters
        if target_num is None:
            return ControlShadowList(ret)

        if exact:
            if len(ret) < target_num:
                raise ValueError("Not enough matching controls found")
            elif trim:
                return ControlShadowList(ret[:target_num])
            else:
                if len(ret) > target_num:
                    raise ValueError("Too many matching controls found. "
                                     "Ensure you are using the trim flag "
                                     "correctly.")
                return ControlShadowList(ret)
        else:
            return ControlShadowList(ret)

    def getNumControlMatches(
        self,
        control: type[ControlSurface],
        allow_substitution: bool = True,
        one_type: bool = True,
    ) -> int:
        """
        Returns the number of controls matching the required type.

        A matching control is defined as inheriting from the given type, being
        a member of the same group as other matches, and which isn't already
        assigned.

        ### Args:
        * `control` (`type`): Type of control to match
        * `allow_substitution` (`bool`, optional): Whether substitutable
          controls should be allowed to be used if a better number of them are
          available. Defaults to `True`.
        * `one_type` (`bool`, optional): Whether the matches should be
          restricted so that they can only be from one subclass. This helps
          prevent mixing of different control groups if a controller has
          multiple controls of the same overarching type that should be
          addressed independently. Defaults to `True`.

        ### Returns:
        * `int`: number of types that match
        """
        return len(self.getControlMatches(
            control,
            allow_substitution,
            raise_on_zero=False,
            one_type=one_type,
        ))

    def bindControl(
        self,
        control: ControlShadow,
        on_event: Optional[EventCallback],
        on_tick: TickCallback = None,
        args: Optional[tuple] = None
    ) -> None:
        """
        Binds a callback function to a control, so the function will be called
        whenever that control is tweaked.

        ### Args:
        * `control` (`ControlShadow`): control to bind
        * `on_event` (`EventCallback`): callback function for events. Refer to
          EventCallback documentation for how this should be structured.
        * `on_tick` (`TickCallback`, optional): callback function for ticks.
          Refer to TickCallback documentation for how this should be
          structured. Defaults to None
        * `args` (`tuple`, optional): arguments to give to the callback
          functions. Defaults to `None` (no arguments).

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
        self._assigned_controls[control.getMapping()] = \
            (control, on_event, on_tick, args_)

    def bindControls(
        self,
        controls: ControlShadowList,
        on_event: EventCallback,
        on_tick: TickCallback = None,
        args_iterable: 'Optional[Iterable[tuple[Any, ...]] | ellipsis]'  # noqa: F821,E501
        = None
    ) -> None:
        """
        Binds a single function all controls in a list.

        This can be used for bulk assignment of controls.

        ### Args:
        * `controls` (`list[ControlShadow]`): List of controls to bind to
        * `bind_to` (`EventCallback`): callback function to bind. Refer to
          EventCallback documentation for how this should be structured.
        * `on_tick` (`TickCallback`): callback function for ticks. Refer to
          TickCallback documentation for how this should be structured.
        * `args_iterable` (`Iterable[tuple] | ellipsis`, optional): Iterable of
          arguments to pass to the function:
                * `None` (default): no arguments will be given.
                * `...`: indices of the controls (ie the first control in
                  the list will cause the callback to be given the argument
                  `0`).
                * `list[tuple]`: each control will be associated with the tuple
                  of arguments with the same index. Note that the list of
                  argument tuples will need to be at least of the same length
                  as the list of controls to bind. Any excess arguments will be
                  ignored.
                * `list[Any]`: each control will be associated with the a
                  single argument at that index. Note that the list of argument
                  tuples will need to be at least of the same length as the
                  list of controls to bind. Any excess arguments will be
                  ignored.
                * `Generator[tuple, None, None]`: the generator will be
                  iterated over in order to generate tuples of arguments for
                  each control. Note that this refers to a generator object,
                  not a generator function.

        ### Raises:
        * `ValueError`: Args list length not equal to controls list length
        * `ValueError`: Not all controls in controls list are free to bind to
        """
        # If ellipsis given for args iterable, generate index numbers
        if args_iterable is Ellipsis:
            args_iter: list[tuple] = [(i,) for i in range(len(controls))]
        # If args iterable is None, use empty args
        elif args_iterable is None:
            args_iter = [tuple() for _ in range(len(controls))]
        # Otherwise, check length
        else:
            try:
                # Ignore type checking, since we're in a try-except to avoid
                # the error anyway
                if len(args_iterable) < len(controls):  # type: ignore
                    raise ValueError("Args list must be of the same length as "
                                     "controls list")

                # Get rid of incorrect flag for ellipsis
                if TYPE_CHECKING:
                    assert not isinstance(
                        args_iterable, ellipsis  # noqa: F821
                    )
                args_iter = [a for a in args_iterable]
            except TypeError:
                # Iterable doesn't support len, assume it's infinite (ie a
                # generator)
                if TYPE_CHECKING:
                    assert isinstance(args_iterable, Generator)
                args_iter = [
                    a for _, a in zip(range(len(controls)), args_iterable)
                ]

        # If it's a list of non-tuples
        if isinstance(args_iter, list) and len(args_iter):
            if not isinstance(args_iter[0], tuple):
                # Convert it to a list of tuples
                for i in range(len(args_iter)):
                    args_iter[i] = (args_iter[i], )

        # Ensure all controls are assignable
        if not all(c in self._free_controls for c in controls):
            raise ValueError("All controls must be free to bind to")

        # Bind each control, using the index of it as the argument
        for c, a in zip(controls, args_iter):
            self.bindControl(c, on_event, on_tick, a)

    def bindMatch(
        self,
        control: type[ControlSurface],
        on_event: Optional[EventCallback],
        on_tick: TickCallback = None,
        args: Optional[tuple] = None,
        allow_substitution: bool = True,
        raise_on_failure: bool = False,
    ) -> IControlShadow:
        """
        Finds the first control of a matching type and binds it to the given
        function.

        ### Args:
        * `control` (`ControlSurface`): control type to bind
        * `bind_to` (`EventCallback`): callback function to bind. Refer to
          EventCallback documentation for how this should be structured.
        * `on_tick` (`TickCallback`): callback function for ticks. Refer to
          TickCallback documentation for how this should be structured.
        * `args` (`tuple`, optional): arguments to give to the callback
          function. Defaults to `None` (no arguments).
        * `allow_substitution` (`bool`, optional): whether the control can be
          substituted for a similar control. Defaults to `True`.
        * `raise_on_failure` (`bool`, optional): whether failure to assign the
          control should result in a `ValueError` being raised. When this is
          `False`, a NullControlShadow will be returned instead of a control
          shadow. Defaults to `False`.

        ### Raises:
        * `ValueError`: No controls were found to bind to (when
          `raise_on_failure` is `True`)

        ### Returns
        * `ControlShadow`: The control surface that was bound to, so that
          properties of it can be set.
        * `NullControlShadow`: if binding failed and `raise_on_failure` is
          `False`. This still allows dummy properties to be set, which can
          simplify the creation of simple plugins.
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
                return NullControlShadow()
        self.bindControl(match, on_event, on_tick, args)
        return match

    def bindMatches(
        self,
        control: type[ControlSurface],
        on_event: EventCallback,
        on_tick: TickCallback = None,
        args_generator: ArgGenerator = None,
        allow_substitution: bool = True,
        target_num: Optional[int] = None,
        trim: bool = True,
        exact: bool = True,
        raise_on_failure: bool = False,
        one_type: bool = True,
    ) -> ControlShadowList:
        """
        Finds all controls of a matching type and binds them to the given
        function.

        ### Args:
        * `control` (`ControlSurface`): control type to bind.
        * `bind_to` (`EventCallback`): callback function to bind. Refer to
          EventCallback documentation for how this should be structured.
        * `on_tick` (`TickCallback`): callback function for ticks. Refer to
          TickCallback documentation for how this should be structured.
        * `args_generator`: Iterable of arguments to pass to the function:
                * `None` (default): no arguments will be given.
                * `...`: indices of the controls (ie the first control in
                  the list will cause the callback to be given the argument
                  `0`).
                * `list[tuple[Any, ...]]`: each control will be associated with
                  the tuple of arguments with the same index. Note that the
                  list of argument tuples will need to be at least of the same
                  length as the list of controls to bind. Any excess arguments
                  will be ignored.
                * `list[Any]`: each control will be associated with the a
                  single argument at that index. Note that the list of argument
                  tuples will need to be at least of the same length as the
                  list of controls to bind. Any excess arguments will be
                  ignored.
                * `GeneratorFunction (list[ControlShadow]) -> Generator ->
                  tuple`: the generator will be iterated
                  over in order to generate tuples of arguments for each
                  control. Note that if the number of matches isn't guaranteed,
                  a generator should be used to get callback arguments.
        * `allow_substitution` (`bool`, optional): whether the control can be
          substituted for a similar control. Defaults to `True`.
        * `target_num` (`int`, optional): Number of matches to look for, to
          ensure we don't waste controls that can support more space. If not
          provided, the maximum sized group will be used. Note that fewer
          controls could be bound if not enough are available. To ensure an
          exact number, use bindMatchesExact(). Defaults to `None`.
        * `trim` (`bool`, optional): whether extra control surface results
          should be trimmed off. This may prevent errors when trying to assign
          a specific number of controls, but if many controls are wanted, then
          it can be disabled. Defaults to `True`.
        * `exact` (`bool`, optional): whether an exact number of controls
          should be required for the function call to be successful. If this is
          disabled, the function could potentially return fewer controls than
          was requested. If this is enabled, then fewer results than the
          requested amount will raise an error, and if `trim` is disabled, then
          more results than the requested amount will raise an error as well.
          Defaults to `True`.
        * `raise_on_failure` (`bool`, optional): whether failure to assign the
          control should result in a `ValueError` being raised. When this is
          `False`, an empty list will be returned instead. Defaults to `False`.
        * `one_type` (`bool`, optional): Whether the matches should be
          restricted so that they can only be from one subclass. This helps
          prevent mixing of different control groups if a controller has
          multiple controls of the same overarching type that should be
          addressed independently. Defaults to `True`.

        ### Raises:
        * `TypeError`: Potential bad number of callback arguments due to
          unknown number of controls being bound (ie. `exact` is `False`).
        * `ValueError`: No controls were found to bind to (when
          `raise_on_failure` is `True`)

        ### Returns:
        * `list[ControlSurface]`: List of controls bound successfully
        """

        # Ensure we don't risk having too few arguments to bind to
        if isinstance(args_generator, list) and not exact:
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
                exact,
                one_type=one_type
            )
        except ValueError as e:
            if raise_on_failure:
                raise ValueError(f"Error binding controls {control}") from e
            else:
                return ControlShadowList([])

        # Check for generator functions
        if not isinstance(args_generator, (list, type(...), type(None))):
            if TYPE_CHECKING:
                assert not isinstance(args_generator, ellipsis)  # noqa: F821
                assert args_generator is not None
            # Turn the generator function into a generator (which is iterable)
            iterable: 'Iterable[tuple[Any, ...]] | ellipsis | None'\
                = args_generator(matches)  # noqa: F821
        else:
            # Otherwise it's already iterable (or will be made so by the
            # bindControls() method)
            iterable = args_generator
        # Finally, bind all the controls
        self.bindControls(matches, on_event, on_tick, iterable)
        return matches

    def processEvent(self, control: ControlEvent, index: FlIndex) -> bool:
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
            control_shadow, fn, _, args = self._assigned_controls[control]
        except KeyError:
            # If we get a KeyError, the control isn't assigned and we should do
            # nothing
            if self._debug is not None:
                print(f"[DEBUG={self._debug}] {control} is not assigned")
            return False
        # If there is no callback, cancel
        if fn is None:
            return False
        # Set the value of the control as required
        control_shadow.value = control.value
        # Generate a control shadow mapping to send to the device
        mapping = ControlShadowEvent(control, control_shadow)
        if self._debug is not None:
            print(f"[DEBUG={self._debug}] {control} is assigned to {fn}")
        # Call the bound function with any extra required args
        return fn(mapping, index, *args)

    def tick(self, index: FlIndex) -> None:
        """
        Tick the assigned control surfaces of the plugin.

        ### Args:
        * `index` (`PluginIndex`): Index of channel or track/slot of the
          selected plugin
        """
        # Get control's mapping if it's assigned
        for control_shadow, _, fn, args in self._assigned_controls.values():
            # If a callback is defined
            if fn is not None:
                # Call the bound function with any extra required args
                fn(control_shadow, index, *args)

    def apply(self, thorough: bool) -> None:
        """
        Apply the configuration of the device shadow to the control it
        represents
        """
        if self._minimal or not thorough:
            controls = (c for c, *_ in self._assigned_controls.values())
        else:
            controls = (c for c in self._all_controls)
        for c in controls:
            c.apply()
