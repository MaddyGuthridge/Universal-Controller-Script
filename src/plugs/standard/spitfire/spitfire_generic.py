"""
plugs > standard > spitfire > spitfire_generic

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""
from typing import Any
import channels

import plugins
from common.types import Color
from common.extension_manager import ExtensionManager
from common.plug_indexes import GeneratorIndex
from control_surfaces import ControlShadowEvent
from control_surfaces import Fader
from devices import DeviceShadow
from plugs import StandardPlugin
from plugs import event_filters, tick_filters
from plugs.mapping_strategies import DrumPadStrategy

# Generate list of supported plugins
# HELP WANTED: I don't own all of these libraries, so the naming may be
# incorrect. If something doesn't work, please create a bug report.
# This is also far from an exhaustive list of all the available plugins, so
# if any you use are missing, let me know!
PRIMARY = [
    'BBC Symphony Orchestra',  # Working
    'LABS',  # Working
    'Abbey Road One',  # Working
    'Eric Whitacre Choir',
    'Hans Zimmer Strings',
    'Abbey Road Two',
    'Appassionata Strings',
    'Polaris',
    'Heirloom',
    'Hammers',
    'Fink Signatures',
]

ORIGINALS = [
    'Media Toolkit',  # Working
    'Cinematic Percussion',  # Working
    'Firewood Piano',  # Working
    'Cinematic Soft Piano',  # Working
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
    'Intimate Grand Piano',
    'Epic Choir',  # Working
]
ORIGINALS = ['Originals - ' + ele for ele in ORIGINALS]

SUPPORTED_PLUGINS = tuple(PRIMARY + ORIGINALS)

BOUND_COLOR = Color.fromRgb(127, 127, 127)


@event_filters.toGeneratorIndex(False)
def trigger(
    control: ControlShadowEvent,
    ch_idx: GeneratorIndex,
    pad_idx: int,
) -> bool:
    channels.midiNoteOn(ch_idx[0], pad_idx, int(control.value * 127))
    return True


class SpitfireGeneric(StandardPlugin):
    """
    Used to interact with Spitfire Audio plugins, mapping faders to parameters
    """
    def __init__(self, shadow: DeviceShadow) -> None:
        self._faders = shadow.bindMatches(
            Fader,
            self.faders,
            target_num=2,
        )

        if len(self._faders) == 2:
            # Set annotation and colors once (since they won't change)
            self._faders[0] \
                .annotate("Expression") \
                .colorize(BOUND_COLOR)
            self._faders[1] \
                .annotate("Dynamics") \
                .colorize(BOUND_COLOR)

        # Drum pads
        drums = DrumPadStrategy(4, 2, False, trigger)
        super().__init__(shadow, [drums])

    @classmethod
    def create(cls, shadow: DeviceShadow) -> 'StandardPlugin':
        return cls(shadow)

    @classmethod
    def getPlugIds(cls) -> tuple[str, ...]:
        return SUPPORTED_PLUGINS

    @tick_filters.toGeneratorIndex()
    def tick(self, index: GeneratorIndex):
        # self._faders[0].value = plugins.getParamValue(0, *index)
        # self._faders[1].value = plugins.getParamValue(1, *index)
        pass

    @event_filters.toGeneratorIndex()
    def faders(
        self,
        control: ControlShadowEvent,
        index: GeneratorIndex,
        *args: Any
    ) -> bool:
        plugins.setParamValue(
            control.value, control.getShadow().coordinate[1], *index)
        return True


ExtensionManager.plugins.register(SpitfireGeneric)
