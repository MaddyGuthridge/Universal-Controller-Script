
# Mapping Strategies

Mapping strategies are used to quickly map controls to pre-built functionality.

## `IMappingStrategy`

The interface used by mapping strategies. This should be implemented by any
mapping strategies.

### Methods to Implement
* `apply(shadow: DeviceShadow)`: Apply the mapping to a device shadow.

## `NoteStrategy`
Maps notes to note events on the channel rack.

## `PedalStrategy`
Maps pedals to required CC parameters.

## `WheelStrategy`
Maps pitch and mod wheels to required parameters.
