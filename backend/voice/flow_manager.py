from typing import Dict, Optional
from core.provider_registry import provider_registry
from core.config import settings
import logging

logger = logging.getLogger(__name__)

class FlowManager:
    def __init__(self):
        self.stt_provider = None
        self.tts_provider = None
    
    async def initialize(self):
        self.stt_provider = provider_registry.get_stt(settings.DEFAULT_STT_PROVIDER)
        
        # Pass API key for TTS providers that need it
        tts_kwargs = {}
        if settings.DEFAULT_TTS_PROVIDER == 'sarvam' and settings.SARVAM_API_KEY:
            tts_kwargs['api_key'] = settings.SARVAM_API_KEY
        elif settings.DEFAULT_TTS_PROVIDER == 'sarvam-streaming' and settings.SARVAM_API_KEY:
            tts_kwargs['api_key'] = settings.SARVAM_API_KEY
        elif settings.DEFAULT_TTS_PROVIDER == 'google' and settings.GOOGLE_TTS_API_KEY:
            tts_kwargs['api_key'] = settings.GOOGLE_TTS_API_KEY
            
        self.tts_provider = provider_registry.get_tts(settings.DEFAULT_TTS_PROVIDER, **tts_kwargs)
        logger.info(f"Initialized voice flow with STT: {settings.DEFAULT_STT_PROVIDER}, TTS: {settings.DEFAULT_TTS_PROVIDER}")
    
    async def process_audio(self, audio_data: bytes) -> str:
        if not self.stt_provider:
            await self.initialize()
        
        transcribed_text = await self.stt_provider.transcribe(audio_data)
        logger.info(f"Transcribed: {transcribed_text}")
        return transcribed_text
    
    async def generate_audio_response(self, text: str, language: str = 'hi') -> bytes:
        if not self.tts_provider:
            await self.initialize()
        
        audio_data = await self.tts_provider.synthesize(text, language)
        logger.info(f"Generated audio for text length: {len(text)}")
        return audio_data

flow_manager = FlowManager()