"""
plugins

Contains definitions for plugins, allowing the script to interface with them
"""

from .mappingstrategies import *

from .plugin import Plugin, SpecialPlugin, StandardPlugin

# Register plugins
from . import special
