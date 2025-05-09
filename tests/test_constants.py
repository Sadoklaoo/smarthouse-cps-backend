import pytest
from app import constants

def test_event_queue_constant():
    assert constants.EVENT_QUEUE == "event_queue"
