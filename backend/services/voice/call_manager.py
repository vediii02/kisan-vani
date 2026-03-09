import asyncio
import logging
from typing import Set
from services.config_service import get_platform_config

logger = logging.getLogger(__name__)

class CallManager:
    def __init__(self):
        self._active_sessions: Set[str] = set()
        self._lock = asyncio.Lock()

    async def can_start_call(self) -> bool:
        """Check if a new call can start based on platform config."""
        config = await get_platform_config()
        max_calls = config.get("max_concurrent_calls", 100)
        
        async with self._lock:
            if len(self._active_sessions) >= max_calls:
                logger.warning(f"Max concurrent calls reached ({max_calls}). Rejecting new call.")
                return False
            return True

    async def register_call(self, session_id: str):
        """Register an active call session."""
        async with self._lock:
            self._active_sessions.add(session_id)
            logger.info(f"Call registered. Active: {len(self._active_sessions)}")

    async def unregister_call(self, session_id: str):
        """Unregister a call session."""
        async with self._lock:
            if session_id in self._active_sessions:
                self._active_sessions.remove(session_id)
                logger.info(f"Call unregistered. Active: {len(self._active_sessions)}")

    def get_active_count(self) -> int:
        return len(self._active_sessions)

# Global instance
call_manager = CallManager()
