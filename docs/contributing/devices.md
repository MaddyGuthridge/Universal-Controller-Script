
# Devices

Device definitions should be contained in the directory
`devices/[manufacturer]/[model]/[generation]`. For example, the definition for
the Novation Launchkey Mk2 series of devices is found in the
`devices/novation/launchkey/mk2` directory.

Generally, devices are created by defining [control surfaces](controlsurface.md)
that the device supports, then adding those controls to a
[control matcher](controlmatcher.md), before calling the parent device class to
initialise it with that control matcher.

## Defining a Control Surface

A control is defined by instantiating a type derived from the `ControlSurface`
class. Most of these types are quite self-explanatory, for example `StopButton`
represents a stop button.

When a control is instantiated, it is usually given an
[event pattern](eventpattern.md) used to recognise matching events, and a 
[value strategy](valuestrategy.md) used to extract a value from the event.

## Methods to Implement
* `@classmethod create(cls, event: Optional[eventData]) -> Device`: Create an 
  instance of this device.
* `@staticmethod getId() -> str`: Returns the ID of the device
  (`"Manufacturer.Model.Mark.Variant"`).
* `@staticmethod getUniversalEnquiryResponsePattern() -> Optional[IEventPattern]`:
  Returns an event pattern used to match the device's response to a universal
  device enquiry.
* `@staticmethod matchDeviceName(name: str) -> bool`: Given a device name,
  return whether it matches this device.
* `@staticmethod getDrumPadSize() -> int, int`: Return the size of the drum
  pad grid in terms of rows, cols.

# Methods to Implement if Required
* `initialise(self)`: Called when the device is initialised.
* `tick(self)`: Called when the script ticks.

## Example Device Definition

```py
class MyControl(Device):
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
        
        # Finally finish the initialisation
        super().__init__(matcher)
    
    @staticmethod
    def getDrumPadSize() -> tuple[int, int]:
        return 0, 0 # Our controller doesn't have drum pads
    
    @classmethod
    def create(cls, event: Optional[eventData]) -> Device:
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
        return name == "My Control"
```
