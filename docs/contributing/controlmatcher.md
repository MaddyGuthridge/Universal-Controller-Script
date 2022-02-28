
# Control Matchers

Control matchers are used to maintain a set of control surfaces, which can
be matched with incoming events.

## `IControlMatcher`

The interface used by control matchers. If the `BasicControlMatcher` doesn't
suit your needs, you can implement this interface to create your own control
matcher.

### Methods to Implement
* `matchEvent(self, event: eventData) -> Optional[ControlEvent]`: Given an
  event, return a [`ControlEvent`](controlevent.md) mapped to the matched
  control, or `None` if there were no matches.
* `getGroups(self) -> set[str]`: Return the set of control groups this control
  matcher uses.
* `getControls(self, group:str=None) -> list[ControlSurface]`: Return a list of
  the controls managed by this control matcher.

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
