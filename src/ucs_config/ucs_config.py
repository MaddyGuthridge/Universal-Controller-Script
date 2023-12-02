"""
config.py

Stores any user-modified parts of the configuration for the script, allowing
for customization of the script's behavior. After setting up the settings
directory, any settings found here will override those found in the default
configuration, which can be found in common/default_config.py.

### Setup

1. This file is found within a `ucs_config` folder. Copy that folder to outside
   the script folder, so that updating the script won't replace your settings
2. Restart FL Studio and the configuration will be automatically loaded.

Authors:
* You

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""
# flake8: noqa
# pragma: no cover

__all__ = [
    'CONFIG',
]

from typing import Any
from common.logger import verbosity

CONFIG: dict[str, Any] = {
    # TODO: Add your configuration here
}
