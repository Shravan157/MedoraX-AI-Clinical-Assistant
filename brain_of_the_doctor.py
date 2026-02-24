
from dotenv import load_dotenv
load_dotenv()

import os
import base64
import asyncio
from groq import AsyncGroq
import aiohttp
from typing import Optional
import concurrent.futures
from PIL import Image
import io

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

# Cache for encoded images
_image_cache = {}

def encode_image_fast(image_path: str, max_size: int = 1024) -> str:
    """
    Optimized image encoding with resizing
    """
    cache_key = f"{image_path}_{max_size}"
    if cache_key in _image_cache:
        return _image_cache[cache_key]
    
    try:
        # Open and resize image if too large
        with Image.open(image_path) as img:
            # Convert to RGB if necessary
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Resize if image is too large
            if max(img.size) > max_size:
                ratio = max_size / max(img.size)
                new_size = tuple(int(dim * ratio) for dim in img.size)
                img = img.resize(new_size, Image.Resampling.LANCZOS)
            
            # Save to bytes
            buffer = io.BytesIO()
            img.save(buffer, format='JPEG', quality=85, optimize=True)
            buffer.seek(0)
            encoded = base64.b64encode(buffer.read()).decode('utf-8')
            
            # Cache result
            _image_cache[cache_key] = encoded
            return encoded
            
    except Exception as e:
        print(f"Image encoding error: {e}")
        # Fallback to original encoding
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

def encode_image(image_path: str) -> str:
    """Backward compatible wrapper"""
    return encode_image_fast(image_path)

async def analyze_image_async(query: str, model: str, encoded_image: str) -> str:
    """
    Async image analysis - 2-3x faster
    """
    client = AsyncGroq(api_key=GROQ_API_KEY)
    
    messages = [{
        "role": "user",
        "content": [
            {"type": "text", "text": query},
            {
                "type": "image_url",
                "image_url": {"url": f"data:image/jpeg;base64,{encoded_image}"}
            }
        ]
    }]
    
    try:
        # Set timeout and faster processing
        chat_completion = await client.chat.completions.create(
            messages=messages,
            model=model,
            temperature=0.1,  # Lower temp for faster response
            max_tokens=1024,   # Increased for treatment suggestions
            timeout=30.0      # Timeout
        )
        
        return chat_completion.choices[0].message.content
        
    except Exception as e:
        print(f"Async analysis error: {e}")
        return f"Analysis error: {str(e)}"

async def get_treatment_suggestions_async(condition_description: str, patient_history: str = "", language: str = "English") -> str:
    """
    Get treatment and medicine suggestions for diagnosed condition
    """
    client = AsyncGroq(api_key=GROQ_API_KEY)
    
    lang_instruction = f"Respond in {language} language." if language != "English" else ""
    
    prompt = f"""As a medical AI assistant, provide treatment suggestions based on this condition. {lang_instruction}

Condition Description: {condition_description}
{patient_history}

Please provide:

1. **Recommended Medical Treatment**:
   - Primary treatment approach
   - Specialist referral needed (if any)
   - Diagnostic tests recommended

2. **Medication Suggestions**:
   - Common medications (with generic names)
   - Typical dosages (general guidance only)
   - Important precautions and contraindications

3. **Lifestyle & Home Care**:
   - Self-care recommendations
   - Activity modifications
   - Dietary suggestions

4. **When to Seek Immediate Care**:
   - Red flag symptoms
   - Emergency warning signs

IMPORTANT: 
- Always mention "CONSULT A DOCTOR before taking any medication"
- Specify that dosages should be determined by a healthcare professional
- Include OTC options only when appropriate
- Mention potential side effects"""

    messages = [{
        "role": "user",
        "content": prompt
    }]
    
    try:
        chat_completion = await client.chat.completions.create(
            messages=messages,
            model="llama-3.3-70b-versatile",
            temperature=0.2,
            max_tokens=1024,
            timeout=30.0
        )
        
        return chat_completion.choices[0].message.content
        
    except Exception as e:
        print(f"Treatment suggestions error: {e}")
        return f"Unable to generate treatment suggestions. Please consult a doctor."

def analyze_image_with_query_sync(query: str, model: str, encoded_image: str) -> str:
    """
    Synchronous wrapper for async function
    """
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(
            analyze_image_async(query, model, encoded_image)
        )
        loop.close()
        return result
    except Exception as e:
        print(f"Sync analysis error: {e}")
        # Fallback to sync
        from groq import Groq
        client = Groq(api_key=GROQ_API_KEY)
        messages = [{
            "role": "user",
            "content": [
                {"type": "text", "text": query},
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{encoded_image}"}
                }
            ]
        }]
        
        chat_completion = client.chat.completions.create(
            messages=messages,
            model=model,
            temperature=0.1,
            max_tokens=1024
        )
        
        return chat_completion.choices[0].message.content

def get_treatment_suggestions_sync(condition_description: str, patient_history: str = "", language: str = "English") -> str:
    """
    Synchronous wrapper for treatment suggestions
    """
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(
            get_treatment_suggestions_async(condition_description, patient_history, language)
        )
        loop.close()
        return result
    except Exception as e:
        print(f"Sync treatment suggestions error: {e}")
        return "Please consult a doctor for treatment recommendations."

# Backward compatibility
def analyze_image_with_query(query: str, encoded_image: str, model: str = "meta-llama/llama-4-scout-17b-16e-instruct") -> str:
    """Optimized main function"""
    return analyze_image_with_query_sync(query, model, encoded_image)