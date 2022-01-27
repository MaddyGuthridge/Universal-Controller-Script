"""
plugins > plugin

Contains the definition of the Plugin base class
"""

from devices import DeviceShadow

class Plugin:
    
    def __init__(self, shadow: DeviceShadow, mapping_strategies) -> None:
        """
        Create a plugin object which interacts with a device shadow

        ### Args:
        * `shadow` (`DeviceShadow`): device shadow to interact with
        """
        
