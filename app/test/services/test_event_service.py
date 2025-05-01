import pytest
from unittest.mock import patch, MagicMock
from unittest.mock import AsyncMock
from datetime import datetime, timezone
from app.services.event_service import log_event
from app.schemas.event import EventCreate
from fastapi import HTTPException

# Mock event data for testing
mock_event_data = {
    "device_id": "60f5c4a1b4c32f1b5c1d34c5",
    "event_type": "motion_detected",
    "data": {"temperature": 23.5},
}


@pytest.mark.asyncio
async def test_log_event_success():
    # Create a mock Event instance
    mock_event = MagicMock()
    mock_event.device_id = "60f5c4a1b4c32f1b5c1d34c5"
    mock_event.event_type = "motion_detected"
    mock_event.data = {"temperature": 23.5}
    mock_event.timestamp = datetime.now(timezone.utc)  # Fix deprecation warning: use timezone-aware datetime
    mock_event.id = "60f5c4a1b4c32f1b5c1d34c6"

    # Mock async 'insert' method using AsyncMock
    mock_event.insert = AsyncMock()

    # Patch the Event model and the process_event function
    with patch('app.services.event_service.Event', return_value=mock_event), \
            patch('app.services.event_service.process_event', new_callable=AsyncMock) as mock_process_event:
        # Create an EventCreate schema instance
        event_in = EventCreate(**mock_event_data)

        # Call the log_event function
        event = await log_event(event_in)

        # Ensure that the event was logged and inserted correctly
        assert event.device_id == mock_event_data["device_id"]
        assert event.event_type == mock_event_data["event_type"]
        assert event.id is not None

        # Verify that the insert method was called once
        mock_event.insert.assert_called_once()

        # Verify that the process_event function was called once
        mock_process_event.assert_called_once_with(event)


@pytest.mark.asyncio
async def test_log_event_failure():
    # Simulate an exception in the log_event method
    with patch('app.services.event_service.Event', side_effect=Exception("Database error")):
        event_in = EventCreate(**mock_event_data)

        # Check if an exception is raised
        with pytest.raises(HTTPException) as exc_info:
            await log_event(event_in)

        assert exc_info.value.status_code == 500
        assert "Error logging event" in str(exc_info.value.detail)