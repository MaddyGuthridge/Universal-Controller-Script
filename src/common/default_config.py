"""
common > default_config

Stores the default configuration for the script. The user configuration will
override any existing settings here.

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""

from .logger import verbosity

CONFIG = {
    # Settings to configure for controllers
    "controls": {
        # The time in seconds for which a double press is valid
        "double_press_time": 0.3,
        # The time in seconds required to register a long press
        "long_press_time": 0.5,
        # The maximum time in seconds required to register a short press
        "short_press_time": 0.1,
        # How fast to navigate when long pressing a button, lower is faster
        "navigation_speed": 3,
        # Whether an undo/redo button should always undo, rather than acting as
        # an undo/redo toggle
        "disable_undo_toggle": False,
    },
    # Settings to configure plugins
    "plugins": {
        # General configuration
        "general": {
            # Whether values that have a centred default should snap close
            # values to the default
            "do_snap": True,
            # The length of time to dump to a pattern from the score log when a
            # capture MIDI button is pressed, in seconds.
            "score_log_dump_length": 120
        },
        # FL Studio mixer
        "mixer": {
            # Whether volumes over 100% should be allowed
            # * True: faders will map from 0-125%
            # * False: faders will map from 0-100%
            "allow_extended_volume": False
        },
    },
    # Settings used during script initialization
    "bootstrap": {
        # Whether to skip sending sysex messages when attempting to recognize
        # devices... will improve startup time for devices that don't support
        # universal device enquiries, but will result in other devices
        # breaking. Enabling this is not recommended.
        "skip_enquiry": False,
        # Whether sending the device enquiry message should be delayed
        # until after initialization (workaround for a bug in FL 20.9.1)
        "delay_enquiry": True,
        # How long to wait after sending a universal device enquiry until the
        # fallback device recognition method is used, in seconds.
        "detection_timeout": 3.0,
        # Associations between device name (as shown in FL Studio) and device
        # id to register (listed in class under getId() function)
        # This can be used to skip using universal device enquiry messages, if
        # necessary
        "name_associations": [
            # For example:
            # ("my device name", "Manufacturer.Model.Mark.Variant")
        ],
    },
    # Settings used for debugging
    "debug": {
        # Whether performance profiling should be enabled
        "profiling": False,
        # Whether profiling should print the tracing of profiler contexts
        # within the script. Useful for troubleshooting crashes in FL Studio's
        # MIDI API. Requires profiling to be enabled.
        "exec_tracing": False
    },
    # Logging settings
    "logger": {
        # Verbosity for which full details will be printed to the console when
        # it is logged.
        "critical_verbosity": verbosity.ERROR,
        # Maximum verbosity for which all logged messages will be printed
        "max_verbosity": verbosity.WARNING,
        # Categories to watch, meaning they will be printed, even if a lower
        # verbosity is used. For details on available categories, refer to
        # common/logger/log_hierarchy.py.
        "watched_categories": [
            "general"
        ],
        # Maximum verbosity for which watched categories of logged messages
        # will be printed
        "max_watched_verbosity": verbosity.INFO,
        # Verbosity levels at or above this will be discarded entirely be the
        # logger to improve performance
        "discard_verbosity": verbosity.NOTE,
    },
    # Advanced settings for the script. Don't edit these unless you know what
    # you're doing, as they could cause the script to break, or behave badly.
    "advanced": {
        # Time in ms during which we expect the script to be ticked. If the
        # script doesn't tick during this time, then the script will consider
        # itself to be constrained by performance, and will drop the next tick
        # to prevent lag in FL Studio.
        "drop_tick_time": 100,
        # Time in ms for which a tick should be expected to complete. If
        # ticking FL Studio takes longer than this, it will be recorded,
        # regardless of whether profiling is enabled.
        "slow_tick_time": 50,
        # The maximum length of the plugin/window tracking history
        "activity_history_length": 25,
    },
}
