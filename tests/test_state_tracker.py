import pytest
from src.state_tracker import StateTracker

@pytest.fixture
def tracker():
    return StateTracker()

def test_add_and_get_states(tracker):
    tracker.add_state("AAPL", "Entered")
    tracker.add_state("AAPL", "Exited")
    states = tracker.get_states("AAPL")
    assert isinstance(states, list)
    assert states == ["Entered", "Exited"]

def test_get_states_empty(tracker):
    assert tracker.get_states("UNKNOWN") == []
