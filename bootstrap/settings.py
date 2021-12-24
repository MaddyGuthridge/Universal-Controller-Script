
import sys

from . import util

class Settings:
    """
    A container for the configuration of the script

    Used to avoid having to deal with the awfulness of pulling things out of
    dictionaries. Also manages the differences between the default config and
    any user modifications.
    """
    
    def __init__(self) -> None:
        """
        Initialise and load the settings
        """
        from . import defaultconfig as d
        import config as c
        config = util.expandDictShorthand(c.CONFIG)
        self._settings_dict = util.recursiveMergeDictionaries(d.CONFIG, config)
        
