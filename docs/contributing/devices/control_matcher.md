
# Control Matchers

Import from `control_surfaces.matchers`

Control matchers are used to maintain a set of control surfaces, which can
be matched with incoming events.

## `BasicControlMatcher`

A basic control matcher that can be used for most devices. It provides various
other methods for managing controls

* `addControl(self, control: ControlSurface)`: Registers a control surface to
  the matcher.
* `addControls(self, controls: list[ControlSurface])`: Registers a list of
  control surfaces to the matcher.
* `addSubMatcher(self, matcher: IControlMatcher)`: If a small amount of
  complexity is required with control matching, the basic matcher may not be
  sufficiently powerful. This function can be used to add another
  IControlMatcher to act as a component of this matcher. An example of this can
  be seen in the implementation of the jog wheel on the M-Audio Hammer 88 Pro,
  where the sub-matcher is used to make events map to a different type of jog
  wheel depending on whether the encoder is pressed down or not.

## `IndexedMatcher`

A control matcher that can be used to match controls that use sequential CC
control numbers. This matcher performs significantly better than a basic
matcher, and can be used in many scenarios given a clear controller definition.

## `ShiftMatcher`

A control matcher that matches different controls based on whether a shift
button is pressed. This can be used alongside more advanced control matchers in
order to build advanced control matching systems.

## `NoteMatcher`

A control matcher that matches all 128 notes. By default, it will match all
channels, but a ByteMatch object can be used to customize this.

## `PedalMatcher`

A control matcher that matches pedal events, including the sustain pedal,
sostenuto pedal, and soft pedal.

## `IControlMatcher`

The interface used by control matchers. If the matchers documented above don't
suit your needs, you can implement this interface to create your own control
matcher.

### Methods to Implement
* `matchEvent(self, event: FlMidiMsg) -> Optional[ControlEvent]`: Given an
  event, return a [`ControlEvent`](../plugins/control_event.md) mapped to the
  matched control, or `None` if there were no matches.

* `getControls(self) -> list[ControlSurface]`: Return a list of
  the controls managed by this control matcher.

* `tick(self)`: Tick the control matcher.
