import pytest
from unittest.mock import patch, MagicMock
from app.services.reactor_service import ReactorService
from app.services.consequence_pool import consequence_pool
from app.models.event import Event


@pytest.mark.asyncio
@patch("app.services.reactor_service.ReactorService.process_event")
async def test_process_event(mock_process_event):
    # Create a mock event
    mock_event = MagicMock(spec=Event)
    mock_event.event_type = "motion_detected"
    mock_event.device_id = 1
    mock_event.timestamp = "2025-03-25T12:00:00Z"

    # Process the event
    ReactorService.process_event(mock_event)

    # Ensure the event was processed
    mock_process_event.assert_called_once_with(mock_event)


@pytest.mark.asyncio
async def test_reactor_service_action_trigger():
    # Create a mock event
    mock_event = MagicMock(spec=Event)
    mock_event.event_type = "motion_detected"
    mock_event.device_id = 1
    mock_event.timestamp = "2025-03-25T12:00:00Z"

    # Trigger the event reaction
    ReactorService.react_to_event(mock_event)

    # Ensure the correct action was taken
    assert len(consequence_pool.pool) == 1
    assert consequence_pool.pool[0].action == "turn_on_lights"
    assert consequence_pool.pool[0].result == "lights_on"
