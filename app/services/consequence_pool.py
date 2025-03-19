from typing import List, Dict, Any
from datetime import datetime


# Consequence class to store the action, result, and timestamp
class Consequence:
    # Initialize the Consequence object with action, result, and timestamp
    def __init__(self, action: str, result: str, timestamp: datetime):
        self.action = action  # Action triggered by the event (e.g., "turn_on_lights")
        self.result = result  # Result of the action (e.g., "lights_on")
        self.timestamp = timestamp  # When the action was executed

    # Convert the Consequence object to a dictionary
    def to_dict(self) -> Dict[str, Any]:
        return {
            "action": self.action,
            "result": self.result,
            "timestamp": self.timestamp.isoformat(),
        }


# ConsequencePool class to store and manage Consequence objects
class ConsequencePool:
    # Initialize the ConsequencePool with an empty pool of Consequence objects
    def __init__(self):
        self.pool: List[Consequence] = []

    # Add a consequence to the pool
    def add_consequence(self, action: str, result: str) -> None:
        """
        Add a consequence to the pool.
        """
        consequence = Consequence(action, result, datetime.now())
        self.pool.append(consequence)

    # Get all stored consequences
    def get_consequences(self) -> List[Dict[str, Any]]:
        """
        Return a list of stored consequences in dictionary form.
        """
        return [consequence.to_dict() for consequence in self.pool]

    # Get the last stored consequence
    def get_last_consequence(self) -> Dict[str, Any]:
        """
        Return the last stored consequence in dictionary form.
        """
        if self.pool:
            return self.pool[-1].to_dict()
        return {}

    # Clear all stored consequences
    def clear_pool(self) -> None:
        """
        Clears all stored consequences.
        """
        self.pool.clear()


# Singleton instance for the ConsequencePool
consequence_pool = ConsequencePool()
