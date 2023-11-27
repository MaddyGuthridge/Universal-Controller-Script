"""
integrations > window > channel_rack > plug

Overall integration for channel rack

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""
from common.extension_manager import ExtensionManager
from common.plug_indexes import WindowIndex
from common.types import Color
from devices import DeviceShadow
from integrations import WindowIntegration, IntegrationPager
from integrations.mapping_strategies import MuteSoloStrategy
from .helpers import INDEX, getChannelRows
from .omni import OmniPreview
from .sequence import StepSequencer


class ChannelRack(IntegrationPager, WindowIntegration):
    """
    Used to process events directed at the channel rack
    """

    def __init__(self, shadow: DeviceShadow) -> None:
        IntegrationPager.__init__(self, shadow)
        self.addPage(StepSequencer(shadow.copy()), Color.fromRgb(0, 127, 255))
        self.addPage(OmniPreview(shadow.copy()), Color.fromRgb(127, 0, 255))
        MuteSoloStrategy(shadow, lambda i: getChannelRows()[i])
        WindowIntegration.__init__(self, shadow)

    @classmethod
    def getWindowId(cls) -> WindowIndex:
        return INDEX

    @classmethod
    def create(cls, shadow: DeviceShadow) -> 'WindowIntegration':
        return cls(shadow)


ExtensionManager.windows.register(ChannelRack)
