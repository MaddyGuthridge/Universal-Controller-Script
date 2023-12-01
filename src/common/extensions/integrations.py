"""
common > extensions > integrations

Code responsible for registering and managing integrations

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""
from ctypes import Union
from typing import TYPE_CHECKING, Optional
from common.types.decorator import Decorator
from common.plug_indexes import WindowIndex

if TYPE_CHECKING:
    from integrations import Integration


_plugin_integrations: dict[str, 'Integration'] = {}
"""Integrations with plugins"""

_window_integrations: dict[WindowIndex, 'Integration'] = {}
"""Integrations with FL Studio windows"""

_core_pre_integrations: list['Integration'] = []
"""Core integrations (preprocessed)"""

_core_post_integrations: list['Integration'] = []
"""Core integrations (postprocessed)"""


def register_plugin(
    plugin_name: str,
) -> Decorator[type['Integration'], type['Integration']]:
    """
    Register an integration with a plugin (FL or VST), given the plugin name.

    ### Usage

    ```py
    @integrations.register_plugin("Flex")
    class MyIntegration(Integration):
        ...
    ```

    ### Args
    * `plugin_name` (`str`): name of the plugin for which this integration
      should be used

    ### Returns
    * `Decorator[type[Integration]]`: a decorator function that registers the
      integration definition
    """
    def inner(integration: type['Integration']) -> type['Integration']:
        if (found_int := _plugin_integrations.get(plugin_name)) is not None:
            raise ValueError(
                f"An integration matching plugin name {plugin_name} has "
                f"already been registered.\n\n"
                f"Attempted to register: {integration}\n"
                f"Previously registered integration: {found_int}"
            )
        _plugin_integrations[plugin_name] = integration
        return integration

    return inner


def register_window(
    idx: WindowIndex,
) -> Decorator[type['Integration'], type['Integration']]:
    """
    Register an integration with an FL Studio window, given its window index.

    ### Usage

    ```py
    @integrations.register_window(WindowIndex.CHANNEL_RACK)
    class MyIntegration(Integration):
        ...
    ```

    ### Args
    * `idx` (`WindowIndex`): index of the window for which this integration
      should be used

    ### Returns
    * `Decorator[type[Integration]]`: a decorator function that registers the
      integration definition
    """
    def inner(integration: type['Integration']) -> type['Integration']:
        if (found_int := _window_integrations.get(idx)) is not None:
            raise ValueError(
                f"An integration matching window index {idx} has "
                f"already been registered.\n\n"
                f"Attempted to register: {integration}\n"
                f"Previously registered integration: {found_int}"
            )
        _window_integrations[idx] = integration
        return integration

    return inner


def register_core(*, preprocess: bool) -> Union[
    type['Integration'],
    Decorator[type['Integration'], type['Integration']]
]:
    """
    Register a core integration with the script. Core integrations are always
    active, and can be used to make a feature set be always in use.

    ### Usage

    ```py
    @integrations.register_core(preprocess=True)
    class MyIntegration(Integration):
        ...
    ```

    ### Args
    * `preprocess`(`bool`): whether the integration should process events
      before other integrations (`True`) or after other integrations (`False`)

    ### Returns
    * `Decorator[type[Integration]]`: a decorator function that registers the
      integration definition
    """
    if preprocess:
        integration_list = _core_pre_integrations
    else:
        integration_list = _core_post_integrations

    def inner(integration: type['Integration']) -> type['Integration']:
        integration_list.append(integration)
        return integration

    return inner


def get_integration_for_plugin(
    plugin_name: str,
) -> Optional[type['Integration']]:
    """
    Returns an integration definition that matches the given plugin name, if
    such an integration is registered.

    ### Args
    * `plugin_name` (`str`): name of plugin to find an integration for

    ### Returns
    * `type[Integration]`: integration definition, if found
    * `None`: if no matches
    """
    return _plugin_integrations.get(plugin_name)


def get_integration_for_window(
    window_index: WindowIndex,
) -> Optional[type['Integration']]:
    """
    Returns an integration definition that matches the given FL Studio window
    index, if such an integration is registered.

    ### Args
    * `window_index` (`WindowIndex`): FL Studio window index

    ### Returns
    * `type[Integration]`: integration definition, if found
    * `None`: if no matches
    """


def get_core_preprocess_integrations() -> list[type['Integration']]:
    """
    Returns a list of all registered preprocessing core integrations.

    ### Returns
    * `list[type[Integration]]`: list of core integration definitions
    """
    return _core_pre_integrations


def get_core_postprocess_integrations() -> list[type['Integration']]:
    """
    Returns a list of all registered postprocessing core integrations.

    ### Returns
    * `list[type[Integration]]`: list of core integration definitions
    """
    return _core_post_integrations
