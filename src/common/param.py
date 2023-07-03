import plugins

from common.plug_indexes import PluginIndex


def Param(paramIndex: int):
    class PluginParameter:
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
                True
            )

        @property
        def name(self) -> str:
            return plugins.getParamName(
                paramIndex,
                self.__plug.index,
                self.__plug.slotIndex,
                True
            )

    return PluginParameter
