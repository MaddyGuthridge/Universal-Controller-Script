from typing import TypedDict


class DebugConfig(TypedDict):
    """
    Settings used for debugging
    """

    profiling_enabled: bool
    """Whether performance profiling should be enabled"""

    exec_tracing_enabled: bool
    """
    Whether profiling should print the tracing of profiler contexts
    within the script. Useful for troubleshooting crashes in FL Studio's
    MIDI API. Requires profiling to be enabled.

    Note that this causes a huge amount of output to be produced on the
    console, which can be immensely laggy. Only use it if absolutely necessary.
    """


class AdvancedConfig(TypedDict):
    """
    Advanced settings for the script. Don't edit these unless you know what
    you're doing, as they could cause the script to break, or behave badly.
    """

    debug: DebugConfig
    """
    Settings used for debugging the script
    """

    drop_tick_time: int
    """
    Time in ms during which we expect the script to be ticked. If the
    script doesn't tick during this time, then the script will consider
    itself to be constrained by performance, and will drop the next tick
    to prevent lag in FL Studio.
    """

    slow_tick_time: int
    """
    Time in ms for which a tick should be expected to complete. If
    ticking FL Studio takes longer than this, it will be recorded,
    regardless of whether profiling is enabled.
    """

    activity_history_length: int
    """
    The maximum length of the plugin/window tracking history
    """
