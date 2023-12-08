"""
common > ucs_context

Defines the overall context for the script, representing almost all of the
script's state.

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""
from fl_classes import FlMidiMsg
from time import time_ns
from typing import TYPE_CHECKING

from .extensions.integrations import (
    get_core_preprocess_integrations,
    get_core_postprocess_integrations,
    get_integration_for_plugin,
    get_integration_for_window,
)
from .config import load_configuration
from .activity_state import ActivityState
from .plug_indexes import WindowIndex
from .util.api_fixes import catchUnsafeOperation
from .util.misc import NoneNoPrintout
from .util.forwarded_events import handle_event_on_external

if TYPE_CHECKING:
    from devices import Device
    from integrations import Integration


class UcsContext:
    """
    The overall context for the script, representing most of its state.
    """

    def __init__(self, device: 'Device') -> None:
        """
        Initialise the script's context
        """
        self.initialized = False
        """Whether the script is currently initialized and running"""
        self.device = device
        """The object representing the overall device"""
        self.device_num = device.get_device_number()
        """The device number, used to forward events"""
        self.settings = load_configuration()
        """The configuration of the script"""
        self.activity = ActivityState()
        """Maintains the currently selected plugin or window"""

        # FIXME: Make profiler detached from the context

        # Storing instances of all the integrations

        self.__plugin_integrations: dict[str, 'Integration'] = {}
        """
        Mapping of plugin names to instances of the corresponding integration
        objects
        """

        self.__window_integrations: dict[WindowIndex, 'Integration'] = {}
        """
        Mapping of window indexes to instances of the corresponding integration
        objects
        """

        self.__core_integrations: list['Integration'] = []
        """
        List of instances of the core script integrations
        """

        # Performance measuring

        self.__last_tick_time = time_ns()
        """The last time that the script ticked"""
        self.__tick_count = 0
        """The number of times the script has ticked since it was loaded"""
        self.__dropped_ticks = 0
        """
        The number of times a tick was skipped due to the previous tick being
        too slow.
        """
        self.__slow_ticks = 0
        """
        The number of times a tick event has been processed slowly, used for
        finding performance issues
        """
        self.__slow_integrations: dict[str, int] = {}
        """
        A mapping of slow integrations to the number of times they've caused
        a slow tick
        """

    def initialize(self) -> None:
        """
        Initialize the device
        """
        # No need to do anything unless this is the main script
        if self.device_num != 0:
            return
        self.device.initialize()
        self.initialized = True

    def deinitialize(self) -> None:
        """
        Deinitialize the device
        """
        # No need to do anything unless this is the main script
        if self.device_num != 0:
            return
        self.device.deinitialize()
        self.initialized = False

    def process_event(self, event: FlMidiMsg) -> None:
        """
        Process a MIDI event

        This handles the event by forwarding it to the active integrations

        ### Args
        * `event` (`FlMidiMsg`): event to process
        """
        if not self.initialized:
            return

        if self.device_num != 0:
            return handle_event_on_external(self.device_num, event)

        # TODO: write this

    @catchUnsafeOperation
    def tick(self) -> None:
        """
        Called frequently to let devices and integrations update.
        """
        # No need to do anything unless this is the main script
        if self.device_num != 0:
            return

        # If the script isn't initialized, performing a tick could be dangerous
        # and get it into an invalid state
        if not self.initialized:
            return

        self.__tick_count += 1

        # If the last tick was too long ago, then our script is getting laggy
        # Skip this tick to compensate
        last_tick = self.__last_tick_time
        self.__last_tick_time = time_ns()
        drop_tick_time = self.settings['advanced']['drop_tick_time']
        if (self.__last_tick_time - last_tick) / 1_000_000 > drop_tick_time:
            self.__dropped_ticks += 1
            return

        tick_start_time = time_ns()

        self.activity.tick()

        # TODO: Tick the state

        tick_end_time = time_ns()
        slow_tick_time = self.settings['advanced']['slow_tick_time']
        if (tick_end_time - tick_start_time) / 1_000_000 > slow_tick_time:
            self.__slow_ticks += 1
            integration_name = self.activity.getActive().getName()
            self.__slow_integrations[integration_name] = \
                self.__slow_integrations.get(integration_name, 0) + 1

    def performance_info(self) -> NoneNoPrintout:
        """
        Display information about the performance of the script.
        """
        dropped_percent = int(self.__dropped_ticks / self.__tick_count * 100)
        slow_percent = int(self.__slow_ticks / self.__tick_count * 100)

        print("=======================")
        print("PERFORMANCE INFORMATION")
        print(f"Tick count: {self.__tick_count}")
        print(f"Dropped ticks: {self.__dropped_ticks} ({dropped_percent}%)")
        print(f"Slow ticks: {self.__slow_ticks} ({slow_percent}%)")
        print("Slow integrations:")
        for integration, count in sorted(
            self.__slow_integrations.items(),
            key=lambda x: x[1],
        ):
            print(f" * {integration} ({count})")
        print()
        print("For more performance metrics, consider enabling the profiler")
        return NoneNoPrintout
