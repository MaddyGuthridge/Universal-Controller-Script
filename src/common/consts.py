"""
common > consts

Constants used within the script

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""
import ui

# Version info
VERSION = (2, 0, 0)

# Sub versions
VERSION_MAJOR = VERSION[0]
VERSION_MINOR = VERSION[1]
VERSION_REVISION = VERSION[2]
VERSION_SUFFIX = "beta-3"

# Minimum API version required to run script
MIN_FL_VERSION = (21, 0, 3)


def getVersionString() -> str:
    """
    Returns the version string of the script

    Eg: `"1.2.3-beta"`
    """
    suffix = f"-{VERSION_SUFFIX}" if VERSION_SUFFIX else ""
    return ".".join(map(str, VERSION)) + suffix


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
             .,;/FL/;,    ,/,
           ,\UCS;FL;UCS; ;/'
          ;FL;UCS;FL;UCS;FL\;;,,     ,,;;;;;/;;,
         'UCS;FL;UCS;FL;UCS;FL;UCS;;;,.'`    ',&
            ':/UCS;FL;UCS;FL;UCS;FL\           &;
                 \UCS;FL;UCS;FL;UCS;\        .&/
                 ,;FL;UCS;FL;UCS;FL;;      ,;&/
              .;;:.'/FL;UCS/;,UCS;FL/    ./&'
           .;;,'      '.'      'FL/'   ;&/"
         ,;,'                       ,\\;'
      .;;.                    ,,';\\;'
    .;;'                    ,;L\/'`
   ;;'                  .,/\L;'
  ;/               .,;/\/,'..
  \;,        .,;/&/;;.    ,'      Universal Controller Script
   ":;;;;;//;;&/''       ;        Version {version}
      ``'''``          .'         FL Studio {fl_version}
                     .;
            ',    ,:'             Made with <3 by Miguel Guthridge
              ';''
"""


def getHeaderArt():
    return HEADER_TEMPLATE\
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
