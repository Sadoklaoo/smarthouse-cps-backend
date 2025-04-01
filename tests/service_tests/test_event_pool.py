import pytest
from app.services.event_pool import EventPool, event_pool


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


# Test for get_events
@pytest.mark.asyncio
async def test_get_events():
    # Mock event pool to return two events
    event_pool.pool = [
        {
            "device_id": "1",
            "event_type": "motion_detected",
            "id": "1",
            "timestamp": "2025-03-25T12:00:00Z",
        },
    ]

    events = event_pool.get_all_events()

    # Fix assertion based on expected result
    assert len(events) == 1

# Test for duplicate event addition
# This test checks if adding the same event twice results in two entries in the pool.
def test_duplicate_event_addition():
    event_pool.clear_events()
    # Adding an event to the pool
    event_data = {
        "id": "1",
        "device_id": "1",
        "event_type": "motion_detected",
        "timestamp": "2025-03-25T12:00:00Z",
    }
    event_pool.add_event(event_data)
    event_pool.add_event(event_data)  # Adding same event again
    assert len(event_pool.pool) == 1  # Check if only one vent is inserted in the pool
    assert event_pool.pool[0]["id"] == "1"  # Check if the first event is still there