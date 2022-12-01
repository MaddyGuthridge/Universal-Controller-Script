"""
common > consts

Constants used within the script

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""

# Version info
VERSION = (1, 1, 2)

# Sub versions
VERSION_MAJOR = VERSION[0]
VERSION_MINOR = VERSION[1]
VERSION_REVISION = VERSION[2]
VERSION_SUFFIX = ""

# Minimum API version required to run script
MIN_API_VERSION = 19


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

ASCII_HEADER_ART = r"""
                                .
                             ,;;'
                            ;;'
             .,;/F\/;,    ,L,
           ,\FFFLFLFFLF; ;L'
          ;FLFLFLFFLFFFFLF/L;;,,     ,,;;;;;/;;,
         'FLL\LFFFFFLFLFLFFFLFFFFLL;;,.'`    ',&
            ':/L;/FFFFLFFLFFFFFLFFF\           &;
                 \;FFFFFLFFFFLFFFFLF;        .&/
                 ,;LFFFLFLFLLFFLFLFFL      ,;&/
              .;;:.'/LFLFL\F;,;LL\FL/    ./&'
           .;;,'      '.'      'FL/'   ;&/"
         ,;,'                       ,\\;'
      .;;.                    ,,';\\;'
    .;;'                    ,;L\/'`
   ;;'                  .,/\L;'
  ;/               .,;/\/,'..
  \;,        .,;/&/;;.    ,'
   ":;;;;;//;;&/''       ;
      ``'''``          .'
                     .;
            ',    ,:'
              ';''
"""

# Device enquiry message
UNIVERSAL_DEVICE_ENQUIRY = bytes([0xF0, 0x7E, 0x7F, 0x06, 0x01, 0xF7])

# Device type constants
DEVICE_TYPE_CONTROLLER = 1
DEVICE_TYPE_FORWARDER = 2

# The starting point for control change parameters in plugins
PARAM_CC_START = 4096
