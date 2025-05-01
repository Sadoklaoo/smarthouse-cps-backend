import pytest
from fastapi import HTTPException

from unittest.mock import patch, MagicMock, AsyncMock
from app.services.rule_service import (
    get_matching_rules,
    create_rule,
    get_all_rules,
    delete_rule_by_id
)
from app.schemas.rule import RuleCreate
from app.models.rule import Rule

# Mock data
VALID_RULE_ID = "60f5c4a1b4c32f1b5c1d34c5"
EVENT_DATA = {
    "type": "temperature_change",
    "temperature": 28.0
}
RULE_CREATE_DATA = RuleCreate(
    name="Temperature Rule",
    trigger_type="temperature_change",
    condition={"temperature": 28.0},
    operator="==",
    target_device_id="device_123",
    action="turn_on_heater"
)


# Test for creating a rule
@pytest.mark.asyncio
async def test_create_rule():
    mock_rule = MagicMock()
    mock_rule.name = "Temperature Rule"
    mock_rule.trigger_type = "temperature_change"
    mock_rule.condition = {"temperature": 28.0}
    mock_rule.operator = "=="
    mock_rule.insert = AsyncMock()

    with patch('app.services.rule_service.Rule', return_value=mock_rule):
        rule = await create_rule(RULE_CREATE_DATA)

        # Ensure insert was called and the rule is created
        mock_rule.insert.assert_called_once()
        assert rule.name == "Temperature Rule"
        assert rule.trigger_type == "temperature_change"
        assert rule.condition == {"temperature": 28.0}
        assert rule.operator == "=="


# Test for getting all rules
@pytest.mark.asyncio
async def test_get_all_rules():
    mock_rule = MagicMock()
    mock_rule.name = "Temperature Rule"

    # Patch the find_all method to return an AsyncMock with to_list() method
    mock_async_query = AsyncMock()
    mock_async_query.to_list.return_value = [mock_rule]

    with patch('app.services.rule_service.Rule.find_all', return_value=mock_async_query):
        rules = await get_all_rules()
        assert len(rules) > 0
        assert rules[0].name == "Temperature Rule"


# Test for getting matching rules based on event
@pytest.mark.asyncio
async def test_get_matching_rules():
    mock_rule = MagicMock()
    mock_rule.trigger_type = "temperature_change"
    mock_rule.condition = {"temperature": 28.0}
    mock_rule.operator = "=="
    mock_rule.id = VALID_RULE_ID

    # Patch the find_all method to return an AsyncMock with to_list() method
    mock_async_query = AsyncMock()
    mock_async_query.to_list.return_value = [mock_rule]

    with patch('app.services.rule_service.Rule.find_all', return_value=mock_async_query):
        matched_rules = await get_matching_rules(EVENT_DATA)
        assert len(matched_rules) == 1
        assert matched_rules[0].id == VALID_RULE_ID


# Test for deleting a rule by ID
@pytest.mark.asyncio
async def test_delete_rule_by_id():
    mock_rule = MagicMock()
    mock_rule.id = VALID_RULE_ID
    mock_rule.delete = AsyncMock()

    with patch('app.services.rule_service.Rule.get', return_value=mock_rule):
        result = await delete_rule_by_id(VALID_RULE_ID)
        assert result is True
        mock_rule.delete.assert_called_once()


# Test for deleting a rule that doesn't exist
@pytest.mark.asyncio
async def test_delete_rule_not_found():
    with patch('app.services.rule_service.Rule.get', return_value=None):
        with pytest.raises(HTTPException):
            await delete_rule_by_id(VALID_RULE_ID)
