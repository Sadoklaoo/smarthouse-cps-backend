import pytest
from unittest.mock import patch, MagicMock
from app.services.monitor_service import MonitorService
from app.models.event import Event
from app.services.event_pool import event_pool


@pytest.mark.asyncio
@patch("app.services.monitor_service.MonitorService.fetch_latest_events")
async def test_monitor_house(mock_fetch_events):
    # Mock the database call to return a list of events
    mock_event = MagicMock(spec=Event)
    mock_event.event_type = "motion_detected"
    mock_event.device_id = 1
    mock_event.timestamp = "2025-03-25T12:00:00Z"

    mock_fetch_events.return_value = [mock_event]

    # Call the method
    await MonitorService.monitor_house()

    # Ensure that the event was added to the event pool
    assert len(event_pool.pool) == 1
    assert event_pool.pool[0]["event_type"] == "motion_detected"
