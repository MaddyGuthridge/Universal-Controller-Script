
# Devices

Device definitions should be contained in the directory
`devices/[manufacturer]/[model]/[generation]`. For example, the definition for
the Novation Launchkey Mk2 series of devices is found in the
`devices/novation/launchkey/mk2` directory.

Generally, devices are created by defining control surfaces that the device
supports, then adding those controls to a control matcher, before calling the
parent device class to initialise it with that control matcher.

## Defining a Control Surface

A control is defined by instantiating a type derived from the ControlSurface
class. Most of these types are quite self-explanatory, for example `StopButton`
represents a stop button.

When a control is instantiated, it is usually given an
[event pattern](eventpattern.md) used to recognise matching events, and a 
[value strategy](valuestrategy.md) used to extract a value from the event.

## Registering a Control

A control can be registered by 
