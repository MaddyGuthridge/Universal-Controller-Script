"""
common > logger > hierarchy

Contains a formal definition of the logging hierarchy, used to verify
logging into particular categories

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""

HIERARCHY = {
    "bootstrap": {
        "initialize": {},
        "context": {
            "reset": {},
            "create": {}
        },
        "device": {
            "type_detect": {},
            "initialize": {},
        }
    },
    "device": {
        "event": {
            "in": {},
            "out": {},
        },
        "idle": {},
        "forward": {
            "bootstrap": {},
            "in": {},
            "out": {}
        }
    },
    "extensions": {
        "manager": {},
        "plugins": {
            "special": {},
            "window": {},
            "standard": {}
        },
    },
    "state": {
        "active": {}
    },
    "general": {}
}
