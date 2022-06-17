
# Control Shadows

`ControlShadow` objects are used to represent a plugin's private copy of a
[control surface](../devices/control_surface.md). This allows them to modify
the state of the control without breaking the state of another plugin.

After event handling or ticking of a plugin, the state of the control shadow
will be applied to the associated `ControlSurface` object.

## Applying Properties

The properties of control shadows can be managed in multiple ways.

### Value Assignment

The following properties are available to assign to:

* `color`: the color that should be displayed on the control

* `annotation`: a short string stating the control's mapping

* `value`: the value of the control between 0 and 1

### Pipeline Assignment

These values can be assigned using methods which return a reference to the
same control surface, which can allow for properties to be quickly assigned to
a control shadow.

* `colorize`

* `annotate`

Note that values cannot be set, as they should be updated in real-time, rather
than setting once.

See also:
* [Device shadow](device_shadow.md)
