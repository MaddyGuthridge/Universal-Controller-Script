
# Control Shadows

`ControlShadow` objects are used to represent a plugin's private copy of a
[control surface](../devices/control_surface.md). This allows them to modify the state of
the control without fear of breaking the state of another plugin.

After event handling or ticking of a plugin, the state of the control shadow
will be applied to the associated `ControlSurface` object.

See also:
* [Device shadow](device_shadow.md)
