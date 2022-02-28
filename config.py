"""
config.py

Stores any user-modified parts of the configuration for the script, allowing for
customisation of the script's behaviour. Any settings found here will override
those found in the default configuration.

Authors:
* Miguel Guthridge [hdsq@outlook.com.au]
* You
"""

from typing import Any
from common.logger import verbosity

CONFIG: dict[str, Any] = {
    "logger.watched_categories": [
        "general",
        # "device.event.in"
    ],
    # "logger.max_watched_verbosity": verbosity.NOTE,
    "debug.profiling": True
}
