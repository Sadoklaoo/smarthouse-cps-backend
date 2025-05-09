import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from app.services.reactor_service import process_event, compare
from fastapi import HTTPException

# Sample data for testing
EVENT_DATA = {
    "id": "event_123",
    "event_type": "temperature_change",
    "data": {"temperature": 28.0}
}

RULE_DATA = {
    "id": "rule_123",
    "name": "Temperature Rule",
    "trigger_type": "temperature_change",
    "condition": {"temperature": 28.0},
    "operator": "==",
    "action": "turn_on_heater",
    "target_device_id": "device_123"
}

# Mock Event object
@pytest.fixture
def mock_event():
    event = MagicMock()
    event.id = "event_123"
    event.event_type = "temperature_change"
    event.data = {"temperature": 28.0}
    return event

# Mock Rule object
@pytest.fixture
def mock_rule():
    rule = MagicMock()
    rule.id = "rule_123"
    rule.name = "Temperature Rule"
    rule.trigger_type = "temperature_change"
    rule.condition = {"temperature": 28.0}
    rule.operator = "=="
    rule.action = "turn_on_heater"
    rule.target_device_id = "device_123"
    return rule

# Mock Consequence object
@pytest.fixture
def mock_consequence():
    consequence = MagicMock()
    consequence.id = "consequence_123"
    consequence.event_id = "event_123"
    consequence.rule_id = "rule_123"
    consequence.action = "turn_on_heater"
    consequence.device_id = "device_123"
    consequence.status = "pending"
    return consequence

# Test for process_event when the event triggers a rule
@pytest.mark.asyncio
async def test_process_event_trigger_rule(mock_event, mock_rule, mock_consequence):
    # Mock Rule.find to return the mock rule wrapped in a list
    with patch('app.services.reactor_service.Rule.find', AsyncMock(return_value=[mock_rule])), \
         patch('app.services.reactor_service.Consequence.insert', AsyncMock()) as mock_insert:

        # Call the process_event function
        await process_event(mock_event)

        # Ensure Consequence.insert was called
        mock_insert.assert_called_once()

        # Check that the consequence was created for the correct device
        mock_insert.assert_called_with()  # Ensure insert was called
        print("Test passed successfully")


# Test for process_event when no rule is triggered
@pytest.mark.asyncio
async def test_process_event_no_rule_triggered(mock_event, mock_rule):
    # Mock Rule.find to return no matching rules
    with patch('app.services.reactor_service.Rule.find', AsyncMock(return_value=[])):
        await process_event(mock_event)

        # Since there are no rules, the Consequence.insert should not be called
        with patch('app.services.reactor_service.Consequence.insert', AsyncMock()) as mock_insert:
            mock_insert.assert_not_called()


# Test for process_event when there is an error in processing
@pytest.mark.asyncio
async def test_process_event_error(mock_event, mock_rule):
    # Mock Rule.find to raise an error
    with patch('app.services.reactor_service.Rule.find', AsyncMock(side_effect=Exception("Test error"))):
        with pytest.raises(HTTPException) as exc_info:
            await process_event(mock_event)

        assert exc_info.value.status_code == 500
        assert "Error processing event in Reactor" in str(exc_info.value.detail)


# Test for the compare function used within process_event
@pytest.mark.parametrize("value, operator, target, expected", [
    (29, ">", 28, True),
    (27, "<", 28, True),
    (28, "==", 28, True),
    (30, "<", 28, False)
])
def test_compare(value, operator, target, expected):
    result = compare(value, operator, target)
    assert result == expected


# Test for process_event when there are matching rules (testing the full flow with mock Rule objects)
@pytest.mark.asyncio
async def test_process_event_with_matching_rule(mock_event, mock_rule, mock_consequence):
    # Mock Rule.find to return the mock rule
    with patch('app.services.reactor_service.Rule.find', AsyncMock(return_value=[mock_rule])), \
         patch('app.services.reactor_service.Consequence.insert', AsyncMock()):

        await process_event(mock_event)

        # Ensure Consequence.insert was called
        mock_consequence.insert.assert_called_once()

        # Ensure the consequence was created correctly
        mock_consequence.insert.assert_called_with()

