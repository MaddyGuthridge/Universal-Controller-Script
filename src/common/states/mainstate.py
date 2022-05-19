"""
common > mainstate

Represents the script in its main state, where the device is recognised and
behaving as expected.
"""

import plugins
from typing import TYPE_CHECKING

import common
from common import ProfilerContext, profilerDecoration
from common import log, verbosity
from common.types import EventData
from common.util.events import eventToString
from .devstate import DeviceState

if TYPE_CHECKING:
    from devices import Device


class MainState(DeviceState):
    """
    Represents the main state of the script, where the device is recognised
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

    def initialise(self) -> None:
        self._device.initialise()

    def deinitialise(self) -> None:
        pass

    @profilerDecoration("main.tick")
    def tick(self) -> None:
        # Get the currently active plugin
        with ProfilerContext("getActive"):
            plug_idx = common.getContext().active.getActive()
            changed = common.getContext().active.hasChanged()

        # Tick special plugins
        for p in common.ExtensionManager.special.get(self._device):
            if p.shouldBeActive():
                with ProfilerContext(f"Tick {type(p)}"):
                    p.doTick(plug_idx)
                with ProfilerContext(f"Apply {type(p)}"):
                    # Special plugins should always be thoroughly applied
                    # TODO: Find out why
                    p.apply(thorough=True)

        # Tick active standard plugin or window
        if plug_idx is not None:
            if isinstance(plug_idx, tuple):
                try:
                    plug_id = plugins.getPluginName(*plug_idx)
                except TypeError:
                    # Plugin not valid
                    plug_id = ""
                plug = common.ExtensionManager.plugins.get(
                    plug_id, self._device
                )
                if plug is not None:
                    with ProfilerContext(f"Tick {type(plug)}"):
                        plug.doTick(plug_idx)
                    with ProfilerContext(f"Apply {type(plug)}"):
                        plug.apply(thorough=changed)
            else:
                window = common.ExtensionManager.windows.get(
                    plug_idx, self._device
                )
                if window is not None:
                    with ProfilerContext(f"Tick {type(window)}"):
                        window.doTick(plug_idx)
                    with ProfilerContext(f"Apply {type(window)}"):
                        window.apply(thorough=changed)

        # Tick final special plugins
        for p in common.ExtensionManager.final.get(self._device):
            if p.shouldBeActive():
                with ProfilerContext(f"Tick {type(p)}"):
                    p.doTick(plug_idx)
                with ProfilerContext(f"Apply {type(p)}"):
                    p.apply(thorough=True)

        # Tick the device
        self._device.doTick()

    @profilerDecoration("main.processEvent")
    def processEvent(self, event: EventData) -> None:
        with ProfilerContext("Match event"):
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
            # raise ValueError(
            #     f"Couldn't identify event: "
            #     f"{eventToString(event)}"
            # )
            return

        else:
            log(
                "device.event.in",
                f"Recognised event: {mapping.getControl()}",
                verbosity.EVENT,
                detailed_msg=eventToString(event)
            )
        # Get active standard plugin
        plug_idx = common.getContext().active.getActive()
        if plug_idx is not None:
            if isinstance(plug_idx, tuple):
                try:
                    plug_id = plugins.getPluginName(*plug_idx)
                except TypeError:
                    # Plugin not valid
                    plug_id = ""
                plug = common.ExtensionManager.plugins.get(
                    plug_id, self._device
                )
                if plug is not None:
                    with ProfilerContext(f"Process {type(plug)}"):
                        if plug.processEvent(mapping, plug_idx):
                            event.handled = True
                            return
            else:
                window = common.ExtensionManager.windows.get(
                    plug_idx, self._device
                )
                if window is not None:
                    with ProfilerContext(f"Process {type(window)}"):
                        if window.processEvent(mapping, plug_idx):
                            event.handled = True
                            return

        # Get special plugins
        for p in (
            common.ExtensionManager.special.get(self._device)
            + common.ExtensionManager.final.get(self._device)
        ):
            if p.shouldBeActive():
                with ProfilerContext(f"Process {type(p)}"):
                    if p.processEvent(mapping, plug_idx):
                        event.handled = True
                        return
