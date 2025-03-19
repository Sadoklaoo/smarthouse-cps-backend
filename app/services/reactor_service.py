from app.services.event_pool import event_pool
from app.services.consequence_pool import consequence_pool


class ReactorService:
    """Listens for events and triggers actions based on predefined rules."""

    def process_event(self):
        """Check EventPool and trigger appropriate actions."""
        events = event_pool.get_all_events()
        for event in events:
            action = self.get_action_for_event(event["event_type"])
            if action:
                consequence_pool.add_consequence({"event": event, "action": action})
                print(f"Action triggered: {action} for event {event['event_type']}")

    def get_action_for_event(self, event_type: str):
        """Define rules for triggering actions based on event type."""
        rules = {
            "motion_detected": "turn_on_light",
            "temp_high": "turn_on_air_conditioning",
            "door_opened": "send_alert",
        }
        return rules.get(event_type)


# Global instance
reactor_service = ReactorService()
