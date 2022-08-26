
# Mapping Strategies

Mapping strategies are used to quickly map controls to pre-built functionality.

## Provided strategies
Some strategies are provided within the script, and can be used to simplify the
creation of advanced plugins that work well for all devices. Refer to each
one's provided documentation within the source code.

### `DirectionStrategy`
Maps direction buttons to control FL Studio.

### `DrumPadStrategy`
Maps drum pads into indexes, so that interfaces using drum pads can be designed
adaptively.

### `JogStrategy`
Maps jog wheel to control FL Studio.

### `ModXYStrategy`
Maps a mod-X/Y controller to mod-x/y parameters in a plugin.

### `MuteSoloStrategy`
Creates a mapping for mute and solo buttons.

### `NoteStrategy`
Maps notes to note events on the channel rack.

### `PedalStrategy`
Maps pedals to required CC parameters.

### `SimpleFaders`
Maps fader controls to the given plugin parameters. This can be used to quickly
link up faders for automation.

### `WheelStrategy`
Maps pitch and mod wheels to required parameters.

## Custom strategies

You can implement your own mapping strategy by extending the `IMappingStrategy`
class, which provides the interface used by all mapping strategies. You should
implement the following methods:

* `apply(shadow: DeviceShadow)`: Apply the mapping to a device shadow.
