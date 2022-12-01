"""
Tests for the step sequencer

* Are the dimensions mapped correctly for various drum pad layouts:
    * 2x4: 1 channel
    * 2x8 (Novation): 1 channel
    * 4x4 (MPC): 1 channel
    * 1x16: 1 channels
    * 2x16: 2 channels
    * 4x16 (Fire): 4 channels
* Does pressing a drum pad toggle the step
* Does pressing a drum pad toggle the correct channel (usually the selected)

TODO From here:

* Does moving up-down affect the toggled step
* Does moving left-right affect the toggled step (move by one beat)
* Does long-pressing then releasing a drum pad not cause the step to toggle
* Does long-pressing a drum pad cause the graph editor to open
    * Event editor shown
    * Colors for controls set
* Can we edit properties of steps when the graph editor is open
* Does editing the properties of a non-existent step cause that step to be set
* Does attempting to edit the properties of events when no steps are selected
  do nothing
* Can we edit the properties of multiple steps at once?
* When we edit the properties of multiple steps at once, do they scale
  correctly?
    * Notes and shift move parallel
    * Velocity and release scale from initial point
    * Pan, fine pitch, X and Y scale from centre
"""
import fl_model
from fl_model.channels import addSampler
import channels
from plugs.windows.channel_rack.sequence import StepSequencer
from devices import DeviceShadow
from tests.helpers.devices.drum_pad import (
    DummyDeviceDrumPads,
    IDummyDeviceDrumPads,
)
import pytest


CR_WINDOW_ID = 1
"""window ID of channel rack"""


@pytest.fixture(autouse=True)
def reset_model():
    """Reset the state between tests"""
    fl_model.resetState()


def get_drum_pad_presses(device: IDummyDeviceDrumPads, r: int, c: int):
    """
    Helper to get control events for a drum pad hit at the given coordinate
    """
    on = device.matchEvent(device.getEventForDrumPad(r, c, 1.0))
    off = device.matchEvent(device.getEventForDrumPad(r, c, 0.0))
    assert on is not None
    assert off is not None
    return on, off


@pytest.mark.parametrize(
    ('dimensions', 'num_channels', 'num_steps'),
    [
        ((2, 4), 1, 8),
        ((4, 4), 1, 16),
        ((8, 2), 1, 16),
        ((1, 16), 1, 16),
        ((2, 16), 2, 16),
        ((4, 16), 4, 16),
    ]
)
def test_dimension_mappings(
    dimensions: tuple[int, int],
    num_channels: int,
    num_steps: int,
):
    """Does the step sequencer map things to channels"""
    device = DummyDeviceDrumPads(*dimensions)
    sequencer = StepSequencer.create(DeviceShadow(device))

    layout = sequencer.getDrumLayout()

    assert len(layout) == dimensions[0]
    for row_num, row in enumerate(layout):
        assert len(row) == dimensions[1]
        # Expected channel should be scaled based on position within channels
        expected_channel = int(row_num / dimensions[0] * num_channels)
        for col_num, entry in enumerate(row):
            # Expected step should be total number of steps so far, minus steps
            # that were from other channels
            expected_step = (
                row_num * dimensions[1] + col_num
                - expected_channel * num_steps
            )
            assert entry == (expected_channel, expected_step)


def test_press_toggle_step():
    """Does pressing a drum pad toggle a step?"""
    device = DummyDeviceDrumPads(2, 8)
    sequencer = StepSequencer.create(DeviceShadow(device))
    device.matchEvent(device.getEventForDrumPad(0, 0, 1.0))
    on, off = get_drum_pad_presses(device, 0, 0)
    sequencer.processEvent(on, CR_WINDOW_ID)
    sequencer.processEvent(off, CR_WINDOW_ID)
    # Grid bit should be set
    assert channels.getGridBit(0, 0)


def test_toggles_correct_channel():
    """Does pressing a drum pad toggle the correct channel (the selected one)?
    """
    # Create and select a new channel
    addSampler('My sampler')
    channels.selectOneChannel(1)

    device = DummyDeviceDrumPads(2, 8)
    sequencer = StepSequencer.create(DeviceShadow(device))
    device.matchEvent(device.getEventForDrumPad(0, 0, 1.0))
    on, off = get_drum_pad_presses(device, 0, 0)
    sequencer.processEvent(on, CR_WINDOW_ID)
    sequencer.processEvent(off, CR_WINDOW_ID)
    # Grid bit on new channel should be set
    assert channels.getGridBit(1, 0)
