from collections import deque
from typing import List, Tuple


class RollingMemory:
    """A simple rolling memory that keeps the last N messages.

    Stores tuples of (role, text) where role is 'user' or 'assistant'.
    """

    def __init__(self, capacity: int = 10):
        self.capacity = capacity
        self._deque = deque(maxlen=capacity)

    def add(self, role: str, text: str) -> None:
        self._deque.append((role, text))

    def get(self) -> List[Tuple[str, str]]:
        return list(self._deque)

    def clear(self) -> None:
        self._deque.clear()
