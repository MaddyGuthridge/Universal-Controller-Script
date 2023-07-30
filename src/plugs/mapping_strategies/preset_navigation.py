"""
plugs > mapping_strategies > preset_navigation
"""
from common.util.api_fixes import PluginIndex
from control_surfaces import (
    DirectionNext,
    DirectionPrevious,
    ControlShadowEvent,
)
from devices import DeviceShadow
from plugs.event_filters import toPluginIndex, filterButtonLift
from .mapping_strategy import IMappingStrategy


class PresetNavigationStrategy(IMappingStrategy):
    """
    Mapping strategy that provides bindings for next/previous buttons
    """
    def __init__(self) -> None:
        super().__init__()

    def apply(self, shadow: DeviceShadow) -> None:
        shadow.bindMatch(DirectionNext, self.eDirectionNext)
        shadow.bindMatch(DirectionPrevious, self.eDirectionPrev)

    @filterButtonLift()
    @toPluginIndex()
    def eDirectionNext(
        self,
        control: ControlShadowEvent,
        index: PluginIndex,
        *args,
    ) -> bool:
        index.presetNext()
        return True

    @filterButtonLift()
    @toPluginIndex()
    def eDirectionPrev(
        self,
        control: ControlShadowEvent,
        index: PluginIndex,
        *args,
    ) -> bool:
        index.presetPrevious()
        return True
