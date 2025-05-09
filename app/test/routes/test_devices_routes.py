import pytest
from fastapi import status
from httpx import AsyncClient
from unittest.mock import AsyncMock, patch
from app.main import app

# Sample data matching your MongoDB
DEVICE_ID = "681254121c823e6ce30ea0fa"  # Smart Light device
USER_ID = "60f5c4a1bc432ffb5c1d34c5"    # User ID for Smart Light devices
NON_EXISTENT_DEVICE_ID = "nonexistent123"
NON_EXISTENT_USER_ID = "nonexistent456"

DEVICE_DATA = {
    "name": "Test Device",
    "type": "Sensor",
    "location": "Kitchen",
    "user_id": USER_ID,
    "is_active": True
}

DEVICE_READ = {
    "id": DEVICE_ID,
    "name": "Smart Light",
    "type": "Light",
    "location": "Living Room",
    "user_id": USER_ID,
    "is_active": True,
    "registered_at": "2025-04-21T12:52:48.436+00:00"
}

USER_DEVICES = [
    {
        "id": "681254121c823e6ce30ea0fa",
        "name": "Smart Light",
        "type": "Light",
        "location": "Living Room",
        "user_id": USER_ID,
        "is_active": True,
        "registered_at": "2025-04-21T12:52:48.436+00:00"
    },
    {
        "id": "681254971c823e6ce30ea0fc",
        "name": "Smart Light",
        "type": "Light",
        "location": "Living Room",
        "user_id": USER_ID,
        "is_active": True,
        "registered_at": "2025-04-21T12:52:48.436+00:00"
    }
]

@pytest.mark.asyncio
async def test_create_device_route():
    # Arrange
    mock_device = AsyncMock()
    mock_device.id = "newdevice123"
    mock_device.name = DEVICE_DATA["name"]
    mock_device.type = DEVICE_DATA["type"]
    mock_device.location = DEVICE_DATA["location"]
    mock_device.user_id = USER_ID
    mock_device.is_active = DEVICE_DATA["is_active"]
    mock_device.registered_at = "2025-04-21T12:52:48.436+00:00"

    with patch("app.routers.devices_routes.create_device", return_value=mock_device) as mock_create:
        async with AsyncClient(app=app, base_url="http://test") as client:
            # Act
            response = await client.post("/api/devices/", json=DEVICE_DATA)

            # Assert
            assert response.status_code == status.HTTP_201_CREATED
            assert response.json() == {
                "id": "newdevice123",
                "name": "Test Device",
                "type": "Sensor",
                "location": "Kitchen",
                "user_id": USER_ID,
                "is_active": True,
                "registered_at": "2025-04-21T12:52:48.436+00:00"
            }
            mock_create.assert_awaited_once()

@pytest.mark.asyncio
async def test_get_device():
    # Arrange
    mock_device = AsyncMock()
    mock_device.id = DEVICE_ID
    mock_device.name = "Smart Light"
    mock_device.type = "Light"
    mock_device.location = "Living Room"
    mock_device.user_id = USER_ID
    mock_device.is_active = True
    mock_device.registered_at = "2025-04-21T12:52:48.436+00:00"

    with patch("app.routers.devices_routes.get_device_by_id", return_value=mock_device) as mock_get:
        async with AsyncClient(app=app, base_url="http://test") as client:
            # Act
            response = await client.get(f"/api/devices/{DEVICE_ID}")

            # Assert
            assert response.status_code == status.HTTP_200_OK
            assert response.json() == DEVICE_READ
            mock_get.assert_awaited_once_with(DEVICE_ID)

@pytest.mark.asyncio
async def test_get_device_not_found():
    # Arrange
    with patch("app.routers.devices_routes.get_device_by_id", return_value=None) as mock_get:
        async with AsyncClient(app=app, base_url="http://test") as client:
            # Act
            response = await client.get(f"/api/devices/{NON_EXISTENT_DEVICE_ID}")

            # Assert
            assert response.status_code == status.HTTP_404_NOT_FOUND
            assert response.json()["detail"] == "Device not found"
            mock_get.assert_awaited_once_with(NON_EXISTENT_DEVICE_ID)

