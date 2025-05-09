import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from app.main import app  # Assuming your FastAPI app is initialized in app.main

client = TestClient(app)

# Mock data for ConsequenceRead
mock_consequence_data = {
    "id": "12345",
    "event_id": "event-123",
    "rule_id": "rule-123",
    "action": "turn_on_device",
    "device_id": "device-123",
    "status": "pending",
    "timestamp": "2025-05-01T12:00:00.000Z"
}


# Test list all consequences
@pytest.mark.asyncio
async def test_list_consequences():
    with patch('app.services.consequence_service.get_all_consequences') as mock_get_all_consequences:
        mock_get_all_consequences.return_value = [mock_consequence_data]

        response = client.get("/consequences/")

        assert response.status_code == 200
        assert len(response.json()) == 1
        assert response.json()[0]["id"] == mock_consequence_data["id"]
        assert response.json()[0]["event_id"] == mock_consequence_data["event_id"]
        assert response.json()[0]["rule_id"] == mock_consequence_data["rule_id"]
        assert response.json()[0]["action"] == mock_consequence_data["action"]
        assert response.json()[0]["device_id"] == mock_consequence_data["device_id"]
        assert response.json()[0]["status"] == mock_consequence_data["status"]


# Test getting a consequence by ID
@pytest.mark.asyncio
async def test_get_consequence_by_id():
    with patch('app.services.consequence_service.get_consequence_by_id') as mock_get_consequence_by_id:
        mock_get_consequence_by_id.return_value = mock_consequence_data

        consequence_id = "12345"
        response = client.get(f"/consequences/{consequence_id}")

        assert response.status_code == 200
        assert response.json()["id"] == mock_consequence_data["id"]
        assert response.json()["event_id"] == mock_consequence_data["event_id"]
        assert response.json()["rule_id"] == mock_consequence_data["rule_id"]
        assert response.json()["action"] == mock_consequence_data["action"]
        assert response.json()["device_id"] == mock_consequence_data["device_id"]
        assert response.json()["status"] == mock_consequence_data["status"]


# Test mark consequence as executed
@pytest.mark.asyncio
async def test_execute_consequence():
    with patch('app.services.consequence_service.mark_consequence_as_executed') as mock_mark_consequence_as_executed:
        mock_mark_consequence_as_executed.return_value = mock_consequence_data

        consequence_id = "12345"
        response = client.put(f"/consequences/{consequence_id}/execute")

        assert response.status_code == 200
        assert response.json()["id"] == mock_consequence_data["id"]
        assert response.json()["status"] == "pending"  # Assuming mock does not update the status
        assert response.json()["timestamp"] == mock_consequence_data["timestamp"]


# Test getting a consequence by ID not found (404 error)
@pytest.mark.asyncio
async def test_get_consequence_not_found():
    with patch('app.services.consequence_service.get_consequence_by_id',
               side_effect=Exception("Consequence not found")):
        consequence_id = "nonexistent_id"
        response = client.get(f"/consequences/{consequence_id}")

        assert response.status_code == 404
        assert "Consequence not found" in response.json()["detail"]


# Test mark consequence as executed when it fails (500 error)
@pytest.mark.asyncio
async def test_execute_consequence_fail():
    with patch('app.services.consequence_service.mark_consequence_as_executed',
               side_effect=Exception("Error executing consequence")):
        consequence_id = "12345"
        response = client.put(f"/consequences/{consequence_id}/execute")

        assert response.status_code == 500
        assert "Error executing consequence" in response.json()["detail"]
