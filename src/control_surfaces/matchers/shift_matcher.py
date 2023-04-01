"""
devices > shift_matcher

Defines a ShiftMatcher interface for matching different events depending on
whether a shift button is active or not.

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""
from typing import Optional
from fl_classes import FlMidiMsg
from common.types import Color
from control_surfaces import ControlEvent, ControlSurface, NullControl
from ..event_patterns import TruePattern
from . import IControlMatcher


class ShiftView:
    """
    Represents a view within the shift matcher
    """
    def __init__(
        self,
        trigger: ControlSurface,
        view: IControlMatcher,
        /,
        latch: bool = False,
        ignore_single_press: bool = False,
        disable_in_other_views: bool = False,
        allow_fallback_match: bool = True,
        debug: bool = False,
    ) -> None:
        """
        Create a ShiftView for use within a ShiftMatcher

        ### Args:
        * `trigger` (`ControlSurface`): control to use when triggering the
          shift view

        * `view` (`IControlMatcher`): the view to trigger when the shift button
          is active

        * `latch` (`bool`, options): whether to make the view be a toggle
          rather than a pulse. This is incompatible with the
          `ignore_single_press` flag. Defaults to `False`.

        * `ignore_single_press` (`bool`, optional): whether to ignore single
          press triggers. If this is `True`, a double press will be used to
          open the shift view. This is incompatible with the `latch` flag.
          Defaults to `False`.

        * `disable_in_other_views` (`bool`, optional): whether to prevent this
          view from being activated if another view is active. This should be
          used if its trigger is also a control in another view. Defaults to
          `False`.

        * `allow_fallback_match` (`bool`, optional): whether to allow events to
          match with the main view if they don't match with this view. Defaults
          to `True`.

        * `debug` (`bool`, optional): whether to print out debugging
          information about this view.
        """
        if latch and ignore_single_press:
            raise ValueError(
                "latch and ignore_single_press parameters are incompatible")

        self.trigger = trigger
        self.view = view
        self.latch = latch
        self.ignore_single_press = ignore_single_press
        self.disable_in_other_views = disable_in_other_views
        self.allow_fallback_match = allow_fallback_match
        self.debug = debug

    def __repr__(self) -> str:
        return f"ShiftView({self.trigger})"


class ShiftMatcher(IControlMatcher):
    """
    Allows controls to be designated as a "shift" button, so that pressing
    them switches between various sub control matchers.

    Note that these buttons are still matched normally, so their events can
    still be handled by plugins. If no action should be taken when pressing a
    button, it should be registered as a NullEvent.

    In order to modify the LED of the shift button, ControlSurfaces should
    determine whether the button is pressed using the onValueChange callback.
    This also implements the behavior of the double pressed shift button.
    """
    def __init__(
        self,
        main_view: IControlMatcher,
        views: list[ShiftView],
    ) -> None:
        """
        Create a shift control matcher

        ### Args:
        * `main_view` (`IControlMatcher`): layer to use when no shift menus are
          active

        * `views` (`list[ShiftView]`): list of views to control with this
          matcher
        """
        self.__null = NullControl(TruePattern())
        self.__main = main_view
        self.__views = views
        self.__active_view: Optional[ShiftView] = None

        # Whether the previous press was a double press
        self.__sustained = False
        # Whether we need to do a thorough tick
        self.__changed = True
        super().__init__()

    def matchEvent(self, event: FlMidiMsg) -> Optional[ControlEvent]:
        # Check to see if we can trigger a view
        for view in self.__views:
            # Skip this view if required
            if (
                self.__active_view is not None
                and self.__active_view is not view
                and view.disable_in_other_views
            ):
                continue

            # If it matches the view's trigger
            if (control := view.trigger.match(event)) is not None:
                # If the view should latch, handle that
                if view.latch:
                    if control.value != 0:
                        if self.__active_view is view:
                            self.__active_view = None
                            view.trigger.color = Color.DISABLED
                        else:
                            self.__active_view = view
                            view.trigger.color = Color.ENABLED
                        self.__changed = True
                    return control

                # If it's a lift, match the event
                # but only deactivate a view if it's the right view
                if control.value == 0:
                    if self.__active_view is view:
                        # Only deactivate if we're not sustaining it
                        if self.__sustained:
                            self.__sustained = False
                            # Keep the value enabled
                            view.trigger.value = 1.0
                            view.trigger.color = Color.ENABLED
                            if view.debug:
                                print(f"sustain {view}")
                        else:
                            self.__changed = True
                            self.__active_view = None
                            view.trigger.color = Color.DISABLED
                            if view.debug:
                                print(f"disable {view}")
                    return control

                # If the menu is already open, this should be a null event
                if self.__active_view is view:
                    return self.__null.match(event)

                # If it's a double press, trigger the sustained menu
                if control.double:
                    if view.debug:
                        print(f"enable (sustained) {view}")
                    self.__sustained = True
                else:
                    # If this menu requires a double press, don't use it
                    if view.ignore_single_press:
                        if view.debug:
                            print(f"ignored (required double press) {view}")
                        return control
                    else:
                        if view.debug:
                            print(f"enable {view}")
                # Open the menu
                self.__active_view = view
                view.trigger.color = Color.ENABLED
                self.__changed = True
                return control

        if self.__active_view is not None:
            if (m := self.__active_view.view.matchEvent(event)) is not None:
                if self.__active_view.debug:
                    print(f"event matched by {view}")
                return m
            else:
                if view.allow_fallback_match:
                    if self.__active_view.debug:
                        print("event matched by main view (fallback)")
                    return self.__main.matchEvent(event)
                else:
                    return None
        else:
            # print("event matched by main view (fallback)")
            return self.__main.matchEvent(event)

    def getControls(self) -> list[ControlSurface]:
        controls = list(self.__main.getControls())
        for view in self.__views:
            controls.append(view.trigger)
            controls.extend(view.view.getControls())
        return controls

    def tick(self, thorough: bool) -> None:
        if self.__changed:
            thorough = True
            self.__changed = False
        # Colorize and tick each view trigger
        for view in self.__views:
            # Skip this view if required
            if self.__active_view is not view and view.disable_in_other_views:
                continue
            # Only color NullControls
            if isinstance(view.trigger, NullControl):
                view.trigger.color = (
                    Color.ENABLED
                    if self.__active_view is view
                    else Color.DISABLED
                )
            view.trigger.doTick(thorough)

        # Tick whichever sub-matcher is active (but don't tick the non-active
        # one or we might cause clashing colors)
        if self.__active_view is None:
            # if thorough:
            #     print("tick main thorough")
            self.__main.tick(thorough)
        else:
            # if thorough:
            #     print("tick active thorough")
            self.__active_view.view.tick(thorough)
