from typing import TypedDict

from .advanced import AdvancedConfig
from .controls import ControlSurfaceConfig
from .integrations import IntegrationConfig


class Config(TypedDict):
    """
    Represents the configuration of the script
    """

    controls: ControlSurfaceConfig
    """
    Options for control surfaces, applied to all devices
    """

    integrations: IntegrationConfig
    """
    Options for integrations
    """

    advanced: AdvancedConfig
    """
    Advanced configuration options, including debug options
    """