@pytest.mark.asyncio
async def test_get_devices_for_user():
    # Arrange
    mock_devices = []
    for device_data in USER_DEVICES:
        mock_device = AsyncMock()
        mock_device.id = device_data["id"]
        mock_device.name = device_data["name"]
        mock_device.type = device_data["type"]
        mock_device.location = device_data["location"]
        mock_device.user_id = device_data["user_id"]
        mock_device.is_active = device_data["is_active"]
        mock_device.registered_at = device_data["registered_at"]
        mock_devices.append(mock_device)

    with patch("app.routers.devices_routes.get_devices_by_user", return_value=mock_devices) as mock_get:
        async with AsyncClient(app=app, base_url="http://test") as client:
            # Act
            response = await client.get(f"/api/devices/user/{USER_ID}")

            # Assert
            assert response.status_code == status.HTTP_200_OK
            assert response.json() == USER_DEVICES
            mock_get.assert_awaited_once_with(USER_ID)

@pytest.mark.asyncio
async def test_get_devices_for_user_not_found():
    # Arrange
    with patch("app.routers.devices_routes.get_devices_by_user", return_value=[]) as mock_get:
        async with AsyncClient(app=app, base_url="http://test") as client:
            # Act
            response = await client.get(f"/api/devices/user/{NON_EXISTENT_USER_ID}")

            # Assert
            assert response.status_code == status.HTTP_404_NOT_FOUND
            assert response.json()["detail"] == "No devices found for this user"
            mock_get.assert_awaited_once_with(NON_EXISTENT_USER_ID)

@pytest.mark.asyncio
async def test_update_device_route():
    # Arrange
    update_data = {"name": "Updated Smart Light", "is_active": False}
    mock_device = AsyncMock()
    mock_device.id = DEVICE_ID
    mock_device.name = "Updated Smart Light"
    mock_device.type = "Light"
    mock_device.location = "Living Room"
    mock_device.user_id = USER_ID
    mock_device.is_active = False
    mock_device.registered_at = "2025-04-21T12:52:48.436+00:00"

    with patch("app.routers.devices_routes.update_device", return_value=mock_device) as mock_update:
        async with AsyncClient(app=app, base_url="http://test") as client:
            # Act
            response = await client.put(f"/api/devices/{DEVICE_ID}", json=update_data)

            # Assert
            assert response.status_code == status.HTTP_200_OK
            assert response.json() == {
                "id": DEVICE_ID,
                "name": "Updated Smart Light",
                "type": "Light",
                "location": "Living Room",
                "user_id": USER_ID,
                "is_active": False,
                "registered_at": "2025-04-21T12:52:48.436+00:00"
            }
            mock_update.assert_awaited_once()

@pytest.mark.asyncio
async def test_update_device_route_not_found():
    # Arrange
    update_data = {"name": "Updated Device", "is_active": False}
    with patch("app.routers.devices_routes.update_device", return_value=None) as mock_update:
        async with AsyncClient(app=app, base_url="http://test") as client:
            # Act
            response = await client.put(f"/api/devices/{NON_EXISTENT_DEVICE_ID}", json=update_data)

            # Assert
            assert response.status_code == status.HTTP_404_NOT_FOUND
            assert response.json()["detail"] == "Device not found"
            mock_update.assert_awaited_once()

@pytest.mark.asyncio
async def test_delete_device_route():
    # Arrange
    with patch("app.routers.devices_routes.delete_device", return_value=True) as mock_delete:
        async with AsyncClient(app=app, base_url="http://test") as client:
            # Act
            response = await client.delete(f"/api/devices/{DEVICE_ID}")

            # Assert
            assert response.status_code == status.HTTP_204_NO_CONTENT
            assert response.text == ""
            mock_delete.assert_awaited_once_with(DEVICE_ID)

@pytest.mark.asyncio
async def test_delete_device_route_not_found():
    # Arrange
    with patch("app.routers.devices_routes.delete_device", return_value=False) as mock_delete:
        async with AsyncClient(app=app, base_url="http://test") as client:
            # Act
            response = await client.delete(f"/api/devices/{NON_EXISTENT_DEVICE_ID}")

            # Assert
            assert response.status_code == status.HTTP_404_NOT_FOUND
            assert response.json()["detail"] == "Device not found"
            mock_delete.assert_awaited_once_with(NON_EXISTENT_DEVICE_ID)