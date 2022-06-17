
# Annotation Manager

Annotation managers are used to provide an interface between the script and
text displays on a device. They can be used to control text displays associated
with a control, or to control a global LED text display.

## Methods to Implement

* `onAnnotationChange()`: called when the annotation should be updated.

* `tick()`: called frequently, so annotations can be refreshed even when they
  haven't explicitly been changed.


# Color Manager

Color managers are used to provide an interface between the script and LEDs on
a device.

## Methods to Implement

* `onColorChange()`: called when the color should be updated.

* `tick()`: called frequently, so colors can be refreshed even when they
  haven't explicitly been changed.


# Value Manager

Value managers are used to provide an interface between the script and
motorized controls on a device.

## Methods to Implement

* `onValueChange()`: called when the value should be updated.

* `tick()`: called frequently, so values can be refreshed even when they
  haven't explicitly been changed.
