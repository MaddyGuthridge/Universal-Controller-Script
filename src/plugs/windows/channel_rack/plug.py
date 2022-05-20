
from common.extension_manager import ExtensionManager
from common.types import Color
from devices import DeviceShadow
from plugs import WindowPlugin, PluginPager
from .helpers import INDEX
from .omni import OmniPreview
from .sequence import StepSequencer


class ChannelRack(PluginPager, WindowPlugin):
    """
    Used to process events directed at the channel rack
    """

    def __init__(self, shadow: DeviceShadow) -> None:
        PluginPager.__init__(self, shadow)
        self.addPage(StepSequencer(shadow.copy()), Color.fromRgb(0, 127, 255))
        self.addPage(OmniPreview(shadow.copy()), Color.fromRgb(127, 0, 255))
        WindowPlugin.__init__(self, shadow, [])

    @staticmethod
    def getWindowId() -> int:
        return INDEX

    @classmethod
    def create(cls, shadow: DeviceShadow) -> 'WindowPlugin':
        return cls(shadow)


ExtensionManager.windows.register(ChannelRack)
