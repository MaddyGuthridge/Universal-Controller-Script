
# Event Patterns

Import from `control_surfaces.event_patterns`

Event patterns are used to recognize events from their MIDI data. The most
common type is the `BasicPattern` which can be used to detect a variety of event
types.

## `IEventPattern`
The interface used to define an event pattern. If none of the following patterns
match your needs, you can make a custom pattern by implementing this.

### Methods to Implement
* `matchEvent(self, event: FlMidiMsg) -> bool`: Given a MIDI event, return
  whether that event matches with the pattern.

## `BasicPattern`
A basic event pattern that can recognize most events.

## `ForwardedPattern`
A pattern used to recognize events that were forwarded from other devices. Its
constructor should be given another event pattern to recognize from.

## `UnionPattern`
A pattern used to recognize events from the union of multiple patterns. Its
constructor should be given other event patterns to match from.

## `ForwardedUnionPattern`
Represents a union between an event pattern and the forwarded version of that
pattern. Equivalent to
`UnionPattern(SomePattern(), ForwardedPattern(SomePattern()))`.

## `NullPattern`
A pattern that won't match with anything. This can be used to instantiate
controls when they are being recognized through other code.
