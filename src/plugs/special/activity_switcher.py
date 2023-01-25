"""
plugs > special > activity_switcher

Contains the definition for the activity switcher plugin

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""
import channels
import mixer
import ui

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
        return Color.fromGrayscale(0.3)
    else:
        if len(activity) == 1:
            # Generator -> channel color
            return Color.fromInteger(channels.getChannelColor(*activity))
        else:
            # Effect -> track color
            return Color.fromInteger(mixer.getTrackColor(activity[0]))


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
            return channels.getChannelName(*activity)
        else:
            return mixer.getTrackName(activity[0])


def triggerActivity(activity: SafeIndex):
    """
    Triggers the given activity

    ### Args:
    * `activity` (`SafeIndex`): activity to open
    """
    if isinstance(activity, int):
        ui.showWindow(activity)
    else:
        if len(activity) == 1:
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
