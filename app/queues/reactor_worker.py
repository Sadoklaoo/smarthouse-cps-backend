import datetime
from app.core.redis_client import redis_client
from app.constants import EVENT_QUEUE
import json
import logging
import asyncio

from app.models.consequence import Consequence
from app.services.consequence_service import mark_consequence_as_executed
from app.services.rule_service import get_matching_rules

logger = logging.getLogger(__name__)

async def consume_events():
    while True:
        try:
            _, event_data = await redis_client.blpop(EVENT_QUEUE)
            event = json.loads(event_data)
            logger.info(f"⚡ Event received by reactor: {event}")

            # TODO: process the event, call consequences, etc.
            await handle_event(event)

        except Exception as e:
            logger.error(f"❌ Error processing event: {e}")
        await asyncio.sleep(0.1)  # avoid tight loop

async def handle_event(event: dict):
    matching_rules = await get_matching_rules(event)
    
    if not matching_rules:
        print("🚫 No matching rules found for this event.")
        return

    for rule in matching_rules:
        consequence = Consequence(
            event_id=event.get("event_id", "event-auto"),
            rule_id=str(rule.id),
            action=rule.action,
            device_id=rule.target_device_id,
            status="pending"
        )
        await consequence.insert()
        print(f"📝 Logged consequence: {consequence}")

        # Simulate execution
        print(f"⚙️  Executing action: {rule.action} on device {rule.target_device_id}")
        await mark_consequence_as_executed(str(consequence.id))