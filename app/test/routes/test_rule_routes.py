import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock
from app.main import app  # Import the FastAPI app
from app.models.rule import Rule
from app.schemas.rule import RuleCreate
from bson import ObjectId  # Import ObjectId to mock it

client = TestClient(app)


# Helper function to mock ObjectId generation for tests
def mock_object_id():
    return ObjectId()


# Test for creating a rule
@pytest.mark.asyncio
async def test_create_rule():
    # Prepare mock data for creating a rule
    rule_data = {
        "name": "Temperature rule",
        "trigger_type": "temperature_change",
        "condition": {"temperature": 25},
        "operator": ">",
        "target_device_id": "device_123",
        "action": "turn_on_heater",
    }

    # Mock Rule creation method in services
    with patch("app.services.rule_service.create_rule", AsyncMock(return_value=Rule(**rule_data, id=mock_object_id()))):
        response = client.post("/rules/", json=rule_data)

        # Assert the status code and content of the response
        assert response.status_code == 201
        response_data = response.json()
        assert response_data["name"] == "Temperature rule"
        assert response_data["trigger_type"] == "temperature_change"
        assert response_data["condition"] == {"temperature": 25}
        assert response_data["operator"] == ">"
        assert response_data["target_device_id"] == "device_123"
        assert response_data["action"] == "turn_on_heater"


# Test for fetching all rules
@pytest.mark.asyncio
async def test_list_rules():
    # Prepare mock data for multiple rules
    rule_data_1 = Rule(id=mock_object_id(), name="Temperature rule", trigger_type="temperature_change",
                       condition={"temperature": 25}, operator=">", target_device_id="device_123",
                       action="turn_on_heater", created_at="2023-05-01")
    rule_data_2 = Rule(id=mock_object_id(), name="Humidity rule", trigger_type="humidity_change",
                       condition={"humidity": 70}, operator="<", target_device_id="device_456",
                       action="turn_on_air_conditioner", created_at="2023-05-02")

    with patch("app.services.rule_service.get_all_rules", AsyncMock(return_value=[rule_data_1, rule_data_2])):
        response = client.get("/rules/")

        # Assert the status code and content of the response
        assert response.status_code == 200
        response_data = response.json()
        assert len(response_data) == 2
        assert response_data[0]["name"] == "Temperature rule"
        assert response_data[1]["name"] == "Humidity rule"


# Test for deleting a rule
@pytest.mark.asyncio
async def test_delete_rule():
    rule_id = str(mock_object_id())  # Convert mock ObjectId to string
    with patch("app.services.rule_service.delete_rule_by_id", AsyncMock(return_value=True)) as mock_delete_rule:
        response = client.delete(f"/rules/{rule_id}/")

        # Assert the status code of the response
        assert response.status_code == 204

    with patch("app.services.rule_service.delete_rule_by_id", AsyncMock(return_value=False)) as mock_delete_rule:
        response = client.delete(f"/rules/{rule_id}/")

        # Assert the response if rule is not found
        assert response.status_code == 404
        assert response.json() == {"detail": "Rule not found"}
