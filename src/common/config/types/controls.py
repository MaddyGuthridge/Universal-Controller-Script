from typing import TypedDict


class ControlSurfaceConfig(TypedDict):
    """
    Configuration of options for control surfaces
    """

    double_press_time: float
    """The time in seconds for which a double press is valid"""

    long_press_time: float
    """
    The time in seconds required to register a long press

    NOTE: This is currently not implemented, but will be used to implement
    things such as long press scrolling.
    """

    short_press_time: float
    """
    The maximum duration in seconds for which a button press is considered
    short.

    This is used for buttons that usually repeat over time, but have a
    different action is pressed and released quickly.
    """

    navigation_speed: int
    """
    How fast to navigate when long-pressing a direction button. This roughly
    corresponds to the number of times the action will be performed per second.
    """

    use_snap: bool
    """
    Whether values that have a centred default value (eg panning) should snap
    to the centred value when values are close.
    """

    use_undo_toggle: bool
    """
    Whether the undo/redo button should act as a toggle between undo and redo.

    * If `True`, it will redo unless there is nothing to redo, in which case it
      will undo
    * If `False`, it will always undo

    Note that devices with separate undo and redo buttons are not affected by
    this option.
    """

    score_log_dump_length: int
    """
    The length of time to dump to a pattern from the score log when a
    capture MIDI button is pressed, in seconds.
    """
