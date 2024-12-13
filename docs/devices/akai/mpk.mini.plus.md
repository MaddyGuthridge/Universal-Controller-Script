
# Akai MPK Mini Plus

## Pre-Setup - Loading the controller configuration file

1. Download the `Akai Professional MPK mini Plus Program Editor` from <https://www.akaipro.com/downloads.html#mpkminiplus>

2. `File -> Open` the `FLStudio2024.mpkminiplus` file in the `Akai Professional MPK mini Plus Program Editor`

3. `File -> Send Program` to `Program 4` which will overwrite the old default for FL Studio with the correct version.

## Setup - Selecting the correct controller program

Continuing from the primary setup instructions.

1. Press the `PROG SELECT` button and use the rotary controller by the OLED screen to select `PGM4: FLStudio2024`.

## Device Details

* In FPC, the banks of drums are mapped as `BANK A` for the bottom 2 rows and `BANK B` for the top row. The pad colours
  broadly reflect this, but are not currently set dynamically from FPC.

* Currently, there is only a drum pad mode implemented for the pads.

* The 8 rotary encoders are set to endless encode / relative mode and work correctly in plugins supported by the
  Universal Controller script.

* The transport controls work correctly for `<<`, `>>`, `STOP`, `PLAY` and `REC`. The `SEQ` button is not implemented.

* The Pitch Wheel is mapped to `Channel pitch` in FL Studio and the Mod Wheel is correctly mapped to `MIDI CC 01 - Mod Wheel`

* The joystick can be used to navigate around the mixer channels or the channel rack sequencer buttons. Not sure that
  is much use but it works.

* This configuration only works on the 1.x series of the Universal Controller script currently. The beta 2.x series breaks
  the Pitch bend and Mod Wheel linkages when plugins are selected.

## Who to contact

This device is maintained by Jon Baker. [Email](mailto:baker_jon_r@yahoo.co.uk),
Discord: ***jrb101***.
