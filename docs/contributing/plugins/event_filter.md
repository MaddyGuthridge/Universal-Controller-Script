
# Event Filters

Import from `plugs.event_filters`

Event filters are decorators that filter out events that shouldn't be processed
by a callback function. They provide a simple way to ensure type safety, and
add simple functionality.

## `filterButtonLift`
Filter out button events if the button is being lifted.

## `filterToPluginIndex`
Filter out events when the index is not a plugin

## `filterToGeneratorIndex`
Filter out events when the index is not a generator plugin

## `filterToEffectIndex`
Filter out events when the index is not an effect plugin

## `filterToWindowIndex`
Filter out events when the index is not a window

## `filterToSafeIndex`
Filter out events when the index is None
