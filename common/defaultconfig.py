"""
common > defaultconfig

Stores the default configuration for the script. The user configuration will
override any existing settings here.

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]
"""

from .logger import verbosity

CONFIG = {
    # Logging settings
    "logger": {
        # Verbosity for which full details will be printed to the console when
        # it is logged.
        "critical_verbosity": verbosity.ERROR,
        # Maximum verbosity for which all logged messages will be printed 
        "max_verbosity": verbosity.WARNING,
        # Categories to watch
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
    # Settings used for debugging
    "debug": {
        # Whether performance profiling should be enabled
        "profiling": False
    },
    # Settings used during script initialisation
    "bootstrap": {
        # Whether to skip sending sysex messages when attempting to recognise
        # devices... may improve startup time for some devices
        "skip_enquiry": False,
        # Whether sending the device enquiry message should be delayed
        # until after initialisation (workaround for a bug in FL 20.9.1)
        "delay_enquiry": True,
        # How long to wait until the fallback device recognition method is used.
        "detection_timeout": 3.0,
        # Associations between device name (as shown in FL Studio) and device id
        # to register (listed in class under getId() function)
        # This can be used to skip using universal device enquiry messages, if
        # necessary
        "name_associations": [
            # For example:
            # ("my device name", "Manufacturer.Model.Mark.Variant")
        ]
    }
}
