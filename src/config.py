"""
config.py

Stores any user-modified parts of the configuration for the script, allowing
for customization of the script's behavior. Any settings found here will
override those found in the default configuration.

Authors:
* Miguel Guthridge [hdsq@outlook.com.au]
* You
"""

__all__ = [
    'verbosity',
    'CONFIG',
]

from typing import Any
from common.logger import verbosity

CONFIG: dict[str, Any] = {
    "logger.watched_categories": [
        "general",
    ],
}
