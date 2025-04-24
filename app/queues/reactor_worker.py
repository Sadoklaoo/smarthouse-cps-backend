import datetime
from app.core.redis_client import redis_client
from app.constants import EVENT_QUEUE
import json
import logging
import asyncio

from app.models.consequence import Consequence
from app.services.consequence_service import mark_consequence_as_executed

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
    # 🔧 Logic to trigger device actions or log to ConsequencePool
    print(f"🚀 Triggering consequence for event: {event}")
    # Example fake rule + action — you'll plug in real ones later
    rule_id = "rule-manual"
    action = "turn_on"
    device_id = event.get("sensor_id")

    consequence = Consequence(
        event_id=event.get("event_id", "event-manual"),
        rule_id=rule_id,
        action=action,
        device_id=device_id,
        status="pending",
        timestamp=datetime.datetime.utcnow()
    )

    await consequence.insert()
    print(f"📝 Logged consequence: {consequence}")


    # 2. Simulate action (e.g., turning on a light)
    print(f"💡 Simulating action: {action} on {device_id}")

    # 3. Mark consequence as executed
    updated = await mark_consequence_as_executed(str(consequence.id))
    print(f"✅ Marked consequence as executed: {updated.id}")