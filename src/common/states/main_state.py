"""
common > main_state

Represents the script in its main state, where the device is recognized and
behaving as expected.

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""

from typing import TYPE_CHECKING

import common
from common import ProfilerContext, profilerDecoration
from common import log, verbosity
from fl_classes import FlMidiMsg
from common.plug_indexes import PluginIndex, WindowIndex
from common.util.events import eventToString
from .dev_state import DeviceState

if TYPE_CHECKING:
    from devices import Device


class MainState(DeviceState):
    """
    Represents the main state of the script, where the device is recognized
    and behaving as expected.
    """

    def __init__(self, device: 'Device') -> None:
        if device.getDeviceNumber() != 1:
            raise ValueError(
                "Non-main devices should be configured to use the 'Universal "
                "Event Forwarder' script, rather than the main 'Universal "
                "Controller' script"
            )
        common.getContext().registerDevice(device)
        self._device = device

    @classmethod
    def create(cls, device: 'Device') -> 'DeviceState':
        return cls(device)

    def initialize(self) -> None:
        self._device.initialize()

    def deinitialize(self) -> None:
        pass

    @profilerDecoration("main.tick")
    def tick(self) -> None:
        # Get the currently active plugin
        with ProfilerContext("getActive"):
            plug_idx = common.getContext().activity.getActive()
            changed = common.getContext().activity.hasChanged()

        # Tick special plugins
        for p in common.ExtensionManager.special.get(self._device):
            if p.shouldBeActive():
                with ProfilerContext(f"tick-{type(p).__name__}"):
                    p.doTick(plug_idx)
                with ProfilerContext(f"apply-{type(p).__name__}"):
                    # Special plugins should always be thoroughly applied
                    # TODO: Find out why
                    p.apply(thorough=True)

        # Tick active standard plugin or window
        if isinstance(plug_idx, PluginIndex):
            try:
                plug_id = plug_idx.getName()
            except TypeError:
                # Plugin not valid
                plug_id = ""
            plug = common.ExtensionManager.plugins.get(
                plug_id, self._device
            )
            if plug is not None:
                with ProfilerContext(f"tick-{type(plug).__name__}"):
                    plug.doTick(plug_idx)
                with ProfilerContext(f"apply-{type(plug).__name__}"):
                    plug.apply(thorough=changed)
        else:
            assert isinstance(plug_idx, WindowIndex)
            window = common.ExtensionManager.windows.get(
                plug_idx, self._device
            )
            if window is not None:
                with ProfilerContext(f"tick-{type(window).__name__}"):
                    window.doTick(plug_idx)
                with ProfilerContext(f"apply-{type(window).__name__}"):
                    window.apply(thorough=changed)

        # Tick final special plugins
        for p in common.ExtensionManager.super_special.get(self._device):
            if p.shouldBeActive():
                with ProfilerContext(f"tick-{type(p).__name__}"):
                    p.doTick(plug_idx)
                with ProfilerContext(f"apply-{type(p).__name__}"):
                    p.apply(thorough=True)

        # Tick the device
        self._device.doTick()

    @profilerDecoration("main.processEvent")
    def processEvent(self, event: FlMidiMsg) -> None:
        with ProfilerContext("match-event"):
            mapping = self._device.matchEvent(event)
        if mapping is None:
            event.handled = True
            log(
                "device.event.in",
                f"Failed to recognize event: {eventToString(event)}",
                verbosity.CRITICAL,
                "This usually means that the device hasn't been configured "
                "correctly. Please contact the device's maintainer."
            )
            # raise ValueError(
            #     f"Couldn't identify event: "
            #     f"{eventToString(event)}"
            # )
            return

        log(
            "device.event.in",
            f"Recognized event: {mapping.getControl()}",
            verbosity.EVENT,
            detailed_msg=eventToString(event)
        )

        # Get active standard plugin
        plug_idx = common.getContext().activity.getActive()

        # Process for super special plugins
        for p in (common.ExtensionManager.super_special.get(self._device)):
            if p.shouldBeActive():
                with ProfilerContext(f"process-{type(p).__name__}"):
                    if p.processEvent(mapping, plug_idx):
                        event.handled = True
                        return

        if isinstance(plug_idx, PluginIndex):
            try:
                plug_id = plug_idx.getName()
            except TypeError:
                # Plugin not valid
                plug_id = ""
            plug = common.ExtensionManager.plugins.get(
                plug_id, self._device
            )
            if plug is not None:
                with ProfilerContext(f"process-{type(plug).__name__}"):
                    if plug.processEvent(mapping, plug_idx):
                        event.handled = True
                        return
        else:
            assert isinstance(plug_idx, WindowIndex)
            window = common.ExtensionManager.windows.get(
                plug_idx, self._device
            )
            if window is not None:
                with ProfilerContext(f"process-{type(window).__name__}"):
                    if window.processEvent(mapping, plug_idx):
                        event.handled = True
                        return

        # Process for special plugins
        for p in (common.ExtensionManager.special.get(self._device)):
            if p.shouldBeActive():
                with ProfilerContext(f"process-{type(p).__name__}"):
                    if p.processEvent(mapping, plug_idx):
                        event.handled = True
                        return
