"""
common > param

Code for interacting with plugin parameters.

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""
import plugins

from common.plug_indexes import PluginIndex
from abc import abstractmethod


class PluginParameter:
    """
    This is an abstract class used to provide type safety when modifying plugin
    parameters.
    """

    @abstractmethod
    def __init__(self, index: PluginIndex) -> None:
        """
        Associate the parameter with a plugin instance. This allows the
        parameter properties to be modified.
        """
        ...

    @property
    @abstractmethod
    def value(self) -> float:
        """
        The value of the parameter (read/write)
        """
        ...

    @value.setter
    @abstractmethod
    def value(self, newValue: float):
        ...

    @property
    @abstractmethod
    def name(self) -> str:
        """
        The name of the parameter
        """
        ...


def Param(paramIndex: int) -> type[PluginParameter]:
    """
    A `Param` represents a parameter for a plugin. This function generates a
    `PluginParameter` class that can be used to access the parameter given a
    plugin instance.

    ```py
    # Create a parameter definition
    SustainParam = Param(5)

    # ...

    def eFader1(control: ControlShadowEvent, plugin: GeneratorIndex):
        # Associate the parameter with the given plugin, then set its value
        SustainParam(plugin).value = control.value
    ```
    """
    class IndexedPluginParameter(PluginParameter):
        def __init__(self, index: PluginIndex) -> None:
            self.__plug = index

        @property
        def value(self) -> float:
            return plugins.getParamValue(
                paramIndex,
                self.__plug.index,
                self.__plug.slotIndex,
                True,
            )

        @value.setter
        def value(self, newValue: float):
            plugins.setParamValue(
                newValue,
                paramIndex,
                self.__plug.index,
                self.__plug.slotIndex,
                2,
                True,
            )

        @property
        def name(self) -> str:
            return plugins.getParamName(
                paramIndex,
                self.__plug.index,
                self.__plug.slotIndex,
                True
            )

    return IndexedPluginParameter
