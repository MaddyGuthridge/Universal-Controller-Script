
# Mapping Strategies

Mapping strategies are used to quickly map controls to pre-built functionality.

## Provided strategies
Some strategies are provided within the script. Refer to each one's provided
documentation.

## `DirectionStrategy`
Maps direction buttons to control FL Studio.

## `JogStrategy`
Maps jog wheel to control FL Studio.

## `ModXYStrategy`
Maps a mod-X/Y controller to mod-x/y parameters in a plugin.

## `MuteSoloStrategy`
Creates a mapping for mute and solo buttons.

## `NoteStrategy`
Maps notes to note events on the channel rack.

## `PedalStrategy`
Maps pedals to required CC parameters.

## `SimpleFaders`
Maps fader controls to a given list of parameters.

## `WheelStrategy`
Maps pitch and mod wheels to required parameters.

## `IMappingStrategy`

The interface used by mapping strategies. This should be implemented by all
mapping strategies.

### Methods to Implement
* `apply(shadow: DeviceShadow)`: Apply the mapping to a device shadow.
