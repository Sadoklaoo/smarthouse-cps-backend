import pytest
from app.services.event_pool import event_pool


def test_add_event():
    # Adding an event to the pool
    event_data = {
        "id": "1",
        "device_id": "1",
        "event_type": "motion_detected",
        "timestamp": "2025-03-25T12:00:00Z",
    }
    event_pool.add_event(event_data)

    # Check if the event was added
    assert len(event_pool.pool) == 1
    assert event_pool.pool[0]["event_type"] == "motion_detected"


def test_get_events():
    # Adding an event to the pool
    event_data = {
        "id": "1",
        "device_id": "1",
        "event_type": "motion_detected",
        "timestamp": "2025-03-25T12:00:00Z",
    }
    event_pool.add_event(event_data)

    # Get the events from the pool
    events = event_pool.get_all_events()

    assert len(events) == 1
    assert events[0]["event_type"] == "motion_detected"
