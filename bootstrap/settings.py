
import sys
from typing import Any

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
        sys.modules.pop(c.__file__)
        sys.modules.pop(d.__file__)
        del c
        del d
    
    @staticmethod
    def _recursiveGet(keys: list[str], settings: dict):
        if len(keys) == 1:
            return settings[keys[0]]
        else:
            return Settings._recursiveGet(keys[1:], settings[keys[0]])

    def get(self, key: str) -> Any:
        """
        Get an entry from 

        [extended_summary]

        ### Args:
        * `key` (`str`): [description]

        ### Raises:
        * `KeyError`: [description]
        * `KeyError`: [description]

        ### Returns:
        * `Any`: [description]
        """
        try:
            return Settings._recursiveGet(key.split('.'), self._settings_dict)
        except KeyError as e:
            raise KeyError(f"Unable to find setting at '{key}'. Failed for key {e}") from None
        except IndexError:
            raise KeyError(f"Unable to find setting at '{key}'") from None
