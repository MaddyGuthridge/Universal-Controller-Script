
# Devices

Device definitions should be contained in the directory
`devices/[manufacturer]/[model]/[generation]`. For example, the definition for
the Novation Launchkey Mk2 series of devices is found in the
`devices/novation/launchkey/mk2` directory.

Generally, devices are created by defining
[control surfaces](control_surface.md) that the device supports, then adding
those controls to a [control matcher](control_matcher.md), before calling the
parent device class to initialize it with that control matcher.

## Defining a Control Surface

A control is defined by instantiating a type derived from the `ControlSurface`
class. Most of these types are quite self-explanatory, for example `StopButton`
represents a stop button.

When a control is instantiated, it is usually given an
[event pattern](event_pattern.md) used to recognize matching events, and a
[value strategy](value_strategy.md) used to extract a value from the event.

For some devices, more fine-grained control may be necessary to take full
advantage of the device's capabilities. In cases like this, you can create a
subclass that inherits from a control surface within the package where you
are creating your device, then instantiate that instead. Refer to
[the documentation](control_surface.md#extending-existing-control-surfaces).

### Control Generators

Some control surfaces, such as notes, need to be generated in bulk for most
controllers. For cases like these, control generators are available to simplify
the creation process. They can be found under `devices.control_generators`.
These are all types of control matcher and can be added to a standard control
matcher using `matcher.addSubMatcher()`.

* `NoteMatcher`: sub matcher for note events
* `NoteAfterTouchMatcher`: sub matcher for per-note after-touch
* `PedalMatcher`: sub matcher for pedals

## Control Surfaces to Implement

In order for users of your device to have the optimal experience, you should
consider implementing as many of the following control surfaces as possible.

* `ControlSwitchButton` to switch between modes in a plugin (eg step sequencer
  to omni preview in the channel rack).

* `PauseActiveButton` to pause updating the active plugin.

* `SwitchActiveButton` if your device uses a split control system (where
  windows are controlled separately to plugins).

* Basic transport buttons (play, stop, etc).

* At least one way to interact with plugins (faders, knobs or encoders).

Obviously if your controller doesn't have these features as hardware, you can
still use the script as a simple way to get compatibility with basic transport
controls, but if your device does have complex hardware, you should let the
script take advantage of that fact.

## Methods to Implement
* `@classmethod create(cls, event: FlMidiMsg = None, id: str = None) -> Device`:
  Create an instance of this device. The event or ID should be used to ensure
  that the device is created with the correct ID.

* `getId(self) -> str`: Returns the ID of the detected device
  (`"Manufacturer.Model.Revision.Variant"`). This is used to encode
  [forwarded events](event_forward.md), as well as to assist with bug reporting.

* `@classmethod getSupportedIds(cls) -> tuple[str, ...]`: Return all the device
  IDs that are supported by this device definition.

## Methods to Implement if Required

* `@classmethod getUniversalEnquiryResponsePattern(cls) -> Optional[IEventPattern]`:
  Returns an event pattern used to match the device's response to a universal
  device enquiry. Refer to the manual page on
  [device detection](detection.md#2-universal-device-enquiry).

* `@classmethod matchDeviceName(cls, name: str) -> bool`: Given a device name,
  return whether it matches this device. Refer to the manual page on
  [device detection](detection.md#3-name-matching).

* `@classmethod getDrumPadSize(cls) -> int, int`: Return the size of the drum
  pad grid in terms of rows, cols. Devices without drum pads should return
  `(0, 0)`.

* `initialize(self)`: Called when the device is initialized.

* `deinitialize(self)`: Called when the device is deinitialized.

* `tick(self)`: Called when the script ticks.

## Example Device Definition

```py
class MyController(Device):
    """
    An example controller for the documentation
    """

    def __init__(self, matcher: BasicControlMatcher) -> None:

        # Notes
        matcher.addControls(getNotesAllChannels())

        # Create knob controls, using a loop
        for i in range(8):
            matcher.addControl( # Register the control
                Knob(
                    BasicPattern(0xB0, i, ...), # Pattern for event
                    Data2Strategy(), # Get the value from data 2
                    (0, i) # Coordinate should be the index in the loop
                )
            )

        # Add a stop button
        matcher.addControl(StopButton(
            BasicPattern(0xB0, 0x72, ...),
            ButtonData2Strategy()
        ))
        # Add a standard pitch wheel
        matcher.addControl(StandardPitchWheel())

        # Finally finish the initialization
        super().__init__(matcher)

    @staticmethod
    def getDrumPadSize() -> tuple[int, int]:
        return 0, 0 # Our controller doesn't have drum pads

    @classmethod
    def create(cls, event: Optional[FlMidiMsg]) -> Device:
        return cls() # Our constructor doesn't take any arguments

    @staticmethod
    def getId() -> str:
        return f"Demo.MyControl.Mk1" # The ID of our controller

    @staticmethod
    def getUniversalEnquiryResponsePattern():
        return BasicPattern(
            [
                0xF0, # Sysex start
                0x7E, # Device response
                ..., # OS Device ID
                0x06, # Separator
                0x02, # Separator
                0x00, # Manufacturer
                0x77, # Manufacturer
                0x77, # Manufacturer
                0x01, # Family code
                0x4D, # Family code
                # Add any other required details
            ]
        )

    @staticmethod
    def matchDeviceName(name: str) -> bool:
        # Since we're providing a universal enquiry response pattern, we don't
        # need to bother implementing this as all devices should be matched
        # correctly from the pattern.
        # In non-standard devices, this function can be used as a backup
        # system, by using an expression such as the following:
        return name == "My Controller"

ExtensionManager.devices.register(MyController)
```
