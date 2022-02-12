
# Plugins

Plugins are extensions that define how the program should handle events and
interact with FL Studio Windows, as well as generator and effect plugins.

## Types of Plugins

* `StandardPlugin`: Standard plugins interact with generators and effects
* `WindowPlugin`: Window plugins interact with FL Studio windows
* `SpecialPlugin`: Plugins that can be active at any time

## Creating a Plugin

When a plugin is created, it should bind callback functions to a
[`DeviceShadow`](deviceshadow.md) object, that represents the plugin's own
private copy of the device that is being mapped to. This can either be done 
manually, or with [mapping strategies](mappingstrategy.md), given as arguments
to the `super` constructor.
