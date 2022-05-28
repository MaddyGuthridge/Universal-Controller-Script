
# Plugins

Plugins are extensions that define how the program should handle events and
interact with FL Studio Windows, as well as generator and effect plugins.

## Types of Plugins

* `StandardPlugin`: Standard plugins interact with generators and effects
* `WindowPlugin`: Window plugins interact with FL Studio windows
* `SpecialPlugin`: Plugins that can be active at any time

## Creating a Plugin

When a plugin is created, it should bind callback functions to a
[`DeviceShadow`](device_shadow.md) object, that represents the plugin's own
private copy of the device that is being mapped to. This can either be done
manually, or with [mapping strategies](mapping_strategy.md), given as arguments
to the `super` constructor. Callbacks can be decorated using
[event filters](event_filter.md) to filter out unwanted events.

### Design Ideals for Plugin Interfaces

When designing a plugin interface, you should strive to make your interface
match the following criteria:
* Simple: although documentation should be available, the control mappings
  should be simple enough that users don't need to think about what controls
  control what.

* Static: where reasonable, controls should always map to the same places.
  Having things change around can be confusing for users, even if the users are
  the ones controlling it. If you need to move between multiple pages of
  elements, the `Pager` plugin extension allows for interfaces to be built in
  a consistent way.

* Concise: you shouldn't try to create a mapping for every parameter that the
  plugin supports. Only add support for the ones that are most used for live
  performance, or for general control (eg macros).

## Methods to Implement

* `@classmethod create(cls, shadow: DeviceShadow) -> Plugin`: Create and return
  an instance of this plugin.

### Standard Plugins

* `@classmethod getPlugIds(cls) -> tuple[str, ...]`: Returns a tuple of the
  plugin IDs to associate this plugin with. Only for plugins of type
  `StandardPlugin`.

### Window Plugins

* `@classmethod getWindowId(cls) -> int`: Returns the ID of the window to
  associate this plugin with. Only for plugins of type `WindowPlugin`

### Special Plugins

* `@classmethod shouldBeActive(cls) -> bool`: Returns whether this plugin should
  be active. Only for plugins of type `SpecialPlugin`.

### Optional Methods

The following methods only need to be implemented if necessary.

* `tick(self, index: UnsafeIndex) -> None`: Perform any actions required to
  update the plugin.

## Control Binding

Control surfaces should be bound to callback functions during the constructor
method of the plugin. The bindings are made using the `DeviceShadow` that
should be provided to the constructor.

Usually, a plugin will bind a control by specifying the type of control to
bind, as well as a callback function that is called whenever an event for that
control is received. The plugin can also optionally provide a callback function
that is called whenever the plugin ticks, which allows the plugin to update
aspects of the control surface dynamically.

This binding is usually made using the `bindMatch` method of the provided
`DeviceShadow` object. This method returns a `ControlShadow` representing the
control that was bound to the given callbacks. If multiple bindings are needed,
`bindMatches` can be used. It returns a list of `ControlShadow` objects.

```py
# Bind a play button to the plugin's `play` method
play = shadow.bindMatch(PlayButton, self.play)

# Bind all available faders to the plugin's `fader` method, with a tick being
# bound to the plugin's `tickFader` method
faders  = shadow.bindMatches(Fader, self.fader, self.tickFader)
```

If only static properties are needed, the device can assign these directly to
the returned `ControlShadow` object. Although usually changes to these controls
should be made by using the `color`, `annotation`, and `value` properties, in
this state, quick changes to the color and annotation can be made using the
`colorize` and `annotate` methods of the `ControlShadow` object. These return
a reference to the same control so that they can be used in a pipeline pattern.

```py
# Bind a play button, set its color to black, then annotate it as "My control"
shadow.bindMatch(PlayButton, ...).colorize(Color()).annotate("My control")


```

If binding multiple controls, the same functions can be used to apply
properties to each control.

```py
# Bind 4 faders
shadow.bindMatches(Fader, self.faders, target_num=4) \
    # Set each color to gray
    .colorize(Color.fromInteger(0x222222)) \
    # Set the annotations to Macros 1 through 4
    .annotate([f"Macro {i+1}" for i in range(4)])
```

If no matches are found for the requested control type, a dummy control is
returned by default. This means that plugins can safely assign the properties
of bound controls without raising an exception. To check if the returned
object represents a successfully bound control, the `isBound()` method can be
called.

```py
c = shadow.bindMatch(PlayButton, ...)
if c.isBound():
    print("We got a match")
else:
    print("There wasn't a play button available")
```

Control bindings can be made in more advanced ways too. Refer to the manual
page on [device shadows](device_shadow.md).

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
            self.eventCallback, # Function to bind to for MIDI events
            self.tickCallback, # Function to bind to for ticks
            target_num=5, # Number of controls to bind
        )
        # Call the super function, and use the pedal strategy to handle pedal
        # events
        super().__init__(shadow, [PedalStrategy()])

    @classmethod
    def create(cls, shadow: DeviceShadow) -> StandardPlugin:
        # Create an instance of the plugin
        return cls(shadow)

    @classmethod
    def getPlugIds(cls) -> tuple[str, ...]:
        # This plugin should map to plugins named MyPlugin
        return ("MyPlugin",)

    @filterToGeneratorIndex # Filter out plugins when the active plugin isn't a generator
    def eventCallback(self, control: ControlShadowEvent, index: GeneratorIndex, *args: Any) -> bool:
        # Set the parameter
        plugins.setParamValue(control.value control.coordinate[1], *index)
        # Handle the event
        return True

    # TODO: Make sure that this filter works correctly
    @filterToGeneratorIndex # Filter out plugins when the active plugin isn't a generator
    def tickCallback(self, control: ControlShadow, index: GeneratorIndex, *args: Any) -> None:
        # Set the color of the control randomly
        control.color = Color.fromInteger(random.random() & 0xFFFFFF)

# Register my plugin
ExtensionManager.plugins.register(MyPlugin)
```
