
import plugins
from typing import Any
from common.types import Color
from common.extensionmanager import ExtensionManager
from common.util.apifixes import GeneratorIndex
from controlsurfaces import Fader
from controlsurfaces import ControlShadowEvent
from devices import DeviceShadow
from plugs import StandardPlugin
from plugs import eventfilters, tickfilters

FADER_START = 10
NUM_FADERS = 8


class Flex(StandardPlugin):
    """
    Used to interact with the Flex plugin
    """

    def __init__(self, shadow: DeviceShadow) -> None:
        self._faders = shadow.bindMatches(
            Fader,
            self.faders,
            target_num=NUM_FADERS,
            allow_substitution=True,
            raise_on_failure=False
        )
        super().__init__(shadow, [])

    @classmethod
    def create(cls, shadow: DeviceShadow) -> 'StandardPlugin':
        return cls(shadow)

    @tickfilters.toGeneratorIndex
    def tick(self, index: GeneratorIndex):
        if len(self._faders):
            for f, i in zip(
                self._faders, range(FADER_START, FADER_START+NUM_FADERS)
            ):
                annotation = plugins.getParamName(i, *index)
                active = annotation != "Not Used"
                f.annotation = annotation if active else ""
                f.color = Color.fromRgb(255, 140, 0) if active else Color()
                f.value = plugins.getParamValue(i, *index)

    @staticmethod
    def getPlugIds() -> tuple[str, ...]:
        return ("FLEX",)

    @eventfilters.toGeneratorIndex
    def faders(
        self,
        control: ControlShadowEvent,
        index: GeneratorIndex,
        *args: Any
    ) -> bool:
        plugins.setParamValue(control.value, FADER_START +
                              control.getShadow().coordinate[1], *index)
        return True


ExtensionManager.registerPlugin(Flex)
