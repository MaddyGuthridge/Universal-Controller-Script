"""
plugins

Contains definitions for plugins, allowing the script to interface with them
"""

from .mappingstrategies import *

from .plugin import Plugin, SpecialPlugin, StandardPlugin, WindowPlugin

# Filters
from . import eventfilters
from . import tickfilters

# Register plugins
from . import special
from . import windows
from . import standard
