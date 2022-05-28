
# Device Shadows

A device shadow is an object representing a plugin's own private copy of a
device's state. It allows the plugin to manipulate the device without impacting
the state of other plugins.

See also:
* [Control shadow](control_shadow.md)

## Methods

Refer to inline documentation for full descriptions. Note that only methods
relevant to plugin manipulation are listed here.

* `getControlMatches(control: type[ControlSurface], ...) -> list[ControlShadow]`:
  Get a list of controls matching the criteria.

* `getNumControlMatches(control: type[ControlSurface], ...) -> int`: Get the
  number of controls matching the criteria.

* `bindControl(control: ControlShadow, bind_to: EventCallback, ...)`: Bind a
  callback function to a control.

* `bindControls(controls: list[ControlShadow], bind_to: EventCallback, ...)`:
  Bind a callback function to all elements of a list of controls.

* `bindMatch(control: type[ControlSurface], bind_to: EventCallback, ...) -> `
  `bool`: Bind the first matching control to the given callback. Essentially a
  shorthand way to get a matching control and bind it.

* `bindMatches(control: type[ControlSurface], bind_to: EventCallback, ...) -> `
  `bool`: Bind the all matching controls to the given callback. Essentially a
  shorthand way to get matching controls and bind them.
