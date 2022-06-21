"""
common > settings

Contains a wrapper class for the settings, allowing for an effective way to
check the configuration of the script.

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""

__all__ = [
    'Settings'
]

import sys
from typing import Any
from .util import dict_tools
from . import default_config as d
from .exceptions import InvalidConfigError

# Load the main config
scripts_dir = \
    '/'.join(__file__.replace('\\', '/').split('/')[:-3]) + '/ucs_config'
sys.path.append(scripts_dir)

had_errors = False
config_errors = ''
try:
    from config import CONFIG  # type: ignore
except ImportError:
    # Failed to import - assume they don't have custom settings
    CONFIG = {}
except SyntaxError as e:
    CONFIG = {}
    had_errors = True
    config_errors = f'Syntax error: {e}'
except Exception as e:
    CONFIG = {}
    had_errors = True
    config_errors = f'Unknown error: {e}'


class Settings:
    """
    A container for the configuration of the script

    Used to avoid having to deal with the awfulness of pulling things out of
    dictionaries. Also manages the differences between the default config and
    any user modifications.
    """

    def __init__(self) -> None:
        """
        Initialize and load the script's settings
        """
        self.__valid = True
        self.__error_msg = ''
        if had_errors:
            self.__valid = False
            self.__error_msg = config_errors
            self._settings_dict = d.CONFIG
            return
        try:
            config = dict_tools.expandDictShorthand(CONFIG)
            self._settings_dict = dict_tools.recursiveMergeDictionaries(
                d.CONFIG, config)
        except (KeyError, TypeError) as e:
            self.__valid = False
            self.__error_msg = str(e)
            self._settings_dict = d.CONFIG

    def assert_loaded(self) -> None:
        """
        Raise an exception if settings didn't load correctly

        ### Raises:
        * `InvalidConfigError`: invalid config
        """
        if not self.__valid:
            raise InvalidConfigError(self.__error_msg)

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

    @staticmethod
    def _recursiveSet(keys: list[str], settings: dict, value: Any) -> None:
        """
        Recursive function for setting settings value

        ### Args:
        * `keys` (`list[str]`): list of keys
        * `settings` (`dict`): settings dictionary to search
        * `value` (`Any`): value to set
        """
        if len(keys) == 1:
            if keys[0] not in settings:
                raise KeyError(keys[0])
            settings[keys[0]] = value
        else:
            Settings._recursiveSet(keys[1:], settings[keys[0]], value)

    def get(self, key: str) -> Any:
        """
        Get an entry in the settings

        ### Args:
        * `key` (`str`): key to access settings from

        ### Raises:
        * `KeyError`: Unable to find settings

        ### Returns:
        * `Any`: Value
        """
        try:
            return Settings._recursiveGet(key.split('.'), self._settings_dict)
        except KeyError as e:
            raise KeyError(
                f"Unable to find setting at '{key}'. Failed for key {e}"
            ) from None
        except IndexError:
            raise KeyError(f"Unable to find setting at '{key}'") from None

    def set(self, key: str, value: Any) -> None:
        """
        Set an entry in the settings

        ### Args:
        * `key` (`str`): key to access settings from
        * `value` (`Any`): value to set

        ### Raises:
        * `KeyError`: Unable to find settings
        """
        try:
            return Settings._recursiveSet(
                key.split('.'),
                self._settings_dict,
                value
            )
        except KeyError as e:
            raise KeyError(
                f"Unable to find setting at '{key}'. Failed for key {e}"
            ) from None
        except IndexError:
            raise KeyError(f"Unable to find setting at '{key}'") from None
