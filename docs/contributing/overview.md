
# Design Overview

This script is quite an advanced piece of software, with over 18000 lines of
Python code. As such, getting a solid grasp of the way it functions can be
challenging. This document aims to describe how the script works in a simple
manner so that you can navigate its code efficiently.

## Main Structure

The script is comprised of a small number of main components.

* Device definitions, which are responsible for describing how the script
  interacts with devices.

* Plugin definitions, which are responsible for describing how the script
  interacts with plugins and FL Studio Windows.

* The common module, which serves as an interface between devices and plugins.

## Initialization

The script's behavior is controlled by using a state machine, which is managed
by the script context manager (which can be accessed by calling
`common.getContext()` from anywhere in the script). The transitions between
these states allow the script to initialize itself.

Initially, the script starts in the "waiting for device" state. In this state,
it uses various methods to attempt to identify the device. For more
information, refer to [this page](devices/detection.md). If no device is
matched, the script will enter an error state.

Otherwise, the script enters the main state.

## Main State

In this state, plugins are allowed to interface with the device.

### Event Processing

Upon receiving any MIDI event, the device is used to recognize the event and
return its mapping as a `ControlEvent`, which contains a reference to the
control surface that was matched, as well as the value and the channel of the
event.

The script then sends the event to any active plugins, so that they can process
it. If a plugin has bound that control surface, then the associated callback
function is triggered, allowing for the plugin to perform any required actions
given the event.

The plugins are checked in the order defined
[here](plugins/event_processing.md).

### Tick Processing

Roughly once every 0.05 seconds, FL Studio calls the `OnIdle()` callback
function. During this time, the script does various operations to keep things
running smoothly. The following steps are taken.

* The script context manager performs preprocessor checks. If it has been too
  long since the last tick, this current tick is skipped to prevent FL
  Studio from behaving badly due to lag.

* The active plugins are updated.

* The current state is ticked. This is usually the main state. In the main
  state:

  * Plugins are ticked using [this order](plugins/event_processing.md).

  * The device is ticked.

    * Control matchers are ticked.

      * Control surfaces are ticked.
