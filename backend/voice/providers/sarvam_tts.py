"""
Sarvam AI Text-to-Speech Provider for Kisan Vani AI
Uses Sarvam AI Python SDK with API key
"""

import os
import logging
import base64
from typing import Optional
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)


class BaseTTSProvider(ABC):
    @abstractmethod
    async def synthesize(self, text: str, language: str = 'hi') -> bytes:
        pass


class SarvamTTSProvider(BaseTTSProvider):
    """Sarvam AI Text-to-Speech provider using Python SDK"""
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "bulbul:v3",
        speaker: str = "pooja",  # Changed to pooja as requested
        pace: float = 1.0,
        sample_rate: int = 24000,
        audio_format: str = "wav"
    ):
        self.api_key = api_key or os.getenv('SARVAM_API_KEY')
        self.model = model
        self.speaker = speaker
        self.pace = pace
        self.sample_rate = sample_rate
        self.audio_format = audio_format
        
        if not self.api_key:
            logger.warning("⚠️ No Sarvam API key provided - TTS will fail")
        else:
            try:
                from sarvamai import SarvamAI
                self.client = SarvamAI(api_subscription_key=self.api_key)
                logger.info(f"✅ Sarvam AI TTS initialized with API key (model: {model}, speaker: {speaker})")
            except ImportError as e:
                logger.error(f"❌ Failed to import Sarvam AI: {e}")
                self.client = None
    
    async def synthesize(self, text: str, language: str = 'hi') -> bytes:
        """Convert text to speech using Sarvam AI TTS SDK"""
        
        if not text or not text.strip():
            logger.warning("Empty text provided")
            return b""
        
        if not self.api_key or not self.client:
            logger.error("❌ No API key or client - cannot synthesize")
            return b""
        
        # Truncate if too long (Sarvam supports longer text, but we'll be safe)
        MAX_LENGTH = 5000
        if len(text) > MAX_LENGTH:
            logger.warning(f"Text too long ({len(text)} chars), truncating")
            text = text[:MAX_LENGTH]
        
        try:
            # Language mapping for Sarvam AI
            language_map = {
                'hi': 'hi-IN',
                'hi-IN': 'hi-IN',
                'en': 'en-IN',
                'en-IN': 'en-IN',
                'bn': 'bn-IN',
                'bn-IN': 'bn-IN',
                'ta': 'ta-IN',
                'ta-IN': 'ta-IN',
                'te': 'te-IN',
                'te-IN': 'te-IN',
                'kn': 'kn-IN',
                'kn-IN': 'kn-IN',
                'ml': 'ml-IN',
                'ml-IN': 'ml-IN',
                'mr': 'mr-IN',
                'mr-IN': 'mr-IN',
                'gu': 'gu-IN',
                'gu-IN': 'gu-IN',
                'pa': 'pa-IN',
                'pa-IN': 'pa-IN',
                'or': 'or-IN',
                'or-IN': 'or-IN'
            }
            lang_code = language_map.get(language, 'hi-IN')
            
            logger.info(f"🎤 Synthesizing with Sarvam AI TTS: '{text[:50]}...' | Model: {self.model}, Speaker: {self.speaker}")
            
            # Use Sarvam AI SDK to convert text to speech
            response = self.client.text_to_speech.convert(
                target_language_code=lang_code,
                text=text,
                model=self.model,
                speaker=self.speaker,
                pace=self.pace
            )
            
            # Extract audio data from the response
            if hasattr(response, 'audio'):
                audio_data = response.audio
            elif hasattr(response, 'audio_content'):
                audio_data = response.audio_content
            elif hasattr(response, 'data'):
                audio_data = response.data
            else:
                # Try to get audio from response attributes
                audio_data = getattr(response, 'audio', None) or getattr(response, 'data', None)
            
            if not audio_data:
                logger.error(f"❌ No audio data in Sarvam response: {response}")
                return b""
            
            # Convert to bytes if needed
            if isinstance(audio_data, str):
                # If it's a base64 string, decode it
                try:
                    audio_data = base64.b64decode(audio_data)
                except:
                    logger.error("❌ Failed to decode audio data")
                    return b""
            elif hasattr(audio_data, 'read'):
                audio_data = audio_data.read()
            elif not isinstance(audio_data, bytes):
                logger.error(f"❌ Unexpected audio data type: {type(audio_data)}")
                return b""
            
            logger.info(f"✅ Synthesized {len(audio_data):,} bytes with Sarvam AI TTS")
            return audio_data
            
        except Exception as e:
            logger.error(f"❌ Sarvam AI TTS synthesis failed: {e}")
            return b""
    
    def get_available_voices(self, language_code: str = 'hi-IN') -> dict:
        """Get available voices for Sarvam AI TTS"""
        # Common voices for different languages
        voices = {
            'hi-IN': ['shubh', 'meera', 'arush', 'anaya'],
            'en-IN': ['shubh', 'meera', 'arush', 'anaya'],
            'bn-IN': ['shubh', 'meera'],
            'ta-IN': ['shubh', 'meera'],
            'te-IN': ['shubh', 'meera'],
            'kn-IN': ['shubh', 'meera'],
            'ml-IN': ['shubh', 'meera'],
            'mr-IN': ['shubh', 'meera'],
            'gu-IN': ['shubh', 'meera'],
            'pa-IN': ['shubh', 'meera'],
            'or-IN': ['shubh', 'meera']
        }
        return voices.get(language_code, ['shubh', 'meera'])
    
    def get_supported_languages(self) -> list:
        """Get list of supported languages"""
        return [
            'hi-IN',  # Hindi
            'en-IN',  # English (Indian accent)
            'bn-IN',  # Bengali
            'ta-IN',  # Tamil
            'te-IN',  # Telugu
            'kn-IN',  # Kannada
            'ml-IN',  # Malayalam
            'mr-IN',  # Marathi
            'gu-IN',  # Gujarati
            'pa-IN',  # Punjabi
            'or-IN'   # Odia
        ]
