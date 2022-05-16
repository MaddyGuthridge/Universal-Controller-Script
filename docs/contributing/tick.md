
# Tick Hierarchy

Roughly once every 0.05 seconds, FL Studio calls the `OnIdle()` callback
function. During this time, the script does various operations to keep things
running smoothly. The following steps are taken.

* The script context manager performs preprocessor checks. If it has been too
  long since the last tick, this current tick is skipped to prevent FL
  Studio from behaving badly.
* The active plugins are updated
* The current state is ticked. This is usually the main state.
    * Special plugins are ticked
    * The current plugin is ticked
    * Final special plugins are ticked
* The device is ticked
    * Control matchers are ticked
        * Control surfaces are ticked
