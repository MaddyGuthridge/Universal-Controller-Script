"""
common > settings

Contains a wrapper class for the settings, allowing for an effective way to
check the configuration of the script.

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]
"""

__all__ = [
    'Settings'
]

from typing import Any

from .util import dicttools, hotreload

from . import defaultconfig as d

class Settings:
    """
    A container for the configuration of the script

    Used to avoid having to deal with the awfulness of pulling things out of
    dictionaries. Also manages the differences between the default config and
    any user modifications.
    """
    
    def __init__(self) -> None:
        """
        Initialise and load the script's settings
        """
        
        c = hotreload.getTemporaryModule('config')
        config = dicttools.expandDictShorthand(c.CONFIG)
        self._settings_dict = dicttools.recursiveMergeDictionaries(d.CONFIG, config)
    
    @staticmethod
    def _recursiveGet(keys: list[str], settings: dict) -> Any:
        """
        Recursive function for getting settings value

        ### Args:
        * `keys` (`list[str]`): list of keys
        * `settings` (`dict`): settings dictionary to search

        ### Returns:
        * any: value
        """
        if len(keys) == 1:
            return settings[keys[0]]
        else:
            return Settings._recursiveGet(keys[1:], settings[keys[0]])

    def get(self, key: str) -> Any:
        """
        Get an entry in the settings

        ### Args:
        * `key` (`str`): key to access settings from

        ### Raises:
        * `KeyError`: Unable to find settings

        ### Returns:
        * any: Value
        """
        try:
            return Settings._recursiveGet(key.split('.'), self._settings_dict)
        except KeyError as e:
            raise KeyError(f"Unable to find setting at '{key}'. Failed for key {e}") from None
        except IndexError:
            raise KeyError(f"Unable to find setting at '{key}'") from None
