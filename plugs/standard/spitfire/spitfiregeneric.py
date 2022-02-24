
from typing import Any

import plugins
from common.extensionmanager import ExtensionManager
from common.util.apifixes import GeneratorIndex
from controlsurfaces import ControlShadowEvent
from controlsurfaces import Fader
from devices import DeviceShadow
from plugs import StandardPlugin
from plugs import eventfilters, tickfilters

# Generate list of supported plugins
# HELP WANTED: I don't own all of these libraries, so the naming may be
# incorrect. If something doesn't work, please create a bug report.
PRIMARY = [
    'BBC Symphony Orchestra',
    'LABS',
    'Abbey Road One',
    'Eric Whitacre Choir',
    'Hans Zimmer Strings'
]

ORIGINALS = [
    'Media Toolkit',
    'Cinematic Percussion',
    'Firewood Piano',
    'Cinematic Soft Piano',
    'Cinematic Frozen Strings',
    'Jangle Box Piano',
    'Cinematic Pads',
    'Mrs Mills Piano',
    'Cimbalom',
    'Drumline',
    'Intimate Strings',
    'Epic Strings',
    'Epic Brass & Woodwinds',
    'Felt Piano',
]
ORIGINALS = ['Originals - '+ele for ele in ORIGINALS]

SUPPORTED_PLUGINS = tuple(PRIMARY + ORIGINALS)


class SpitfireGeneric(StandardPlugin):
    """
    Used to interact with Spitfire Audio plugins, mapping faders to parameters
    """
    def __init__(self, shadow: DeviceShadow) -> None:
        shadow.bindMatches(
            Fader, self.faders, ..., target_num=2, raise_on_failure=False)
        super().__init__(shadow, [])
    
    @classmethod
    def create(cls, shadow: DeviceShadow) -> 'StandardPlugin':
        return cls(shadow)
    
    @staticmethod
    def getPlugIds() -> tuple[str, ...]:
        return SUPPORTED_PLUGINS

    @tickfilters.filterToGeneratorIndex
    def tick(self, index: GeneratorIndex):
        pass

    @eventfilters.filterToGeneratorIndex
    def faders(self, control: ControlShadowEvent, index: GeneratorIndex, idx: int, *args: Any) -> bool:
        plugins.setParamValue(control.value, control.getShadow().coordinate[1], *index)
        return True

ExtensionManager.registerPlugin(SpitfireGeneric)
