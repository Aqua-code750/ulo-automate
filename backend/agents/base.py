import abc
from typing import Any, Dict, List

class BaseAgent(abc.ABC):
    def __init__(self, name: str, role: str):
        self.name = name
        self.role = role
        self.memory: List[Dict[str, Any]] = []

    def add_to_memory(self, message: Dict[str, Any]):
        self.memory.append(message)

    @abc.abstractmethod
    def execute(self, task: str, context: Dict[str, Any] = None) -> str:
        """Execute a task and return the result as a string."""
        pass
