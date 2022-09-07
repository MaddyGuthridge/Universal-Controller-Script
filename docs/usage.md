
# Basic Usage

A few common functions are maintained throughout the entirety of the script.

Make sure you refer to your [device's page](devices/README.md) in the manual
for information on how these controls are implemented in particular for your
device. Every device is different, so it's a good idea to double check so you
can be sure you're getting the most out of the script.

## Basic Events

* Notes are sent to the selected plugin.

* After-touch is sent to the selected plugin if the plugin is a VST.

* Pedals are sent to the selected plugin if the plugin is a VST. Otherwise,
  the hold pedal increases note length (the default behavior in FL).

## Transport Controls

* Stop button stops playback

* Play button plays or pauses (playhead location isn't reset) playback.
  If no stop button is available, playback is stopped.

* Loop button switches the loop mode between pattern and song mode.

* Record button toggles recording.

* Fast forward and rewind buttons do what you'd expect.

* Jog wheel changes selection.

* Direction buttons (including next/previous track buttons) change the
  selection.

* Shift buttons may toggle between alternate functions for some buttons.
  Consult your device's documentation for more info. Note that double pressing
  a shift button will keep the shifted options enabled for standard
  implementations of shift buttons.

## Macros

* Metronome button toggles the metronome.

* Undo button undoes things.

* Save button hits save.

* Quantize button quantizes the selection.

* Capture MIDI button writes the last 2 minutes of MIDI data to the selected
  pattern.

## Manual Mappings

By default, the program will automatically map your device's controls to any
plugin which it supports. However, as not all plugins are supported, it is
possible to create manual links when no event handling is active.

To do this, activate an the plugin and choose your selected parameter.
For FL Studio plugins, you can right click and choose the "Link to controller"
button. For VST plugins, you can find the parameter in the "Current project"
section of the FL Studio browser and choose the "Link to controller" option in
the parameter's right click menu from there.

Note that if the script is automatically linking a control to a plugin
parameter already, it is impossible to manually create the mapping.

# Activity Management

The script tracks the active plugin and FL Studio window so that it can
automatically map controls the the most logical destinations.

There are two different ways that this can be managed, depending on the design
of your device. Make sure you know which one your device uses.

### Split Controls

FL Studio windows (mixer, channel rack, etc) are controlled separately to
plugins. Your device will let you select a DAW mode or a Plugin mode to
determine what will be controlled.

### Unified Controls

FL Studio windows are controlled alongside plugins. Your device will map
controls to whichever window or plugin is currently selected.

## Managing Activity

This activity can be controlled using the following controls:

* Pause active button prevents the active plugin or window selection from being
  updated, meaning that you can continue interfacing with that plugin, even if
  you change your selection.

* Switch Active button switches between window and plugin activity if a device
  with split controls is being used.

Note that if your device doesn't include a pause active button, the behavior
can be triggered manually from the script output window but entering the
command `getContext().activity.playPause()`.

# Plugin-specific Usage

For information on how the script interacts with FL Studio windows and
plugins, refer to the [plugins](plugins/README.md) section of the
documentation.
