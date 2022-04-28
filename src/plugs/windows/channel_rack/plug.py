
from common.extensionmanager import ExtensionManager
from devices import DeviceShadow
from plugs import WindowPlugin, PluginPager
from .helpers import INDEX
from .omni import OmniPreview


class ChannelRack(PluginPager, WindowPlugin):
    """
    Used to process events directed at the channel rack
    """

    def __init__(self, shadow: DeviceShadow) -> None:
        WindowPlugin.__init__(self, shadow, [])
        PluginPager.__init__(self)
        self.addPage(OmniPreview(shadow.copy()))

    @staticmethod
    def getWindowId() -> int:
        return INDEX

    @classmethod
    def create(cls, shadow: DeviceShadow) -> 'WindowPlugin':
        return cls(shadow)


ExtensionManager.registerWindowPlugin(ChannelRack)
