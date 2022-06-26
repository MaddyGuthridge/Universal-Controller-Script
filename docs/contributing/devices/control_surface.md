
# Control Surfaces

Control surfaces represent a control on a device. The are instantiated during
the construction of `Device` objects, and are indirectly mapped to by plugins,
via the [`ControlShadow`](../plugins/control_shadow.md) type.

## List of Control Surfaces

This is all the control surfaces defined in the `control_surfaces` module.
Classes labelled with `*` have a `Master` variant, which represents that
control surface, but specifically for the master channel.

* `Note`: Represents a note event
* `ModWheel`: Represents a modulation wheel
    * `StandardModWheel`: a mod wheel that behaves in the standard way
* `PitchWheel`: Represents a pitch bend wheel
    * `StandardPitchWheel`: a pitch wheel that behaves in the standard way
    * `Data2PitchWheel`: a pitch wheel that only sends pitch data in the
      `data2` byte of the event.
* `AfterTouch`: Represents after-touch events
    * `ChannelAfterTouch`
    * `NoteAfterTouch`
* `Pedal`: Represents a foot pedal
    * `SustainPedal`
    * `SostenutoPedal`
    * `SoftPedal`
* `Button`: Represents a button (used by many transport controls)
* `ControlSwitchButton`: Used as a command for plugins to switch modes, for
  example switching from omni mode to sequencer mode in the channel rack.
* `JogWheel`: Represents an encoder used for transport and navigation.
    * `StandardJogWheel`: Scrolling and changing selection
    * `ShiftedJogWheel`: Scrolling and changing selection, but along the opposite
      axis
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
* `FaderButton` * : Represents a button commonly found near a fader.
    * `GenericFaderButton` * : A button that can act as a mute or solo control
    * `MuteButton` * : A mute track button
    * `SoloButton` * : A solo track button
    * `ArmButton` * : An arm track button
    * `SelectButton` * : A select track button
* `Fader` * : Represents a fader (linear slider).
* `Knob` * : Represents a knob (rotating dial).
* `ModXY`: 2D modulation surface
    * `ModX`: 2D modulation surface (X component)
    * `ModY`: 2D modulation surface (Y component)
* `Encoder`: Represents an encoder (endlessly rotating dial)
* `DrumPad`: Represents a drum pad
* `MacroButton`: Represents a button used to perform some action in FL Studio
    * `SaveButton`: Save
    * `UndoRedoButton`: Redo if possible, otherwise undo
    * `UndoButton`: Undo
    * `RedoButton`: Redo
    * `QuantizeButton`: Quantize
    * `CaptureMidiButton`: Dump score log to selected pattern
* `ActivityButton`:
    * `SwitchActiveButton`: Button that switches between plugins and windows
      for controllers designed with a split activity scheme
        * `SwitchActivePluginButton`: Switch activity to the active plugin
        * `SwitchActiveWindowButton`: Switch activity to the active window
        * `SwitchActiveToggleButton`: Toggle activity between plugins and
          windows
    * `PauseActiveButton`: Pause updating of the active plugin and window.
* `HintMsg`: A control that shouldn't map to any events, but which should use
  an [`AnnotationManager`](property_managers.md#annotation-manager) to display
  the contents of FL Studio's hint panel.
* `NotifMsg`: A control that shouldn't map to any events, but which should use
  an [`AnnotationManager`](property_managers.md#annotation-manager) to display
  notification messages.
* `NullEvent`: Used to handle events that the script should ignore

## Instantiating Control Surfaces
Control surfaces can be instantiated by providing any of the following
arguments:

* `event_pattern`: an [event pattern](event_pattern.md) that can be used to
  recognize the event. If not provided, the control can never be matched.

* `value_strategy`: a [value strategy](value_strategy.md) that can be used to
  determine a value from events. If not provided, the control won't get values.

* `coordinate`: the coordinate of the control. Defaults to `(0, 0)`.

* `annotation_manager`: an
  [`AnnotationManager`](property_managers.md#annotation-manager).

* `color_manager`: a [`ColorManager`](property_managers.md#color-manager)

* `value_manager`: a [`ValueManager`](property_managers.md#value-manager)

As well as this, some control surfaces provide class methods to create
instances without specifying all the properties.

## Defining New Control Surfaces

As a general rule of thumb, new control surfaces types shouldn't be created
except for those that don't match any existing types. This should be discussed
in the Discord server before creating one. This is because having more control
surface types will make it harder to assign controls easily within plugins.

## Extending Existing Control Surfaces

By default, the provided control surfaces don't provide any advanced
functionality such as color or annotation support. If a control on your device
supports this, or requires logic that doesn't work well with the parent class
(such as the M-Audio Hammer 88 Pro's pitch wheel), it should implement it in a
child class to the control surface it most accurately represents, and then
implement any required functions.

### Methods to Implement if Required
* `tick(self)`: Called when a tick happens. This should be used to send any
  events required to keep the control functioning. For example, if your
  controller is prone to losing LED colors randomly (like the Novation
  Launchkey Mk2 Series), it can send out a color update every few ticks. Note
  that these events should be limited to reduce slowness.

* `@staticmethod isPress(value: float) -> bool`: Should return whether a
  particular value is equivalent to a button press (as opposed to a lift), used
  to detect double presses. By default this is implemented for most control
  surfaces, but can be overridden if needed.
