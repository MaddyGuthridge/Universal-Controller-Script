
# Control Events and Mappings

`ControlEvent`, `ShadowControlEvent` and `ControlMapping` all serve as a way to
map to controls, but are used in different scenarios.

* `ControlEvent` types represent a MIDI event after it has been recognized.
  They contain info on the value of the event (as a float between 0 and 1) and
  on the channel of the event (-1 if no channel otherwise 0-15)
* `ControlShadowEvent` types are similar to a `ControlEvent` but are used within
  the context of plugins so that plugins have access to both the event info
  and the [control shadow](control_shadow.md) associated with the event.
* `ControlMapping` types serve as a way to map to a control surface outside the
  context of events, and as such don't have value or channel parameters.
