"""
plugs > special > activity_switcher

Contains the definition for the activity switcher plugin

## Limitations

Currently doesn't handle cases where plugins have been rearranged, which may
lead to confusing behavior.

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""
import channels
import mixer
import ui
import plugins

from common.extension_manager import ExtensionManager
from common import getContext
from common.consts import WINDOW_NAMES
from common.types import Color
from common.plug_indexes import SafeIndex
from control_surfaces import (
    ActivitySwitcher as ActivitySwitchControl,
    ControlShadowEvent,
    ControlShadow,
)
from devices import DeviceShadow
from plugs import SpecialPlugin
from plugs.event_filters import filterButtonLift


def getActivityColor(activity: SafeIndex) -> Color:
    """
    Returns the color associated with a particular activity

    ### Args:
    * `activity` (`SafeIndex`): activity

    ### Returns:
    * `Color`: color
    """
    if isinstance(activity, int):
        return Color.ENABLED
    else:
        if len(activity) == 1:
            # Generator -> channel color
            try:
                return Color.fromInteger(channels.getChannelColor(*activity))
            except (TypeError, RuntimeError):
                # Prevent issues if we deleted stuff
                return Color.BLACK
        else:
            # Effect -> track color
            try:
                return Color.fromInteger(mixer.getTrackColor(activity[0]))
            except (TypeError, RuntimeError):
                return Color.BLACK


def getActivityName(activity: SafeIndex) -> str:
    """
    Returns the name associated with a particular activity

    ### Args:
    * `activity` (`SafeIndex`): activity

    ### Returns:
    * `str`: name of activity
    """
    if isinstance(activity, int):
        return WINDOW_NAMES[activity]
    else:
        if len(activity) == 1:
            try:
                return channels.getChannelName(*activity)
            except (TypeError, RuntimeError):
                # Prevent issues if we deleted stuff
                return ""
        else:
            try:
                return (
                    # Mypy really should support tuple unpacking properly
                    f"{mixer.getTrackName(activity[0])}: "  # type: ignore
                    f"{plugins.getPluginName(*activity, True)}"
                )
            except (TypeError, RuntimeError):
                # Prevent issues if we deleted stuff
                return ""


def triggerActivity(activity: SafeIndex):
    """
    Triggers the given activity

    ### Args:
    * `activity` (`SafeIndex`): activity to open
    """
    if isinstance(activity, int):
        getContext().activity.ignoreNextHistory()
        ui.showWindow(activity)
    else:
        if len(activity) == 1:
            getContext().activity.ignoreNextHistory()
            channels.focusEditor(activity[0])
        else:
            print("Would select effects")


class ActivitySwitcher(SpecialPlugin):
    @classmethod
    def shouldBeActive(cls) -> bool:
        return True

    @classmethod
    def create(cls, shadow: DeviceShadow) -> 'SpecialPlugin':
        return cls(shadow)

    def __init__(self, shadow: DeviceShadow) -> None:
        shadow.setMinimal(True)
        shadow.bindMatches(
            ActivitySwitchControl,
            self.eActivity,
            self.tActivity,
            args_generator=...,
        )
        super().__init__(shadow, [])

    @filterButtonLift()
    def eActivity(
        self,
        control: ControlShadowEvent,
        _,
        c_index: int,
    ) -> bool:
        try:
            triggerActivity(getContext().activity.getHistoryActivity(c_index))
        except IndexError:
            pass
        return True

    def tActivity(
        self,
        control: ControlShadow,
        _,
        c_index: int,
    ):
        try:
            activity = getContext().activity.getHistoryActivity(c_index)
            control.color = getActivityColor(activity)
            control.annotation = getActivityName(activity)
        except IndexError:
            pass


ExtensionManager.super_special.register(ActivitySwitcher)
