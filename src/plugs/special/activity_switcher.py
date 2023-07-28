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
from common.extension_manager import ExtensionManager
from common import getContext
from common.types import Color
from common.plug_indexes import (
    FlIndex,
    GeneratorIndex,
    WindowIndex,
    EffectIndex,
)
from control_surfaces import (
    ActivitySwitcher as ActivitySwitchControl,
    ControlShadowEvent,
    ControlShadow,
)
from devices import DeviceShadow
from plugs import SpecialPlugin
from plugs.event_filters import filterButtonLift


def getActivityColor(activity: FlIndex) -> Color:
    """
    Returns the color associated with a particular activity

    ### Args:
    * `activity` (`SafeIndex`): activity

    ### Returns:
    * `Color`: color
    """
    if isinstance(activity, WindowIndex):
        return Color.ENABLED
    else:
        if isinstance(activity, GeneratorIndex):
            # Generator -> channel color
            try:
                return activity.channel.color
            except TypeError:
                # Prevent issues if we deleted stuff
                return Color.BLACK
        else:
            assert isinstance(activity, EffectIndex)
            # Effect -> track color
            try:
                return activity.track.color
            except TypeError:
                return Color.BLACK


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
            getContext().activity.getHistoryActivity(c_index).focus()
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
            control.annotation = activity.getName()
        except IndexError:
            pass


ExtensionManager.super_special.register(ActivitySwitcher)
