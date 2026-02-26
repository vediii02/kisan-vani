"""
Production Advisory Service using Gemini AI
"""

import google.generativeai as genai
from core.config import settings
import logging
import os

logger = logging.getLogger(__name__)


class GeminiAdvisoryService:
    """Production-ready advisory service with Gemini"""
    
    def __init__(self):
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-pro')
    
    async def generate_advisory(self, farmer_query: str, session_id: str) -> dict:
        """Generate agricultural advisory using Gemini without RAG"""
        try:
            system_message = """You are an agricultural expert assistant for Kisan Vani AI. 
            Provide helpful, practical advice to farmers about crops, pests, diseases, and farming practices.
            Keep responses concise and actionable. If you're unsure about something, admit it."""
            
            prompt = f"{system_message}\n\nFarmer Query: {farmer_query}\n\nProvide helpful advice:"
            
            response = await self.model.generate_content_async(prompt)
            
            answer = response.text
            
            return {
                "answer": answer,
                "confidence": 0.8,
                "sources": [],
                "escalate": False
            }
            
        except Exception as e:
            logger.error(f"Error generating advisory with Gemini: {str(e)}")
            return {
                "answer": "मुझे खेद है, मैं अभी आपकी सहायता नहीं कर सकता। कृपया बाद में फिर से प्रयास करें।",
                "confidence": 0.0,
                "sources": [],
                "escalate": True
            }
