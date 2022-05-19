
# Device Detection

Various methods are used to attempt to identify the device. These are each
checked in the following order.

## 1. Name Associations

The user can configure the script to map a device name to a particular device
definition by modifying their `config.py` file. Note that this method is
deprecated, and may be removed in the future, since it places the burden of
configuration onto users.

## 2. Universal Device Enquiry

The script sends out the MIDI equivalent of a "who are you?". It sends a
message where all standard devices should respond with a unique identifier that
gives information on the device's manufacturer, family, model and revision.

This info is compared with patterns provided by each device. If the event
matches the universal enquiry response pattern of a device definition, then
we have found a matching device.

## 3. Name Matching

Each device is given an opportunity to match the device given its name in FL
Studio. This should only be used when a device does not provide a valid
response to the universal device enquiry, as the name of a device differs
depending on the OS it is connected to which can make implementations difficult
to create and maintain.
