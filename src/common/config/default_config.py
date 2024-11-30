"""
common > default_config

Stores the default configuration for the script. The user configuration will
override any existing settings here.

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""
from .types import Config

DEFAULT_CONFIG: Config = {
    "controls": {
        "double_press_time": 0.3,
        "long_press_time": 0.5,
        "short_press_time": 0.1,
        "navigation_speed": 5,
        "use_snap": True,
        "use_undo_toggle": True,
        "score_log_dump_length": 120
    },
    "integrations": {
        "mixer": {
            "allow_extended_volume": False
        },
    },
    "advanced": {
        "debug": {
            "profiling_enabled": False,
            "exec_tracing_enabled": False
        },
        "drop_tick_time": 100,
        "slow_tick_time": 50,
        "activity_history_length": 25,
    },
}
