"""Defines the abstract base class for all AI agents."""

from abc import ABC, abstractmethod
from typing import List, Dict, Any
from datetime import datetime, timezone
import logging

logger = logging.getLogger(__name__)

class Agent(ABC):
    """Abstract base class for an AI agent."""

    def __init__(self, name: str):
        """Initializes the agent."""
        if not name:
            raise ValueError("Agent must have a name.")
        self.name = name
        self.interaction_history: List[Dict[str, Any]] = []
        logger.info(f"Agent '{self.name}' initialized.")

    @abstractmethod
    def execute_task(self, task_details: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executes a given task based on the provided details.

        Args:
            task_details: A dictionary containing information about the task.

        Returns:
            A dictionary containing the result of the task execution.
        """
        pass

    @abstractmethod
    def get_capabilities(self) -> List[str]:
        """
        Returns a list of capabilities or specializations of the agent.
        """
        pass

    def log_interaction(self, task_input: Dict[str, Any], task_output: Dict[str, Any]):
        """Logs an interaction (task input and output) to the agent's history."""
        log_entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "input": task_input,
            "output": task_output
        }
        self.interaction_history.append(log_entry)
        logger.debug(f"Interaction logged for agent '{self.name}': {log_entry}")

    def get_history(self) -> List[Dict[str, Any]]:
        """Returns the interaction history of the agent."""
        return self.interaction_history

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name='{self.name}')"