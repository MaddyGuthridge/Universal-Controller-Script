"""
common > mainstate

Represents the script in its main state, where the device is recognised and
behaving as expected.
"""

import plugins

from common import log, verbosity
from common.extensionmanager import ExtensionManager
from common.types import eventData
from common.util.apifixes import getFocusedPluginIndex
from common.util.events import eventToString
from devices import Device
from .scriptstate import IScriptState

class MainState(IScriptState):
    """
    Represents the main state of the script, where the device is recognised and
    behaving as expected.
    """
    
    def __init__(self, device: Device) -> None:
        self._device = device
    
    def initialise(self) -> None:
        pass
    
    def tick(self) -> None:
        self._device.tick()

    def processEvent(self, event: eventData) -> None:
        mapping = self._device.matchEvent(event)
        
        if mapping is None:
            event.handled = True
            log(
                "device.event.in",
                f"Failed to recognise event: {eventToString(event)}",
                verbosity.CRITICAL,
                "This usually means that the device hasn't been configured "
                "correctly. Please contact the device's maintainer."
            )
            # raise ValueError(f"Couldn't identify event: {eventToString(event)}")
            
        else:
            log("device.event.in", f"Recognised event: {mapping.getControl()}", verbosity.NOTE)
        
        # Get active standard plugin
        plug_idx = getFocusedPluginIndex()
        if plug_idx is not None:
            plug_id = plugins.getPluginName(*plug_idx)
            plug = ExtensionManager.getPluginById(plug_id, self._device)
            if plug is not None:
                if plug.processEvent(mapping, plug_idx):
                    event.handled = True
                    return

        # Get special plugins
        for p in ExtensionManager.getSpecialPlugins(self._device):
            if p.processEvent(mapping, plug_idx):
                event.handled = True
                return
