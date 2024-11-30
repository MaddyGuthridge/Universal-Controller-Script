"""
common > config > loader

Code for loading the user configuration.
"""
import sys
from .types import Config
from .default_config import DEFAULT_CONFIG
from common.util import dict_tools


# Add the custom configuration directory to the path so we can load from it
scripts_dir = \
    '/'.join(__file__.replace('\\', '/').split('/')[:-4]) + '/ucs_config'
sys.path.insert(0, scripts_dir)


def load_configuration() -> Config:
    """
    Load the script configuration
    """
    try:
        from ucs_config import CONFIG as user_settings
    except ImportError as e:
        # The file doesn't exist
        # FIXME: Log the error properly
        print(f"User configuration not found {e}")
        return DEFAULT_CONFIG
    except SyntaxError as e:
        # FIXME: Log the error properly
        print(e)
        return DEFAULT_CONFIG
    except Exception as e:
        # FIXME: Log the error properly
        print(e)
        return DEFAULT_CONFIG

    # Now merge the user settings with the defaults
    merged_settings = dict_tools.recursive_merge_dictionaries(
        DEFAULT_CONFIG,
        user_settings,
    )

    return merged_settings
