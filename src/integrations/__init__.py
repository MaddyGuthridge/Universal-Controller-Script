"""
integrations

Contains definitions for script integrations, allowing the Universal Controller
Script to interface with FL Studio
"""

__all__ = [
    'IMappingStrategy',
    'NoteStrategy',
    'PedalStrategy',
    'WheelStrategy',
    'Integration',
    'CoreIntegration',
    'PluginIntegration',
    'WindowIntegration',
    'IntegrationPager',
]

from .mapping_strategies import (
    NoteStrategy,
    PedalStrategy,
    WheelStrategy,
)

from .integration import (
    Integration,
    CoreIntegration,
    PluginIntegration,
    WindowIntegration,
)
from .pager import IntegrationPager

# Register all integrations
from . import (
    core,
    window,
    plugin,
)
del (
    core,
    window,
    plugin,
)
