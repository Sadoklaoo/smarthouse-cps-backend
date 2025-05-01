import pytest
from unittest.mock import patch, MagicMock
from unittest.mock import AsyncMock
from app.services.consequence_service import get_consequence_by_id, mark_consequence_as_executed


@pytest.mark.asyncio
async def test_get_consequence_by_id():
    # Valid 24-character hex string for ObjectId
    mock_consequence = MagicMock()
    mock_consequence.id = "60f5c4a1b4c32f1b5c1d34c5"  # Valid 24-character ObjectId

    with patch('app.services.consequence_service.Consequence.get', return_value=mock_consequence):
        consequence = await get_consequence_by_id("60f5c4a1b4c32f1b5c1d34c5")
        assert consequence.id == "60f5c4a1b4c32f1b5c1d34c5"


@pytest.mark.asyncio
async def test_mark_consequence_as_executed():
    # Mocking the consequence object
    mock_consequence = MagicMock()
    mock_consequence.id = "consequence_123"
    mock_consequence.status = "pending"
    mock_consequence.save = AsyncMock()  # Mocking async save

    with patch('app.services.consequence_service.get_consequence_by_id', return_value=mock_consequence):
        executed_consequence = await mark_consequence_as_executed("consequence_123")

        # Ensure the consequence was marked as executed
        assert executed_consequence.status == "executed"
        mock_consequence.save.assert_called_once()  # Verify save was called once