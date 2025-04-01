from app.models.event import Event
from app.services.consequence_pool import consequence_pool


class ReactorService:
    def __init__(self, event_pool):
        # Event to action mapping
        self.event_actions = {
            "motion_detected": ("turn_on_lights", "lights_on"),
            "temperature_high": ("turn_on_ac", "ac_on"),
            "door_opened": ("send_alert", "alert_sent"),
        }
        # Store the event pool instance
        self.event_pool = event_pool

    def process_event(self, event: Event):
        """Process the event and trigger the corresponding action."""
        action, result = self.react_to_event(event)
        # Log the action to the consequence pool
        consequence_pool.add_consequence(action, result)
        # Print the action and result
        print(f"Action triggered: {action} | Result: {result}")

    def react_to_event(self, event: Event):
        """React to the event by triggering an action."""
        # Get the action and result based on the event type
        action, result = self.event_actions.get(
            event.event_type, ("no_action", "no_action")
        )

        # Store the consequence in consequence_pool
        consequence_pool.add_consequence(action, result)

        # Optional: Log the triggered action and result for debugging
        print(f"Triggered action: {action} for event: {event.event_type}")

        return action, result

    def handle_event(self, event: Event):
        """Handle event processing."""
        print(f"Handling event: {event.event_type} from Device {event.device_id}")
        self.process_event(event)
