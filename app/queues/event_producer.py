from app.core.redis_client import redis_client
from app.constants import EVENT_QUEUE
import json
import logging

logger = logging.getLogger(__name__)

async def enqueue_event(event: dict):
    try:
        await redis_client.rpush(EVENT_QUEUE, json.dumps(event))
        logger.info(f"✅ Event queued: {event}")
    except Exception as e:
        logger.error(f"❌ Failed to queue event: {e}")
        