
# Event Forwarding

For devices that use multiple ports, the Universal Controller Script uses a
many-to-one one-to-many model for processing events. The main script should be
assigned to the MIDI port for your controller, and the forwarder script should
be assigned to other ports such as the DAW port. All incoming events are then
forwarded to the main script such that it can determine what device sent each
event. Outgoing forwarded events are broadcast to all devices, where they will
be filtered and ignored unless they match the target device.

## Setting up Devices

In order for a device to accept input from multiple ports, it must implement the
following functionality:

* Must be able to recognize the device from every port (if it sends a different
  universal device enquiry on different ports, this must be noted).

* Must be able to determine the device number for each device. Device numbers
  are specified as follows:
    * `1` Main device (that is connected to the primary script).
    * `2+` Other devices (that are connected to the forwarder script). Note that
      these should match with the `MIDIIN` number used as the device name on
      Windows, for example a device named `MIDIIN2 (My Device)` would have
      device number `2`.

  In order to include this functionality, a number of strategies can be used:
    * Determined based on device name. Note that device names are different on
      Windows and MacOS/Linux - test on both platforms if possible. If you can't
      try your device on oth platforms, refer to your controller's documentation
      to find the name of the device's ports.
    * Determined based on another MIDI Sysex query. Currently, there isn't a
      context state for performing these queries before the device is loaded,
      but if there is demand, I will create one.
    * Determined based on the universal device enquiry response. The event data
      for this response will be given to your device object's `create()`
      classmethod, if the device was recognized through the universal device
      enquiry. Note that device recognition through a universal device enquiry
      may not be guaranteed.
    * If you find any other strategies, please contribute them to this
      documentation.

## Forwarding Events

The following functions in the `common.util.events` module are available when
working with forwarded events. Refer to their docstrings for full information.

* `isEventForwarded(event: FlMidiMsg) -> bool`
  * Returns whether an event has been forwarded
* `isEventForwardedHere(event: FlMidiMsg) -> bool`
  * Returns whether an event has been forwarded, and is targeting this device
    ID.
* `isEventForwardedHereFrom(event: FlMidiMsg, device_num: int = -1) -> bool`
  * Returns whether an event has been forwarded, is targeting this device ID,
    and was forwarded from a forwarder device with number `device_num`, or was
    forwarded from the primary device targeting the forwarder device with
    number `device_num`.
* `encodeForwardedEvent(event: FlMidiMsg, device_num: int = -1) -> bytes`
  * Encode an event for forwarding.
* `decodeForwardedEvent(event: FlMidiMsg, type_idx:int=-1) -> FlMidiMsg`
  * Decode a forwarded event.
* `forwardEvent(event: FlMidiMsg, device_num: int = -1)`
  * Forward an event.

## Forwarded Event Specification

The following structure is used for packaging forwarded events.

* `0xF0` Sysex start.

* `0x7D` Non-commercial system exclusive ID. This should prevent any clashing
  messages with other hardware, which will be using a registered system
  exclusive ID.

* `[device id]` An ASCII-encoded string containing the device identifier,
  returned by the `Device.getId()` method. This is used to filter events so
  that devices only receive events from their own device.

* `0x00` Null terminator, to determine the end point of the device ID.

* `[device number]` For incoming messages, the number of the device that
  received the event, as returned by the `Device.getDeviceNumber()` method. For
  outgoing messages, the number of the target device that should output the
  event.

* `[event category]` The type of the event that was forwarded:
    * `0` for standard events.
    * `1` for sysex events.

* `[event data]` The data from the event.
    * `data2`, `data1`, `status` for standard events, followed by the `0xF7`
      event terminator, which will terminate the forwarded event.
    * `[sysex data]` for sysex events, including the `0xF7` event terminator,
      which will terminate the forwarded event.

## Limitations of Current System

* The system currently breaks if multiple devices with the same ID are
  connected. Their events will be impossible to filter correctly.

If you can think of a way to remove any of the above limitations, please let me
know.
