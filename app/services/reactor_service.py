from app.models.rule import Rule
from app.models.event import Event
from app.models.consequence import Consequence
from fastapi import HTTPException
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  # 👈 make sure logs are visible

def compare(value: float, operator: str, target: float) -> bool:
    if operator == ">":
        return value > target
    if operator == "<":
        return value < target
    if operator == "==":
        return value == target
    return False

async def process_event(event: Event):
    try:
        logger.info(f"🔁 Reactor triggered for event type: {event.event_type}")
        
        # ✅ Step 1: Get matching rules
        rules = await Rule.find(Rule.trigger_type == event.event_type).to_list()
        logger.info(f"Found {len(rules)} rule(s) matching event type '{event.event_type}'")

        for rule in rules:
            logger.info(f"Evaluating rule: {rule.name} for device {rule.target_device_id}")
            for key, threshold in rule.condition.items():
                event_value = event.data.get(key)
                logger.info(f"Condition: event[{key}] = {event_value}, rule {rule.operator} {threshold}")

                if event_value is not None and compare(event_value, rule.operator, threshold):
                    logger.info(f"✅ Rule '{rule.name}' triggered by event {event.id} (value: {event_value})")

                    consequence = Consequence(
                        event_id=str(event.id),
                        rule_id=str(rule.id),
                        action=rule.action,
                        device_id=rule.target_device_id,
                        status="pending"
                    )

                    await consequence.insert()
                    logger.info(f"📦 Consequence created for device {rule.target_device_id}")

    except Exception as e:
        logger.error(f"🚨 Error in reactor: {e}")
        raise HTTPException(status_code=500, detail="Error processing event in Reactor")
