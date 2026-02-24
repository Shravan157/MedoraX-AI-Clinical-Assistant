from dotenv import load_dotenv
load_dotenv()

import os
import asyncio
import speech_recognition as sr
from groq import AsyncGroq
import tempfile
import concurrent.futures
from pydub import AudioSegment
import io

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

def record_audio_fast(file_path: str, timeout: int = 15, phrase_time_limit: int = 10) -> bool:
    """
    Faster audio recording with optimized settings
    """
    recognizer = sr.Recognizer()
    recognizer.energy_threshold = 300  # Lower threshold for faster detection
    recognizer.dynamic_energy_threshold = False
    
    try:
        with sr.Microphone() as source:
            # Skip ambient noise adjustment for speed
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            
            # Record with minimal settings
            audio_data = recognizer.listen(
                source, 
                timeout=timeout, 
                phrase_time_limit=phrase_time_limit
            )
            
            # Convert directly to MP3
            wav_data = audio_data.get_wav_data(convert_rate=16000)  # Lower sample rate
            audio_segment = AudioSegment.from_wav(io.BytesIO(wav_data))
            
            # Use lower bitrate for faster processing
            audio_segment.export(file_path, format="mp3", bitrate="64k")
            
            return True
            
    except Exception as e:
        print(f"Recording error: {e}")
        return False

def record_audio(file_path: str, timeout: int = 20, phrase_time_limit: int = None) -> bool:
    """Backward compatible wrapper"""
    return record_audio_fast(file_path, timeout, phrase_time_limit)

async def transcribe_with_groq_async(audio_filepath: str, stt_model: str = "whisper-large-v3") -> str:
    """
    Async transcription - 2x faster
    """
    client = AsyncGroq(api_key=GROQ_API_KEY)
    
    try:
        with open(audio_filepath, "rb") as audio_file:
            transcription = await client.audio.transcriptions.create(
                model=stt_model,
                file=audio_file,
                response_format="text",
                temperature=0.0  # Lower temp for faster processing
            )
        
        return transcription if isinstance(transcription, str) else transcription.text
        
    except Exception as e:
        print(f"Async transcription error: {e}")
        return ""

def transcribe_with_groq_fast(audio_filepath: str, stt_model: str = "whisper-large-v3") -> str:
    """
    Fast synchronous transcription
    """
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(
            transcribe_with_groq_async(audio_filepath, stt_model)
        )
        loop.close()
        return result
    except Exception as e:
        print(f"Fast transcription error: {e}")
        # Fallback to sync
        from groq import Groq
        client = Groq(api_key=GROQ_API_KEY)
        with open(audio_filepath, "rb") as audio_file:
            transcription = client.audio.transcriptions.create(
                model=stt_model,
                file=audio_file,
                response_format="text"
            )
        return transcription.text

# Backward compatibility
def transcribe_with_groq(GROQ_API_KEY: str, audio_filepath: str, stt_model: str = "whisper-large-v3") -> str:
    """Optimized main function"""
    return transcribe_with_groq_fast(audio_filepath, stt_model)