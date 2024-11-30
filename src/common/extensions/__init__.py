"""
common > extensions

Code responsible for managing script integrations and device definitions.

* Allows for devices and integrations to be registered alongside their criteria
  for usage.
* Allows for the script core to access these integrations in order to integrate
  the script with devices and FL Studio

Authors:
* Miguel Guthridge [hdsq@outlook.com.au, HDSQ#2154]

This code is licensed under the GPL v3 license. Refer to the LICENSE file for
more details.
"""
from . import devices, integrations


__all__ = ['devices', 'integrations']
