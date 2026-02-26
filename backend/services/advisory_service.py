from openai import AsyncOpenAI
from core.config import settings
import logging

logger = logging.getLogger(__name__)

class AdvisoryService:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.EMERGENT_LLM_KEY)
    
    async def generate_advisory(self, farmer_query: str, session_id: str) -> dict:
        """Generate agricultural advisory using LLM without RAG"""
        try:
            system_message = """You are an agricultural expert assistant for Kisan Vani AI. 
            Provide helpful, practical advice to farmers about crops, pests, diseases, and farming practices.
            Keep responses concise and actionable. If you're unsure about something, admit it."""
            
            response = await self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": farmer_query}
                ],
                max_tokens=500,
                temperature=0.7
            )
            
            answer = response.choices[0].message.content
            
            return {
                "answer": answer,
                "confidence": 0.8,
                "sources": [],
                "escalate": False
            }
            
        except Exception as e:
            logger.error(f"Error generating advisory: {str(e)}")
            return {
                "answer": "मुझे खेद है, मैं अभी आपकी सहायता नहीं कर सकता। कृपया बाद में फिर से प्रयास करें।",
                "confidence": 0.0,
                "sources": [],
                "escalate": True
            }
