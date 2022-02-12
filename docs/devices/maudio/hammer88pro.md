
# M-Audio Hammer 88 Pro

## Setup

In order for the controller to work correctly, DAW and Preset configurations
need to be sent to the device.

1. Open the Hammer 88 Pro Preset Editor Program (this can be installed with the
   included software bundle for your controller).
2. Ensure that the Preset tab is selected.
3. In the file menu, choose "Load Preset". Navigate to the script's folder, then
   choose the device's configuration from the 
   `resources/deviceconfigs/maudio/hammer88pro` folder.
4. In the file menu, choose "Send Preset", and send the preset to RAM.
5. Use the "Send Preset" tool again to send it to a bank of your choosing.
   Note that if you don't choose Bank 1, this preset won't be loaded by default
   in by the keyboard.
6. Switch to the DAW tab, then choose "Load Preset" again, selecting the 
   device's configuration again.
7. Use the "Send Preset" tool again to send the configuration to the device.
8. Open FL Studio's MIDI Settings, and set a port for the controller listed as
   `MIDIIN3 (Hammer 88 Pro)` in both the input and output sections. Assign this
   device to the controller type "Universal Event Forwarded (user)", so that
   events from this script can be forwarded to the main script to be processed.

## Usage

#### Bank Selection
Currently, the script doesn't support bank switching. Please keep your device on
bank 1.

#### Jog Wheel Usage
The controller can behave differently depending on the state of the jog wheel.
When it is used normally, it will change selections and scroll. If it is turned
while pressed, it will either move items, or scroll along a different axis.

## Who to contact
This device is maintained by Miguel Guthridge. [Email](mailto:hdsq@outlook.com),
Discord: ***HDSQ#2154***.
