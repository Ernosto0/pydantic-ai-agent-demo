"""In-memory state management for user sessions."""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class UserState:
    """Tracks conversation state for a single user."""
    
    user_id: str
    last_intent: Optional[str] = None
    last_order_id: Optional[str] = None
    message_count: int = 0
    
    def update(
        self,
        intent: Optional[str] = None,
        order_id: Optional[str] = None,
    ) -> None:
        """Update state with new values."""
        if intent:
            self.last_intent = intent
        if order_id:
            self.last_order_id = order_id
        self.message_count += 1


# In-memory storage for all user states
_user_states: dict[str, UserState] = {}


def get_user_state(user_id: str) -> UserState:
    """Get or create state for a user."""
    if user_id not in _user_states:
        _user_states[user_id] = UserState(user_id=user_id)
    return _user_states[user_id]


def clear_user_state(user_id: str) -> None:
    """Clear state for a user."""
    if user_id in _user_states:
        del _user_states[user_id]


def get_all_states() -> dict[str, UserState]:
    """Get all user states (for debugging)."""
    return _user_states.copy()


