
from common.extension_manager import ExtensionManager
from devices import DeviceShadow
from plugs import WindowPlugin

INDEX = 3


class PianoRoll(WindowPlugin):
    """
    Used to process events directed at the piano-roll

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


ExtensionManager.windows.register(PianoRoll)
