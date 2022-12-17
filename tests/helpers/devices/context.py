"""
tests > helpers > devices > context

Helper code for entering and exiting the context of using a device.

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""
from common.context_manager import getContext, unsafeResetContext
from .basic import DummyDeviceBasic, DummyDeviceAbstract

__all__ = [
    'DummyDeviceContext',
]


class DummyDeviceContext:
    """A context manager for working with dummy devices"""

    def __init__(
        self,
        num: int = 1,
        dev: type[DummyDeviceAbstract] = DummyDeviceBasic
    ) -> None:
        """
        Create a DummyDeviceContext

        ### Args:
        * `num` (`int`, optional): device number (for testing forwarded
          events). Defaults to `1`.

        * `dev` (`type[DummyDevice]`, optional): device type to use. Defaults
          to `DummyDevice`.
        """
        self._dev = dev
        self._num = num

    def __enter__(self):
        getContext().registerDevice(self._dev(self._num))  # type: ignore

    def __exit__(self, exc_type, exc_value, exc_traceback):
        unsafeResetContext()
