import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock
from app.main import app  # Import the FastAPI app instance
from app.schemas.event import EventCreate, EventRead
from app.services.event_service import log_event
from app.queues.event_producer import enqueue_event

# Create a TestClient to interact with the FastAPI app
client = TestClient(app)

# Sample event data for testing
EVENT_DATA = {
    "event_type": "temperature_change",
    "device_id": "device_123",
    "data": {"temperature": 26},
    "timestamp": "2025-05-01T00:00:00Z"
}


# Test for creating an event (POST /monitor/)
@pytest.mark.asyncio
async def test_create_event():
    event_data = EVENT_DATA

    # Mock the log_event function to return a fake event
    with patch('app.services.event_service.log_event', AsyncMock(return_value=MagicMock(id="event_123", **event_data))):
        response = client.post("/monitor/", json=event_data)

        # Ensure the response status code is 200 OK
        assert response.status_code == 200

        # Check the event data in the response
        response_json = response.json()
        assert response_json['event_type'] == event_data['event_type']
        assert response_json['device_id'] == event_data['device_id']
        assert response_json['data'] == event_data['data']
        assert response_json['timestamp'] == event_data['timestamp']


# Test for triggering an event (POST /monitor/trigger)
@pytest.mark.asyncio
async def test_trigger_event():
    event = {
        "type": "temperature_change",
        "sensor_id": "abc123",
        "temperature": 26,
        "timestamp": "2025-05-01T00:00:00Z"
    }

    # Mock the enqueue_event function to prevent actual queue operation
    with patch('app.queues.event_producer.enqueue_event', AsyncMock()):
        response = client.post("/monitor/trigger")

        # Ensure the response status code is 200 OK
        assert response.status_code == 200

        # Check the message in the response
        response_json = response.json()
        assert response_json['message'] == "Event queued"
        assert response_json['event'] == event


# Test for event creation failure (simulating error in log_event)
@pytest.mark.asyncio
async def test_create_event_failure():
    event_data = EVENT_DATA

    # Mock log_event to raise an error
    with patch('app.services.event_service.log_event', AsyncMock(side_effect=Exception("Event creation failed"))):
        response = client.post("/monitor/", json=event_data)

        # Ensure the response status code is 500 Internal Server Error
        assert response.status_code == 500
        assert response.json()['detail'] == "Error registering event: Event creation failed"


# Test for event trigger failure (simulating error in enqueue_event)
@pytest.mark.asyncio
async def test_trigger_event_failure():
    event = {
        "type": "temperature_change",
        "sensor_id": "abc123",
        "temperature": 26,
        "timestamp": "2025-05-01T00:00:00Z"
    }

    # Mock enqueue_event to raise an error
    with patch('app.queues.event_producer.enqueue_event', AsyncMock(side_effect=Exception("Failed to enqueue event"))):
        response = client.post("/monitor/trigger")

        # Ensure the response status code is 500 Internal Server Error
        assert response.status_code == 500
        assert response.json()['detail'] == "Error processing event in Reactor"
