"""
integrations > plugin > spitfire > spitfire_generic

Generic integration for Spitfire Audio plugins

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""
from typing import Any
import channels

from common.param import Param
from common.types import Color
from common.extension_manager import ExtensionManager
from common.plug_indexes import GeneratorIndex
from common.util.grid_mapper import GridCell
from control_surfaces import ControlShadowEvent
from control_surfaces import Fader
from devices import DeviceShadow
from integrations import PluginIntegration
from integrations import event_filters, tick_filters
from integrations.mapping_strategies import GridStrategy

# Params

EXPRESSION = Param(0)
DYNAMICS = Param(1)
FADER_PARAMS = [EXPRESSION, DYNAMICS]


# Generate list of supported plugins

# HELP WANTED: I don't own all of these libraries, so the naming may be
# incorrect. If something doesn't work, please create a bug report.
# This is also far from an exhaustive list of all the available plugins, so
# if any you use are missing, let me know!

# Main plugins
PRIMARY = [
    'LABS',  # Working
    'Polaris',
    'Fink Signatures',
]

# Main plugins using keyswitches
PRIMARY_KEYSWITCHES = [
    'BBC Symphony Orchestra',  # Working
    'Abbey Road One',  # Working
    'Eric Whitacre Choir',
    'Hans Zimmer Strings',
    'Abbey Road Two',
    'Appassionata Strings',
    'Heirloom',
    'Hammers',
]

# Originals (as far as I know, none use keyswitches)
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
SUPPORTED_KEYSWITCH_PLUGINS = tuple(PRIMARY_KEYSWITCHES)

BOUND_COLOR = Color.fromRgb(127, 127, 127)


@event_filters.toGeneratorIndex(False)
def trigger(
    control: ControlShadowEvent,
    ch_idx: GeneratorIndex,
    pad_idx: GridCell,
) -> bool:
    channels.midiNoteOn(
        ch_idx.index,
        pad_idx.overall_index,
        int(control.value * 127)
    )
    return True


class SpitfireGeneric(PluginIntegration):
    """
    Used to interact with Spitfire Audio plugins, mapping faders to parameters
    """
    def __init__(self, shadow: DeviceShadow) -> None:
        # FIXME: This can probably be done using `SimpleFaders`, which would be
        # much cleaner and more readable
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
        super().__init__(shadow)

    @classmethod
    def create(cls, shadow: DeviceShadow) -> 'PluginIntegration':
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
        FADER_PARAMS[control.getShadow().coordinate[1]](index).value \
            = control.value
        return True


class SpitfireKeyswitch(SpitfireGeneric):
    """
    A version of the Spitfire Audio generic plugin with support for
    keyswitches.
    """
    def __init__(self, shadow: DeviceShadow) -> None:
        GridStrategy(shadow, 4, 2, trigger, do_property_update=False)
        super().__init__(shadow)

    @classmethod
    def create(cls, shadow: DeviceShadow) -> 'PluginIntegration':
        return cls(shadow)

    @classmethod
    def getPlugIds(cls) -> tuple[str, ...]:
        return SUPPORTED_KEYSWITCH_PLUGINS


ExtensionManager.plugins.register(SpitfireGeneric)
ExtensionManager.plugins.register(SpitfireKeyswitch)
