
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
to the `super` constructor. Callbacks can be decorated using
[event filters](eventfilter.md) to filter out unwanted events.

### Design Ideals for Plugin Interfaces

When designing a plugin interface, you should strive to make your interface
match the following criteria:
* Simple: although documentation should be available, the control mappings
  should be simple enough that users don't need to think about what controls
  control what.
* Static: where reasonable, controls should always map to the same places.
  Having things change around can be confusing for users, even if the users are
  the ones controlling it.
* Concise: you shouldn't try to create a mapping for every parameter that the
  plugin supports. Only add support for the ones that are most used for live
  performance, or for general control (eg macros).

## Methods to Implement

* `@classmethod create(cls, shadow: DeviceShadow) -> Plugin`: Create and return
  an instance of this plugin.
* `@staticmethod getPlugIds() -> tuple[str, ...]`: Returns a tuple of the
  plugin IDs to associate this plugin with. Only for plugins of type
  `StandardPlugin`.
* `@staticmethod getWindowId() -> int`: Returns the ID of the window to
  associate this plugin with. Only for plugins of type `WindowPlugin`
* `@staticmethod shouldBeActive() -> bool`: Returns whether this plugin should
  be active. Only for plugins of type `SpecialPlugin`.

## Example Plugin

```py
class MyPlugin(StandardPlugin):
    """
    Used to interact with my imaginary plugin
    """
    def __init__(self, shadow: DeviceShadow) -> None:
        # Bind faders to myCallback
        shadow.bindMatches(
            Fader, # Type to bind
            self.myCallback, # Function to bind to
            target_num=5, # Number of controls to bind
            allow_substitution=True, # Substitute faders for other types if needed
            raise_on_failure=False # Don't give an error if we can't bind the controls
        )
        # Call the super function
        super().__init__(shadow, [])

    @classmethod
    def create(cls, shadow: DeviceShadow) -> StandardPlugin:
        # Create an instance of the plugin
        return cls(shadow)

    @staticmethod
    def getPlugIds() -> tuple[str, ...]:
        # This plugin should map to plugins named MyPlugin
        return ("MyPlugin",)

    @filterToGeneratorIndex # Filter out plugins when the active plugin isn't a generator
    def myCallback(self, control: ControlShadowEvent, index: GeneratorIndex, *args: Any) -> bool:
        # Set the parameter
        plugins.setParamValue(control.value control.coordinate[1], *index)
        # Handle the event
        return True

# Register my plugin
ExtensionManager.registerPlugin(MyPlugin)
```
