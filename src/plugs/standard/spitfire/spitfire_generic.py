
from typing import Any
import channels

import plugins
from common.types import Color
from common.extension_manager import ExtensionManager
from common.util.api_fixes import GeneratorIndex
from control_surfaces import ControlShadowEvent
from control_surfaces import Fader, DrumPad
from devices import DeviceShadow
from plugs import StandardPlugin
from plugs import event_filters, tick_filters

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
]
ORIGINALS = ['Originals - ' + ele for ele in ORIGINALS]

SUPPORTED_PLUGINS = tuple(PRIMARY + ORIGINALS)

BOUND_COLOR = Color.fromRgb(127, 127, 127)


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
        # Bind a different callback depending on drum pad size
        # TODO: Find a way to improve this, and reduce repeated code between
        # this and FPC
        size = shadow.getDevice().getDrumPadSize()
        if size[0] >= 4 and size[1] >= 8:
            self._pads = shadow.bindMatches(DrumPad, self.drumPad4x8)
            # TODO: Figure out the logic of this at some point
            self._coordToIndex = lambda r, c: 16 - (c + 1) * 4 + r
        if size[0] >= 4 and size[1] >= 4:
            self._pads = shadow.bindMatches(DrumPad, self.drumPad4x4)
            self._coordToIndex = lambda r, c: c + 4 * r
        elif size[0] >= 2 and size[1] >= 8:
            self._pads = shadow.bindMatches(DrumPad, self.drumPad2x8)
            self._coordToIndex = lambda r, c: c + 4 * r + 4 * (c >= 4)

        super().__init__(shadow, [])

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

    @event_filters.toGeneratorIndex()
    def drumPad4x8(
        self,
        control: ControlShadowEvent,
        index: GeneratorIndex,
        *args: Any
    ) -> bool:
        row, col = control.getShadow().coordinate
        # Handle pads out of bounds as well
        if row >= 4 or col >= 8:
            return True
        channels.midiNoteOn(index[0], self._coordToIndex(
            row, col), int(control.value * 127))
        return True

    @event_filters.toGeneratorIndex()
    def drumPad4x4(
        self,
        control: ControlShadowEvent,
        index: GeneratorIndex,
        *args: Any
    ) -> bool:
        row, col = control.getShadow().coordinate
        # Handle pads out of bounds as well
        if row >= 4 or col >= 4:
            return True
        channels.midiNoteOn(index[0], self._coordToIndex(
            row, col), int(control.value * 127))
        return True

    @event_filters.toGeneratorIndex()
    def drumPad2x8(
        self,
        control: ControlShadowEvent,
        index: GeneratorIndex,
        *args: Any
    ) -> bool:
        row, col = control.getShadow().coordinate
        # Handle pads out of bounds
        if row >= 2 or col >= 8:
            return True
        channels.midiNoteOn(index[0], self._coordToIndex(
            row, col), int(control.value * 127))
        return True


ExtensionManager.plugins.register(SpitfireGeneric)
