from dotenv import load_dotenv
load_dotenv()

import os
import asyncio
import aiohttp
import edge_tts
from gtts import gTTS
import concurrent.futures
import tempfile

# Use cache for repeated text
_tts_cache = {}

def text_to_speech_multilingual_fast(input_text, output_filepath="output.mp3", language="English"):
    """
    Ultra-fast TTS with caching and parallel processing
    """
    if not input_text or len(input_text.strip()) == 0:
        input_text = "Analysis complete."
    
    # Cache check
    cache_key = f"{hash(input_text[:100])}_{language}"
    if cache_key in _tts_cache:
        with open(output_filepath, 'wb') as f:
            f.write(_tts_cache[cache_key])
        return True
    
    try:
        # Language mapping for faster lookup
        language_map = {
            "English": "en",
            "Hindi": "hi", 
            "Marathi": "mr"
        }
        
        lang_code = language_map.get(language, "en")
        
        # Use gTTS directly (fastest option)
        tts = gTTS(
            text=input_text,
            lang=lang_code,
            slow=False,
            lang_check=False
        )
        
        # Save to temp file first
        with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as tmp:
            temp_path = tmp.name
        
        tts.save(temp_path)
        
        # Cache the audio
        with open(temp_path, 'rb') as f:
            audio_data = f.read()
            _tts_cache[cache_key] = audio_data
            with open(output_filepath, 'wb') as out_f:
                out_f.write(audio_data)
        
        # Cleanup
        os.unlink(temp_path)
        
        return True
        
    except Exception as e:
        print(f"Fast TTS error: {str(e)}")
        # Fallback to simple text
        return False

async def text_to_speech_edge_async(input_text, output_filepath="output.mp3", language="English"):
    """
    Alternative: Edge TTS (faster, better voices)
    """
    try:
        voice_map = {
            "English": "en-US-AriaNeural",
            "Hindi": "hi-IN-SwaraNeural",
            "Marathi": "mr-IN-AarohiNeural"
        }
        
        voice = voice_map.get(language, "en-US-AriaNeural")
        communicate = edge_tts.Communicate(input_text, voice)
        
        # Save directly
        await communicate.save(output_filepath)
        return True
    except Exception as e:
        print(f"Edge TTS error: {e}")
        return False

# Main optimized function
def text_to_speech_multilingual(input_text, output_filepath="output.mp3", language="English"):
    """
    Main function with fallbacks
    """
    # Return immediately if text is short
    if len(input_text) < 50:
        return text_to_speech_multilingual_fast(input_text, output_filepath, language)
    
    # For longer text, use async
    try:
        # Try Edge TTS first (faster for longer text)
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        success = loop.run_until_complete(
            text_to_speech_edge_async(input_text, output_filepath, language)
        )
        loop.close()
        
        if success:
            return True
    except:
        pass
    
    # Fallback to fast gTTS
    return text_to_speech_multilingual_fast(input_text, output_filepath, language)