"""
control_surfaces > managers

Contains interfaces for managing the properties of control surfaces, so that
these properties can be reflected on the physical hardware.

Authors:
* Maddy Guthridge [hello@maddyguthridge.com, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""
__all__ = [
    'IAnnotationManager',
    'IColorManager',
    'IValueManager',
    'DummyAnnotationManager',
    'DummyColorManager',
    'DummyValueManager',
]

from .annotation_manager import IAnnotationManager, DummyAnnotationManager
from .color_manager import IColorManager, DummyColorManager
from .value_manager import IValueManager, DummyValueManager
