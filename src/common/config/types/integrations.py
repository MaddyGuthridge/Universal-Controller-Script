from typing import TypedDict


class MixerConfig(TypedDict):
    """
    Configuration for FL Studio mixer
    """

    allow_extended_volume: bool
    """
    Whether volumes over 100% should be allowed
    * `True`: faders will map from 0-125%
    * `False`: faders will map from 0-100%
    """


class IntegrationConfig(TypedDict):
    """
    Configuration of script integrations - any integrations that provide
    settings are listed as members of this.
    """

    mixer: MixerConfig
    """
    FL Studio mixer window
    """
