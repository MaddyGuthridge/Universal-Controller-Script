"""
common > consts

Constants used within the script

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]
"""

# Version info
VERSION = (0, 0, 1)

VERSION_MAJOR = VERSION[0]
VERSION_MINOR = VERSION[1]
VERSION_REVISION = VERSION[2]

def getVersionString() -> str:
    """
    Returns the version string of the script
    """
    return ".".join(map(str, VERSION))

# Website
WEBSITE = "https://github.com/MiguelGuthridge/Universal-Controller-Script"
DISCORD = "https://discord.gg/6vpfJUF"

# Contributor information
AUTHORS: dict[str, list[str]] = {
    "Designers": [
        "Miguel Guthridge"
    ],
    "Primary Developers": [
        "Miguel Guthridge"
    ],
    "Minor Contributors": [
    ],
    "Plugin Contributors": [
    ],
    "Device Contributors": [
    ]
}
