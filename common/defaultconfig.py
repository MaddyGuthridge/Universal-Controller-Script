"""
common > defaultconfig

Stores the default configuration for the script. The user configuration will
override any existing settings here.
"""

from logger import verbosity

CONFIG = {
    # Logging settings
    "logger": {
        # Maximum verbosity for which all logged messages will be printed 
        "max_verbosity": verbosity.WARNING,
        # Categories to watch
        "watched_categories": [],
        # Maximum verbosity for which watched categories of logged messages
        # will be printed 
        "max_watched_verbosity": verbosity.INFO,
    }
}
