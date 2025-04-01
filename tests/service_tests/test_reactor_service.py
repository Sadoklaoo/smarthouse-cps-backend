import asyncio
import pytest
from unittest.mock import patch, MagicMock
from app.services.event_pool import EventPool
from app.services.reactor_service import ReactorService
from app.services.consequence_pool import consequence_pool
from app.models.event import Event


# Test for process_event
@pytest.mark.asyncio
@patch("app.services.reactor_service.ReactorService.process_event")
async def test_process_event(mock_process_event):
    # Create a mock event
    mock_event = MagicMock(spec=Event)
    mock_event.event_type = "motion_detected"
    mock_event.device_id = 1
    mock_event.timestamp = "2025-03-25T12:00:00Z"

    # Mock the async method
    mock_process_event.return_value = asyncio.Future()
    mock_process_event.return_value.set_result(None)

    # Create a mock event pool
    mock_event_pool = MagicMock(spec=EventPool)

    # Create an instance of ReactorService with mock event pool
    reactor_service = ReactorService(event_pool=mock_event_pool)

    # Process the event
    await reactor_service.process_event(mock_event)

    # Ensure the event was processed
    mock_process_event.assert_called_once_with(mock_event)


# Test for reactor_service_action_trigger
@pytest.mark.asyncio
async def test_reactor_service_action_trigger():
    # Create a mock event
    mock_event = MagicMock(spec=Event)
    mock_event.event_type = "motion_detected"
    mock_event.device_id = 1
    mock_event.timestamp = "2025-03-25T12:00:00Z"

    # Mock the event pool (if needed by the method)
    mock_event_pool = MagicMock(spec=EventPool)

    # Create an instance of ReactorService
    reactor_service = ReactorService(event_pool=mock_event_pool)

    # Trigger the event reaction
    action, result = reactor_service.react_to_event(mock_event)

    # Ensure the correct action was taken
    assert len(consequence_pool.pool) == 1

    consequence_data = consequence_pool.pool[0].to_dict() 

    assert consequence_data["action"] == "turn_on_lights"
    assert consequence_data["result"] == "lights_on"