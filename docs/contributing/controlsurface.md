
# Control Surfaces

Control surfaces represent a control on a device. The are instantiated during
the construction of `Device` objects, and are indirectly mapped to by plugins,
via the [`ControlShadow`](controlshadow.md) type.

## List of Control Surfaces

* `Note`: Represents a note event
* `ModWheel`: Represents a modulation wheel
* `PitchWheel`: Represents a pitch bend wheel
* `AfterTouch`: Represents aftertouch events
    * `ChannelAfterTouch`
    * `NoteAfterTouch`
* `Pedal`: Represents a foot pedal
    * `SustainPedal`
    * `SostenutoPedal`
    * `SoftPedal`
* `Button`: Represents a button (used by many transport controls)
* `JogWheel`: Represents an encoder used for transport and navigation
    * `StandardJogWheel`: Scrolling and changing selection
    * `MoveJogWheel`: Moving selection
* `TransportButton`: Buttons used for transport
    * `PlayButton`
    * `StopButton`
    * `LoopButton`: Toggle FL Studio's loop mode
    * `RecordButton`
    * `FastForwardButton`
    * `RewindButton`
    * `MetronomeButton`
* `NavigationButton`: Buttons used for navigating FL Studio
    * `DpadButtons`: Buttons used for directions
        * `DirectionUp`
        * `DirectionDown`
        * `DirectionLeft`
        * `DirectionRight`
        * `DirectionSelect`
    * `NextPrevButton`: Next and previous buttons
        * `DirectionNext`
        * `DirectionPrevious`
* `Fader`: Represents a fader (linear slider)
* `Knob`: Represents a knob (rotating dial)
* `Encoder`: Represents an encoder (endlessly rotating dial)
* `DrumPad`: Represents a drum pad

## Creating New Control Surfaces

As a general rule of thumb, new control surfaces types shouldn't be created
except for those that don't match any existing types. This should be discussed
in the Discord server before creating one. This is because having more control
surface types will make it harder to assign controls easily within plugins.

## Extending Existing Control Surfaces

By default, the provided control surfaces don't provide any advanced
functionality such as colour or annotation support. If a control on your device
supports this, or requires logic that doesn't work well with the parent class
(such as the M-Audio Hammer 88 Pro's pitch wheel), it should implement it in a
child class to the control surface it most accurately represents, and then
implement any required functions.

### Methods to Implement if Required
* `onColorChange(self)`: Called when the color of the control has changed
* `onAnnotationChange(self)`: Called when the annotation of the control has
  changed.
* `onValueChange(self)`: Called when the value of the control has changed.
* `tick(self)`: Called when a tick happens.
