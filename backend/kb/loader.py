import os
import logging
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from openai import AsyncOpenAI

from db.base import AsyncSessionLocal
from db.models.kb_entry import KBEntry
from db.models.knowledge_base import KnowledgeEntry

logger = logging.getLogger(__name__)

class KBLoader:
    def __init__(self):
        self.openai_client = None

    def _get_openai_client(self):
        if not self.openai_client:
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                logger.error("OPENAI_API_KEY is not set. Cannot generate embeddings.")
                return None
            self.openai_client = AsyncOpenAI(api_key=api_key)
        return self.openai_client
    
    async def load_entry_to_vector_db(self, kb_entry: KBEntry):
        """Generates OpenAI embedding and saves it to knowledge_entries table."""
        if not kb_entry.is_approved or kb_entry.is_banned:
            logger.warning(f"Skipping KB entry {kb_entry.id} - not approved or banned")
            return
        
        client = self._get_openai_client()
        if not client:
            return

        try:
            # Construct a comprehensive text representation
            content_parts = [
                f"Title: {kb_entry.title}",
                f"Crop: {kb_entry.crop_name or 'N/A'}",
                f"Problem Type: {kb_entry.problem_type or 'N/A'}",
                f"Description: {kb_entry.content}",
                f"Solution: {kb_entry.solution_steps or 'N/A'}",
                f"Tags: {kb_entry.tags or 'N/A'}"
            ]
            embed_text = "\n".join([p for p in content_parts if p])
            full_content_text = f"Title: {kb_entry.title}\n{kb_entry.content}\nSolution: {kb_entry.solution_steps or ''}"

            logger.info(f"Generating OpenAI embedding for KB entry {kb_entry.id}")
            response = await client.embeddings.create(
                input=embed_text,
                model="text-embedding-3-small",
            )
            embedding_vector = response.data[0].embedding
            source_id = f"kb_entry:{kb_entry.id}"

            async with AsyncSessionLocal() as db:
                # Find existing KnowledgeEntry if it exists
                stmt = select(KnowledgeEntry).where(KnowledgeEntry.source == source_id)
                result = await db.execute(stmt)
                knowledge_entry = result.scalar_one_or_none()
                
                if knowledge_entry:
                    # Update existing
                    knowledge_entry.organisation_id = kb_entry.organisation_id
                    knowledge_entry.crop = kb_entry.crop_name
                    knowledge_entry.problem_type = kb_entry.problem_type
                    knowledge_entry.content = full_content_text
                    knowledge_entry.embedding = embedding_vector
                    
                    # We commit to save changes.
                    await db.commit()
                    logger.info(f"Updated existing KnowledgeEntry for kb_entry {kb_entry.id}")
                else:
                    # Create new
                    knowledge_entry = KnowledgeEntry(
                        organisation_id=kb_entry.organisation_id,
                        company_id=None,
                        crop=kb_entry.crop_name,
                        problem_type=kb_entry.problem_type,
                        source=source_id,
                        content=full_content_text,
                        embedding=embedding_vector
                    )
                    db.add(knowledge_entry)
                    await db.commit()
                    logger.info(f"Created new KnowledgeEntry with embedding for kb_entry {kb_entry.id}")

        except Exception as e:
            logger.error(f"Error generating or saving embedding for kb_entry {kb_entry.id}: {e}")

kb_loader = KBLoader()
