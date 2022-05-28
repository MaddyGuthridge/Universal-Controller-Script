
from common.extension_manager import ExtensionManager
from devices import DeviceShadow
from plugs import WindowPlugin

INDEX = 4


class Browser(WindowPlugin):
    """
    Used to process events directed at the browser

    Currently empty: will expand in the future
    """

    def __init__(self, shadow: DeviceShadow) -> None:
        super().__init__(shadow, [])

    @classmethod
    def getWindowId(cls) -> int:
        return INDEX

    @classmethod
    def create(cls, shadow: DeviceShadow) -> 'WindowPlugin':
        return cls(shadow)


ExtensionManager.windows.register(Browser)
