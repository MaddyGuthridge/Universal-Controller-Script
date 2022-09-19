"""
plugs > mapping_strategies > preset_navigation
"""
import plugins
from common.util.api_fixes import PluginIndex
from control_surfaces import (
    DirectionNext,
    DirectionPrevious,
    ControlShadowEvent,
)
from devices import DeviceShadow
from plugs.event_filters import toPluginIndex
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

    @toPluginIndex()
    def eDirectionNext(
        self,
        control: ControlShadowEvent,
        index: PluginIndex,
        *args,
    ) -> bool:
        plugins.nextPreset(*index)
        return True

    @toPluginIndex()
    def eDirectionPrev(
        self,
        control: ControlShadowEvent,
        index: PluginIndex,
        *args,
    ) -> bool:
        plugins.prevPreset(*index)
        return True
