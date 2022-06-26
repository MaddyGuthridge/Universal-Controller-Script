
# Event Filters

Import from `plugs.event_filters` and `plugs.tick_filters`

Filters are decorators that filter out events that shouldn't be processed
by a callback function. They provide a simple way to ensure type safety, and
add repetitive functionality.

Event filters should be used to decorate registered event callbacks, and tick
filters should be used to decorate the tick function of your plugin class.

## Filter parameters
A number of callback parameters are provided to customize the filter's
behavior.

* `method`: Whether the function we're decorating is a member function.
  Defaults to `True`, and should be unset if the callback isn't a member
  function of your plugin class.

* `enforce`: Whether to raise an exception if the event is filtered. This could
  be useful for detecting incorrect behavior in the script. Defaults to
  `False`.

* `filtered_return`

### `filterButtonLift`
Filter out button events if the button is being lifted. Only usable for events.

### `toPluginIndex`
Filter out events when the index is not a plugin

### `toGeneratorIndex`
Filter out events when the index is not a generator plugin

### `toEffectIndex`
Filter out events when the index is not an effect plugin

### `toWindowIndex`
Filter out events when the index is not a window

### `toSafeIndex`
Filter out events when the index is None

## Example Usage

To decorate an event callback so that it is guaranteed to be a generator plugin

```py
@event_filters.toGeneratorIndex()
def callback(
    self,
    control: ControlShadowEvent,
    index: GeneratorIndex,
    *args: Any
) -> bool:
    print("Received callback")
    return True
```

To decorate an event callback that isn't bound to a class.

```py
@event_filters.toGeneratorIndex(method=False)
def callback(
    control: ControlShadowEvent,
    index: GeneratorIndex,
    *args: Any
) -> bool:
    print("Received callback")
    return True
```

To decorate the tick method of a plugin class.

```py
@tick_filters.toGeneratorIndex()
def tick(self, index: GeneratorIndex):
    print("Ticking a generator")
```
