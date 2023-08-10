"""
common > consts

Constants used within the script

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""
import ui

# Name to present for the script

# Version info
VERSION = (2, 0, 0)

# Sub versions
VERSION_MAJOR = VERSION[0]
VERSION_MINOR = VERSION[1]
VERSION_RELEASE = VERSION[2]
VERSION_SUFFIX = "beta-3"

# Minimum API version required to run script
MIN_FL_VERSION = (21, 0, 3)


def formatVersion(version: tuple[int, int, int], suffix: str = '') -> str:
    """
    Format the given version string
    """
    suffix = f"-{suffix}" if suffix else ""
    return ".".join(map(str, version)) + suffix


def getVersionString() -> str:
    """
    Returns the version string of the script

    Eg: `"1.2.3-beta"`
    """
    return formatVersion(VERSION, VERSION_SUFFIX)


def getFlVersion() -> tuple[int, int, int]:
    fl_major = ui.getVersion(0)
    assert isinstance(fl_major, int)
    fl_minor = ui.getVersion(1)
    assert isinstance(fl_minor, int)
    fl_release = ui.getVersion(2)
    assert isinstance(fl_release, int)

    return fl_major, fl_minor, fl_release


def checkFlVersion() -> bool:
    """
    Checks if the script is running in a compatible version of FL Studio
    """
    fl_major, fl_minor, fl_release = getFlVersion()

    req_major, req_minor, req_release = MIN_FL_VERSION

    if fl_major < req_major:
        return False
    if fl_major > req_major:
        return True

    if fl_minor < req_minor:
        return False
    if fl_minor > req_minor:
        return True

    if fl_release < req_release:
        return False

    return True


# Website
WEBSITE = "https://github.com/MiguelGuthridge/Universal-Controller-Script"
ISSUES_PAGE = f"{WEBSITE}/issues"
DOCUMENTATION = f"{WEBSITE}/tree/main/docs"
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

HEADER_TEMPLATE = r"""
                                .
                             ,;;'
                            ;;'
             .,;UCS/;,    ,/,
           ,\FL;FL;FL\;  /'
          /UCS;UCS;UCS;UCS;UCS\,     ,,;;&&;/;;,
         'FL;FL;FL;FL;FL;FL;FL;FL;\/;&|'`   `',\
            ':/UCS;UCS;UCS;UCS;UCS;\           ;;
                 \FL;FL;FL;FL;FL;FL;\        .;/
                 ,;UCS;UCS;UCS;UCS;/;      ,;&/
              .;;:.'/FL;;FL;FLFL;FL;/    ./&'
           .;&,'      '.'      ':;/'   ;&/"
         ,/,'                       ,\\;'
      .;;.                    ,,';\\;'
    .;&'                    ,;/:/'`
   ;;'                  .,/&|;'
  //               .,;/\/,'..
  \;         .,;&\|;;'    ,'      {title}
   ":;&&;;|/;&|/''       ;        Version {version}
      ``'''``          .'         FL Studio {fl_version}
                     .;
            ',    ,:'             Made with <3 by Miguel Guthridge
              ':''
"""


def getHeaderArt(title_string: str):
    return HEADER_TEMPLATE\
        .replace("{title}", title_string)\
        .replace("{version}", getVersionString())\
        .replace("{fl_version}", str(ui.getVersion()))


# Device enquiry message
UNIVERSAL_DEVICE_ENQUIRY = bytes([0xF0, 0x7E, 0x7F, 0x06, 0x01, 0xF7])

# Device type constants
DEVICE_TYPE_CONTROLLER = 1
DEVICE_TYPE_FORWARDER = 2

# The starting point for control change parameters in plugins
PARAM_CC_START = 4096

WINDOW_NAMES = ['Mixer', 'Channel Rack', 'Playlist', 'Piano Roll', 'Browser']
