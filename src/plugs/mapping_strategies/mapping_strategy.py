"""
plugins > mapping_strategies > mapping_strategy

Definition for a mapping strategy, which can be used to map a controls
with little effort on the part of the plugin developer

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""

from common.util.abstract_method_error import AbstractMethodError
from devices import DeviceShadow
from abc import abstractmethod


class IMappingStrategy:
    """
    Creates a quick and simple way to map controls to plugin parameters used by
    many plugins, for example pedal events
    """

    @abstractmethod
    def apply(self, shadow: DeviceShadow) -> None:
        """
        Apply the strategy to a control shadow.

        ### Args:
        * `shadow` (`DeviceShadow`): device shadow to apply mappings to
        """
        raise AbstractMethodError(self)
