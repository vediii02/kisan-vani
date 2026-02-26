from sqlalchemy.ext.asyncio import AsyncSession
from db.models.kb_entry import KBEntry
from core.config import settings
import logging

logger = logging.getLogger(__name__)

class KBLoader:
    def __init__(self):
        pass
    
    async def load_entry_to_vector_db(self, kb_entry: KBEntry):
        """KB Loader without RAG - just logs the entry"""
        if not kb_entry.is_approved or kb_entry.is_banned:
            logger.warning(f"Skipping KB entry {kb_entry.id} - not approved or banned")
            return
        
        logger.info(f"KB entry {kb_entry.id} processed: {kb_entry.title}")
        # RAG functionality removed - entries are just logged now

kb_loader = KBLoader()
