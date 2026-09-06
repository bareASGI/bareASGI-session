"""Session Storage"""

from typing import Any

from .session_storage import SessionStorage


class MemorySessionStorage(SessionStorage[dict[str, Any]]):
    """Memory session storage"""

    def __init__(self) -> None:
        """Memory session storage"""
        self.sessions: dict[str, dict[str, Any]] = {}

    async def load(self, key: str) -> dict[str, Any]:
        return self.sessions.setdefault(key, {})

    async def save(self, key: str, session: dict[str, Any]) -> None:
        self.sessions[key] = session
