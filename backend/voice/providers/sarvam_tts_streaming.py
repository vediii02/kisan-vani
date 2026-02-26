"""
Sarvam AI Streaming Text-to-Speech Provider for Kisan Vani AI
Uses Sarvam AI streaming API for real-time audio generation
"""

import os
import logging
import requests
import tempfile
from typing import Optional, AsyncGenerator
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)


class BaseTTSProvider(ABC):
    @abstractmethod
    async def synthesize(self, text: str, language: str = 'hi') -> bytes:
        pass


class SarvamStreamingTTSProvider(BaseTTSProvider):
    """Sarvam AI Streaming Text-to-Speech provider using streaming API"""
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "bulbul:v3",
        speaker: str = "pooja",  # Changed to pooja as requested
        pace: float = 1.1,
        speech_sample_rate: int = 22050,
        output_audio_codec: str = "mp3",
        enable_preprocessing: bool = True
    ):
        self.api_key = api_key or os.getenv('SARVAM_API_KEY')
        self.model = model
        self.speaker = speaker
        self.pace = pace
        self.speech_sample_rate = speech_sample_rate
        self.output_audio_codec = output_audio_codec
        self.enable_preprocessing = enable_preprocessing
        self.api_url = "https://api.sarvam.ai/text-to-speech/stream"
        
        if not self.api_key:
            logger.warning("⚠️ No Sarvam API key provided - TTS will fail")
        else:
            logger.info(f"✅ Sarvam AI Streaming TTS initialized with API key (model: {model}, speaker: {speaker})")
    
    async def synthesize(self, text: str, language: str = 'hi') -> bytes:
        """Convert text to speech using Sarvam AI streaming API"""
        
        if not text or not text.strip():
            logger.warning("Empty text provided")
            return b""
        
        if not self.api_key:
            logger.error("❌ No API key - cannot synthesize")
            return b""
        
        # Truncate if too long
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
            
            headers = {
                "api-subscription-key": self.api_key,
                "Content-Type": "application/json"
            }
            
            payload = {
                "text": text,
                "target_language_code": lang_code,
                "speaker": self.speaker,
                "model": self.model,
                "pace": self.pace,
                "speech_sample_rate": self.speech_sample_rate,
                "output_audio_codec": self.output_audio_codec,
                "enable_preprocessing": self.enable_preprocessing
            }
            
            logger.info(f"🎤 Streaming TTS with Sarvam AI: '{text[:50]}...' | Model: {self.model}, Speaker: {self.speaker}")
            
            # Stream the response
            with requests.post(self.api_url, headers=headers, json=payload, stream=True) as response:
                response.raise_for_status()
                
                # Save to temporary file as chunks arrive
                with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as temp_file:
                    total_bytes = 0
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            temp_file.write(chunk)
                            total_bytes += len(chunk)
                            logger.debug(f"Received {len(chunk)} bytes")
                    
                    temp_file_path = temp_file.name
                    logger.info(f"✅ Streamed {total_bytes:,} bytes to {temp_file_path}")
                
                # Read the complete file as bytes
                with open(temp_file_path, 'rb') as f:
                    audio_data = f.read()
                
                # Clean up temporary file
                os.unlink(temp_file_path)
                
                return audio_data
                
        except Exception as e:
            logger.error(f"❌ Sarvam AI Streaming TTS failed: {e}")
            return b""
    
    async def synthesize_stream(self, text: str, language: str = 'hi') -> AsyncGenerator[bytes, None]:
        """Stream TTS audio chunks in real-time"""
        
        if not text or not text.strip():
            logger.warning("Empty text provided")
            return
        
        if not self.api_key:
            logger.error("❌ No API key - cannot synthesize")
            return
        
        # Truncate if too long
        MAX_LENGTH = 5000
        if len(text) > MAX_LENGTH:
            logger.warning(f"Text too long ({len(text)} chars), truncating")
            text = text[:MAX_LENGTH]
        
        try:
            # Language mapping
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
            
            headers = {
                "api-subscription-key": self.api_key,
                "Content-Type": "application/json"
            }
            
            payload = {
                "text": text,
                "target_language_code": lang_code,
                "speaker": self.speaker,
                "model": self.model,
                "pace": self.pace,
                "speech_sample_rate": self.speech_sample_rate,
                "output_audio_codec": self.output_audio_codec,
                "enable_preprocessing": self.enable_preprocessing
            }
            
            logger.info(f"🎤 Starting streaming TTS: '{text[:50]}...'")
            
            with requests.post(self.api_url, headers=headers, json=payload, stream=True) as response:
                response.raise_for_status()
                
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        yield chunk
                        logger.debug(f"Streamed {len(chunk)} bytes")
                        
        except Exception as e:
            logger.error(f"❌ Sarvam AI Streaming TTS failed: {e}")
            return
    
    def get_available_voices(self, language_code: str = 'hi-IN') -> list:
        """Get available voices for Sarvam AI TTS"""
        voices = {
            'hi-IN': ['pooja', 'meera', 'arush', 'anaya'],
            'en-IN': ['pooja', 'meera', 'arush', 'anaya'],
            'bn-IN': ['pooja', 'meera'],
            'ta-IN': ['pooja', 'meera'],
            'te-IN': ['pooja', 'meera'],
            'kn-IN': ['pooja', 'meera'],
            'ml-IN': ['pooja', 'meera'],
            'mr-IN': ['pooja', 'meera'],
            'gu-IN': ['pooja', 'meera'],
            'pa-IN': ['pooja', 'meera'],
            'or-IN': ['pooja', 'meera']
        }
        return voices.get(language_code, ['pooja', 'meera'])
    
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


# Example usage function
def stream_tts_example():
    """Example function showing how to use the streaming TTS"""
    
    API_KEY = "YOUR_API_KEY"  # Replace with actual API key
    API_URL = "https://api.sarvam.ai/text-to-speech/stream"
    
    headers = {
        "api-subscription-key": API_KEY,
        "Content-Type": "application/json"
    }
    
    payload = {
        "text": """Hello! This is a streaming text-to-speech example.""",
        "target_language_code": "hi-IN",
        "speaker": "pooja",
        "model": "bulbul:v3",
        "pace": 1.1,
        "speech_sample_rate": 22050,
        "output_audio_codec": "mp3",
        "enable_preprocessing": True
    }
    
    # Stream the response
    with requests.post(API_URL, headers=headers, json=payload, stream=True) as response:
        response.raise_for_status()
        
        # Save to file as chunks arrive
        with open("output.mp3", "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    print(f"Received {len(chunk)} bytes")
        
        print("Audio saved to output.mp3")


if __name__ == "__main__":
    stream_tts_example()
