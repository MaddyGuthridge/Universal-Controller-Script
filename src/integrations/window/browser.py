"""
integrations > window > browser

Integration for FL Studio's browser

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""
from common.extension_manager import ExtensionManager
from common.plug_indexes.window import WindowIndex
from devices import DeviceShadow
from integrations import WindowIntegration

INDEX = WindowIndex.BROWSER


class Browser(WindowIntegration):
    """
    Used to process events directed at the browser

    Currently empty: will expand in the future
    """

    def __init__(self, shadow: DeviceShadow) -> None:
        super().__init__(shadow)

    @classmethod
    def getWindowId(cls) -> WindowIndex:
        return INDEX

    @classmethod
    def create(cls, shadow: DeviceShadow) -> 'WindowIntegration':
        return cls(shadow)


ExtensionManager.windows.register(Browser)
