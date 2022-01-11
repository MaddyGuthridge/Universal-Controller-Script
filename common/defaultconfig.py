"""
common > defaultconfig

Stores the default configuration for the script. The user configuration will
override any existing settings here.

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]
"""

from logger import verbosity

CONFIG = {
    # Logging settings
    "logger": {
        # Maximum verbosity for which all logged messages will be printed 
        "max_verbosity": verbosity.WARNING,
        # Categories to watch
        "watched_categories": [
            "general"
        ],
        # Maximum verbosity for which watched categories of logged messages
        # will be printed 
        "max_watched_verbosity": verbosity.INFO,
    },
    # Device settings
    "device": {
        # Associations between device name (as shown in FL Studio) and device id
        # to register (listed in class under id function)
        "name_associations": [
            # For example:
            # ("my device name", "Manufacturer.Model.Mark.Variant")
        ]
    }
}
