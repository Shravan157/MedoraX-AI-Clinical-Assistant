import os
import gradio as gr
import re
from groq import Groq
from dotenv import load_dotenv

# Import isolated nearby care service
from nearby_care import find_hospitals_nearby

# Load environment variables
load_dotenv()

from brain_of_the_doctor import encode_image, analyze_image_with_query, get_treatment_suggestions_sync
from voice_of_the_patient import record_audio, transcribe_with_groq
from voice_of_the_doctor import text_to_speech_multilingual
import base64

def get_base64_logo(image_path="logo.png"):
    try:
        if os.path.exists(image_path):
            with open(image_path, "rb") as f:
                return f"data:image/png;base64,{base64.b64encode(f.read()).decode()}"
        return ""
    except Exception:
        return ""

LOGO_BASE64 = get_base64_logo()

# --- Configuration ---
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
GOOGLE_MAPS_API_KEY = os.environ.get("GOOGLE_MAPS_API_KEY")
client = Groq(api_key=GROQ_API_KEY)

print(f"Starting MedoraX with Google Maps API...")
print(f"API Key (first 10 chars): {GOOGLE_MAPS_API_KEY[:10]}...")

# --- Translations ---
TRANSLATIONS = {
    "English": {
        "title": "MEDORAX",
        "chat_tab": "SMART CONSULT",
        "diag_tab": "AI DIAGNOSTICS",
        "map_tab": "NEARBY CARE",
        "about_tab": "ABOUT SYSTEM",
        "welcome": "Advanced <span style='background: linear-gradient(135deg, #fff 0%, #888 50%, #444 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>Clinical Intelligence</span>",
        "sub_welcome": "Professional-grade medical analysis with multimodal AI capabilities.",
        "chat_placeholder": "How can I help you today?",
        "ask_btn": "Ask MedoraX",
        "emergency_btn": "🚨 Find Nearby Hospitals",
        "upload_title": "📸 Clinical Analysis",
        "upload_sub": "Upload medical image and describe symptoms via voice or text.",
        "analyze_btn": "Analyze with AI",
        "get_treatment_btn": "💊 Get Treatment Suggestions",
        "analysis_report": "🔬 Diagnostic Report",
        "transcription_label": "Patient Description",
        "insight_label": "Medical Assessment",
        "treatment_label": "💊 Treatment & Medication Suggestions",
        "voice_summary": "Audio Summary",
        "disclaimer": "Disclaimer: MedoraX is an AI diagnostic assistant, not a licensed physician. Always consult healthcare professionals.",
        "map_title": "Local Healthcare Facilities",
        "map_desc": "Find nearby hospitals using Google Maps.",
        "find_best_btn": "📍 Get My Location",
        "fetching_msg": "🔍 Searching hospitals...",
        "text_input_label": "Text Description (if no voice)",
        "text_input_placeholder": "Describe your symptoms here...",
        "voice_tab": "🎤 Voice Input",
        "text_tab": "📝 Text Input",
        "treatment_disclaimer": "⚠️ IMPORTANT: Always consult a doctor before taking any medication. Dosages should be determined by healthcare professionals.",
        "no_treatment": "Please get a diagnosis first to receive treatment suggestions.",
        "no_image": "I need a medical image for proper diagnosis."
    },
    "Hindi": {
        "title": "मेडोराX",
        "chat_tab": "स्मार्ट चैट",
        "diag_tab": "एआई निदान",
        "map_tab": "पास के अस्पताल",
        "about_tab": "जानकारी",
        "welcome": "उन्नत एआई चिकित्सा निदान",
        "sub_welcome": "बहु-मोडल एआई क्षमताओं के साथ पेशेवर-ग्रेड चिकित्सा विश्लेषण।",
        "chat_placeholder": "मैं आज आपकी कैसे मदद कर सकता हूँ?",
        "ask_btn": "मेडोराX से पूछें",
        "emergency_btn": "🚨 पास के अस्पताल खोजें",
        "upload_title": "📸 क्लिनिकल विश्लेषण",
        "upload_sub": "चिकित्सा छवि अपलोड करें और आवाज या पाठ के माध्यम से लक्षणों का वर्णन करें।",
        "analyze_btn": "एआई के साथ विश्लेषण करें",
        "get_treatment_btn": "💊 उपचार सुझाव प्राप्त करें",
        "analysis_report": "🔬 निदान रिपोर्ट",
        "transcription_label": "रोगी विवरण",
        "insight_label": "चिकित्सा मूल्यांकन",
        "treatment_label": "💊 उपचार और दवा सुझाव",
        "voice_summary": "ध्वनी सारांश",
        "disclaimer": "अस्वीकरण: मेडोराX एक एआई निदान सहायक है, लाइसेंस प्राप्त चिकित्सक नहीं। हमेशा स्वास्थ्य पेशेवरों से परामर्श करें।",
        "map_title": "स्थानीय स्वास्थ्य सुविधाएं",
        "map_desc": "Google मानचित्र का उपयोग करके पास के अस्पताल खोजें।",
        "find_best_btn": "📍 मेरा स्थान प्राप्त करें",
        "fetching_msg": "🔍 अस्पताल खोज रहे हैं...",
        "text_input_label": "पाठ विवरण (यदि आवाज नहीं)",
        "text_input_placeholder": "अपने लक्षणों का वर्णन यहां करें...",
        "voice_tab": "🎤 आवाज इनपुट",
        "text_tab": "📝 पाठ इनपुट",
        "treatment_disclaimer": "⚠️ महत्वपूर्ण: किसी भी दवा लेने से पहले हमेशा डॉक्टर से परामर्श करें। खुराक स्वास्थ्य पेशेवरों द्वारा निर्धारित की जानी चाहिए।",
        "no_treatment": "उपचार सुझाव प्राप्त करने के लिए कृपया पहले निदान प्राप्त करें।",
        "no_image": "मुझे उचित निदान के लिए एक चिकित्सा छवि की आवश्यकता है।"
    },
    "Marathi": {
        "title": "मेडोराX",
        "chat_tab": "स्मार्ट चॅट",
        "diag_tab": "एआय निदान",
        "map_tab": "जवळची रुग्णालये",
        "about_tab": "माहिती",
        "welcome": "प्रगत एआय वैद्यकीय निदान",
        "sub_welcome": "बहु-मोडल एआय क्षमतांसह व्यावसायिक-ग्रेड वैद्यकीय विश्लेषण।",
        "chat_placeholder": "मी तुम्हाला आज कशी मदत करू शकतो?",
        "ask_btn": "मेडोराX ला विचारा",
        "emergency_btn": "🚨 जवळची रुग्णालये शोधा",
        "upload_title": "📸 क्लिनिकल विश्लेषण",
        "upload_sub": "वैद्यकीय प्रतिमा अपलोड करा आणि आवाज किंवा मजकूराद्वारे लक्षणांचे वर्णन करा।",
        "analyze_btn": "एआय सह विश्लेषण करा",
        "get_treatment_btn": "💊 उपचार सूचना मिळवा",
        "analysis_report": "🔬 निदान अहवाल",
        "transcription_label": "रुग्ण वर्णन",
        "insight_label": "वैद्यकीय मूल्यांकन",
        "treatment_label": "💊 उपचार आणि औषध सूचना",
        "voice_summary": "ध्वनी सारांश",
        "disclaimer": "डिस्क्लेमर: मेडोराX हा एआय निदान सहाय्यक आहे, डॉक्टर नाही। नेहमी वैद्यकीय व्यावसायिकांचा सल्ला घ्या।",
        "map_title": "स्थानिक आरोग्य सुविधा",
        "map_desc": "Google Maps वापरून जवळची रुग्णालये शोधा।",
        "find_best_btn": "📍 माझे स्थान मिळवा",
        "fetching_msg": "🔍 रुग्णालये शोधत आहे...",
        "text_input_label": "मजकूर वर्णन (जर आवाज नसेल तर)",
        "text_input_placeholder": "तुमची लक्षणे येथे वर्णन करा...",
        "voice_tab": "🎤 आवाज इनपुट",
        "text_tab": "📝 मजकूर इनपुट",
        "treatment_disclaimer": "⚠️ महत्वाचे: कोणतेही औषध घेण्यापूर्वी नेहमी डॉक्टरांचा सल्ला घ्या। खुराक वैद्यकीय व्यावसायिकांद्वारे निश्चित केली पाहिजे।",
        "no_treatment": "कृपया उपचार सूचना मिळवण्यासाठी प्रथम निदान मिळवा।",
        "no_image": "मला योग्य निदानासाठी वैद्यकीय प्रतिमा आवश्यक आहे।"
    }
}

def groq_chat(message, history, language):
    """
    Chat with Groq (Llama-3.3-70b) with Medical Persona - Enhanced for treatment suggestions
    """
    if not message:
        return history + [{"role": "assistant", "content": ""}], ""
    
    lang_map = {
        "Hindi": "Respond primarily in Hindi (हिंदी). Use Devnagari script.",
        "Marathi": "Respond primarily in Marathi (मराठी). Use Devnagari script.",
        "English": "Respond in English."
    }
    lang_instruction = lang_map.get(language, "Respond in English.")
    
    # Check if user is asking for treatment/medicine suggestions
    treatment_keywords = ["medicine", "medication", "drug", "treatment", "prescription", "tablet", "capsule", 
                         "dose", "dosage", "what to take", "how to treat", "remedy", "cure", "therapy"]
    
    is_treatment_query = any(keyword in message.lower() for keyword in treatment_keywords)
    
    if is_treatment_query:
        system_instruction = (
            f"You are MedoraX, a professional AI medical assistant specialized in clinical pharmacology. "
            f"{lang_instruction} Provide precise, evidence-based treatment and medication suggestions (Standard Treatment Guidelines). "
            f"IMPORTANT: Always include these points:\n"
            f"1. **MANDATORY DISCLAIMER**: State 'CONSULT A DOCTOR for precise dosage and diagnosis' at the start.\n"
            f"2. **Specific Medicines**: Recommend exact GENERIC medicine names (e.g., 'Paracetamol 500mg', 'Cetirizine 10mg') instead of vague classes.\n"
            f"3. **Dosage**: Mention standard adult dosages but emphasize they vary by patient.\n"
            f"4. **Brand Names**: You may mention common brand names in parentheses for clarity (e.g., 'Ibuprofen (Advil/Brufen)').\n"
            f"5. **Red Flags**: Clearly list symptoms that require immediate ER visits.\n"
            f"6. **Home Care**: Suggest supportive care (hydration, rest) alongside medication.\n"
            f"7. **Safety**: Mention contraindications (e.g., 'Avoid if you have liver issues')."
        )
    else:
        system_instruction = (
            f"You are MedoraX, a professional AI medical assistant. "
            f"{lang_instruction} Provide concise, evidence-based medical advice. "
            f"Maintain a calm, reassuring tone. "
            f"CRITICAL: Always advise seeing a doctor for serious symptoms."
        )

    try:
        messages = [{"role": "system", "content": system_instruction}]
        for h in history:
            messages.append({"role": h["role"], "content": h["content"]})
        
        messages.append({"role": "user", "content": message})
        
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            temperature=0.4,
            max_tokens=1024,
        )
        history.append({"role": "user", "content": message})
        history.append({"role": "assistant", "content": response.choices[0].message.content})
        return history, ""
    except Exception as e:
        print(f"Chat Error: {e}")
        history.append({"role": "user", "content": message})
        history.append({"role": "assistant", "content": f"Error: {str(e)}"})
        return history, ""

def process_inputs(audio_filepath, image_filepath, text_description, language):
    """
    Process audio, text and image inputs for AI diagnosis with language support
    """
    # Get language instruction based on selected language
    if language == "Hindi":
        lang_instruction = "कृपया हिंदी में उत्तर दें। देवनागरी लिपि का प्रयोग करें।"
        lang_name = "हिंदी"
    elif language == "Marathi":
        lang_instruction = "कृपया मराठी में उत्तर दें। देवनागरी लिपि का प्रयोग करें।"
        lang_name = "मराठी"
    else:  # English
        lang_instruction = "Please respond in English."
        lang_name = "English"
    
    # Create system prompt with language instruction
    system_prompt = f"""{lang_instruction}

You are MedoraX, a professional medical diagnostician. 

Analyze the provided medical image and describe any visible conditions or concerns. 
Provide:
1. Possible diagnosis based on visual evidence
2. Confidence level of assessment
3. Recommended next steps
4. Red flag symptoms to watch for

CRITICAL: All responses must be in {lang_name} language."""

    if not audio_filepath and not image_filepath and not text_description:
        no_input_msg = TRANSLATIONS.get(language, TRANSLATIONS["English"])["no_treatment"]
        return no_input_msg, no_input_msg, None, ""

    patient_description = ""
    
    # Get patient description from audio or text
    if audio_filepath:
        try:
            patient_description = transcribe_with_groq(
                GROQ_API_KEY=GROQ_API_KEY, 
                audio_filepath=audio_filepath,
                stt_model="whisper-large-v3"
            )
        except Exception as e:
            print(f"Transcription error: {e}")
            patient_description = "Transcription failed."
    elif text_description:
        patient_description = text_description
    
    doctor_response = ""
    treatment_response = ""
    
    if image_filepath:
        # Create a comprehensive query with language instruction
        if language == "Hindi":
            query_suffix = "छवि और रोगी के विवरण के आधार पर अपना व्यापक चिकित्सा विश्लेषण प्रदान करें:"
        elif language == "Marathi":
            query_suffix = "प्रतिमा आणि रुग्णाच्या वर्णनाच्या आधारे आपले सर्वसमावेशक वैद्यकीय विश्लेषण प्रदान करा:"
        else:  # English
            query_suffix = "Based on the image and the patient's description above, provide your comprehensive medical analysis:"
        
        query_text = f"""{system_prompt}

रोगी का विवरण / Patient's Description: {patient_description if patient_description else "कोई विवरण प्रदान नहीं किया गया / No description provided."}

{query_suffix}"""
        
        try:
            encoded_image = encode_image(image_filepath)
            
            # Add language instruction explicitly at the beginning of the query
            final_query = f"{lang_instruction}\n\n{query_text}"
            
            doctor_response = analyze_image_with_query(
                query=final_query, 
                encoded_image=encoded_image, 
                model="meta-llama/llama-4-scout-17b-16e-instruct"
            ) 
            
            # Automatically generate treatment suggestions if diagnosis is made
            if doctor_response and "no diagnosis" not in doctor_response.lower() and "unable" not in doctor_response.lower():
                treatment_response = get_treatment_suggestions_sync(
                    condition_description=doctor_response[:500],  # First 500 chars of diagnosis
                    patient_history=patient_description[:200] if patient_description else "",
                    language=language
                )
                
        except Exception as e:
            error_msg = f"Analysis Error: {str(e)}"
            doctor_response = error_msg
    else:
        doctor_response = TRANSLATIONS.get(language, TRANSLATIONS["English"])["no_image"]

    # Generate audio output using gTTS
    output_audio_path = "final.mp3"
    cleaned_response = re.sub(r'[*#_`~]', '', doctor_response) if doctor_response else ""
    
    try:
        # Use the multilingual gTTS function
        text_to_speech_multilingual(
            input_text=cleaned_response[:2000],  # Increased limit for audio summary
            output_filepath=output_audio_path,
            language=language
        )
    except Exception as e:
        print(f"Audio generation error: {e}")
        # Fallback to English
        text_to_speech_multilingual(
            input_text="Analysis complete. Please read the text report.",
            output_filepath=output_audio_path,
            language="English"
        )
    
    return patient_description, doctor_response, output_audio_path, treatment_response

def get_treatment_suggestions_for_diagnosis(diagnosis_text, patient_history, language):
    """
    Generate treatment suggestions based on diagnosis
    """
    if not diagnosis_text or diagnosis_text in ["No input.", TRANSLATIONS.get(language, TRANSLATIONS["English"])["no_image"]]:
        return TRANSLATIONS.get(language, TRANSLATIONS["English"])["no_treatment"]
    
    try:
        treatment_response = get_treatment_suggestions_sync(
            condition_description=diagnosis_text,
            patient_history=patient_history[:200] if patient_history else "",
            language=language
        )
        
        # Add disclaimer in appropriate language
        disclaimer = TRANSLATIONS.get(language, TRANSLATIONS["English"])["treatment_disclaimer"]
        return f"{treatment_response}\n\n{disclaimer}"
        
    except Exception as e:
        print(f"Treatment generation error: {e}")
        return f"Error generating treatment suggestions: {str(e)}"

# --- Updated UI CSS with Gray Theme matching screenshot ---
custom_css = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Outfit:wght@300;400;500;600;700;800&family=Roboto+Mono:wght@400;500&display=swap');

:root { 
    --primary: #3a86ff;  /* Blue accent from screenshot */
    --primary-dark: #2667cc; 
    --primary-light: #6ca3ff;
    --secondary: #6c757d;
    --accent: #ff6b6b;
    --danger: #dc3545;
    --bg-dark: #1a1d27;  /* Dark blue-gray background */
    --bg-card: #252836;   /* Card background - darker gray */
    --card-bg: #2d3041;
    --text-primary: #f8f9fa;
    --text-secondary: #adb5bd;
    --text-muted: #6c757d;
    --border: #3a3f50;    /* Subtle border color */
    --border-light: #4a4f60;
    --shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    --glass: rgba(37, 40, 54, 0.9);
    --success: #28a745;
    --warning: #ffc107;
    --logo-main: #ffffff;
    --logo-accent: #3a86ff;
}

.text-logo {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    line-height: 1;
    font-family: 'Outfit', sans-serif;
}

.logo-main {
    font-size: 2.2rem;
    font-weight: 900;
    letter-spacing: -1px;
    margin-bottom: 4px;
}

.logo-medora {
    color: #ffffff;
    background: linear-gradient(135deg, #ffffff 0%, #a5b4fc 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.logo-x {
    color: #3a86ff;
}

.logo-sub {
    font-size: 0.85rem;
    font-weight: 500;
    letter-spacing: 2px;
    color: #8b9dc3;
    text-transform: uppercase;
}

.logo-header .logo-main { font-size: 1.8rem; }
.logo-header .logo-sub { font-size: 0.7rem; letter-spacing: 1.5px; }

.logo-welcome .logo-main { font-size: 3.5rem; }
.logo-welcome .logo-sub { font-size: 1.1rem; letter-spacing: 3px; }

* {
    font-family: 'Outfit', 'Inter', sans-serif !important;
}

body, .gradio-container { 
    background: linear-gradient(135deg, #1a1d27 0%, #252836 100%) !important;
    color: var(--text-primary) !important;
    min-height: 100vh;
    margin: 0;
    padding: 0;
}

/* Main container fixes */
#main-container {
    width: 100vw !important;
    max-width: 100% !important;
    margin: 0 !important;
    padding: 0 !important;
    background: transparent !important;
}

/* Sidebar adjustments */
.sidebar {
    background: rgba(26, 29, 39, 0.95) !important;
    backdrop-filter: blur(10px);
    border-right: 1px solid rgba(58, 63, 80, 0.5);
    height: 100vh;
    padding: 30px 15px;
    display: flex;
    flex-direction: column;
    gap: 15px;
    width: 240px !important;
    min-width: 240px !important;
    max-width: 240px !important;
    position: fixed !important;
    left: 0;
    top: 0;
    z-index: 1000;
    box-shadow: 4px 0 20px rgba(0, 0, 0, 0.2);
}

/* Main content area fixes */
.content-area {
    padding: 30px !important;
    margin-left: 240px !important;
    width: calc(100% - 240px) !important;
    min-height: 100vh;
    background: transparent !important;
    overflow-y: auto;
}

.matte-panel { 
    background: linear-gradient(145deg, #2d3041 0%, #252836 100%) !important;
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 25px;
    box-shadow: var(--shadow);
    margin-bottom: 20px;
    transition: all 0.3s ease;
}

.matte-panel:hover {
    border-color: var(--primary-light);
    box-shadow: 0 12px 40px rgba(0, 0, 0, 0.4);
    transform: translateY(-2px);
}

.medical-card {
    background: linear-gradient(145deg, #2d3041 0%, #252836 100%) !important;
    border-left: 4px solid var(--primary);
    border-radius: 12px;
    transition: all 0.3s ease;
    padding: 20px;
}

.medical-card:hover {
    transform: translateY(-4px);
    background: linear-gradient(145deg, #333647 0%, #2a2d3e 100%) !important;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
}

.primary-btn { 
    background: linear-gradient(135deg, #3a86ff 0%, #2667cc 100%) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 12px !important;
    font-weight: 600 !important;
    padding: 14px 28px !important;
    font-size: 14px !important;
    text-transform: uppercase;
    letter-spacing: 1px;
    box-shadow: 0 4px 15px rgba(58, 134, 255, 0.3) !important;
    transition: all 0.3s ease !important;
}

.primary-btn:hover {
    background: linear-gradient(135deg, #4a96ff 0%, #3677dd 100%) !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(58, 134, 255, 0.4) !important;
}

.secondary-btn {
    background: rgba(255, 255, 255, 0.1) !important;
    color: white !important;
    border: 1px solid rgba(255, 255, 255, 0.2) !important;
    border-radius: 12px !important;
    font-weight: 600 !important;
}

.treatment-btn {
    background: linear-gradient(135deg, #2d3041 0%, #3a3f50 100%) !important;
    border: 1px solid rgba(58, 134, 255, 0.3) !important;
    color: #ffffff !important;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2) !important;
}

.treatment-btn:hover {
    background: linear-gradient(135deg, #3a3f50 0%, #4a4f60 100%) !important;
    border-color: var(--primary) !important;
    color: white !important;
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3) !important;
}

.chatbot {
    border-radius: 16px !important;
    border: 1px solid var(--border) !important;
    background: linear-gradient(145deg, #2d3041 0%, #252836 100%) !important;
    height: 500px !important;
}

.tabs {
    border-bottom: 2px solid rgba(58, 63, 80, 0.5) !important;
}

.tab-nav button {
    font-size: 15px !important;
    font-weight: 500 !important;
    color: var(--text-muted) !important;
    padding: 10px 20px !important;
    background: transparent !important;
    border: none !important;
}

.tab-nav button.selected {
    color: var(--primary-light) !important;
    border-bottom: 3px solid var(--primary) !important;
    background: rgba(58, 134, 255, 0.1) !important;
}

.header-gradient {
    color: #ffffff;
    background: linear-gradient(135deg, #ffffff 0%, #a5b4fc 50%, #3a86ff 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    display: inline-block;
}

.logo-float {
    animation: float 6s ease-in-out infinite;
}

@keyframes float {
    0% { transform: translateY(0px); }
    50% { transform: translateY(-10px); }
    100% { transform: translateY(0px); }
}

.pulse-red {
    animation: pulse-red 2s infinite;
}

@keyframes pulse-red {
    0% { box-shadow: 0 0 0 0 rgba(220, 53, 69, 0.4); }
    70% { box-shadow: 0 0 0 12px rgba(220, 53, 69, 0); }
    100% { box-shadow: 0 0 0 0 rgba(220, 53, 69, 0); }
}

.nav-btn {
    text-align: left !important;
    justify-content: flex-start !important;
    background: transparent !important;
    border: 1px solid transparent !important;
    color: var(--text-muted) !important;
    font-size: 15px !important;
    padding: 14px 18px !important;
    border-radius: 12px !important;
    transition: all 0.3s ease !important;
    margin: 4px 0 !important;
}

.nav-btn:hover {
    background: rgba(255, 255, 255, 0.05) !important;
    color: var(--text-primary) !important;
    border-color: rgba(255, 255, 255, 0.1) !important;
    transform: translateX(4px) !important;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2) !important;
}

.nav-btn-active, .nav-btn-active:hover {
    background: linear-gradient(135deg, rgba(58, 134, 255, 0.2) 0%, rgba(38, 103, 204, 0.2) 100%) !important;
    color: #ffffff !important;
    border: 1px solid rgba(58, 134, 255, 0.3) !important;
    box-shadow: 0 4px 12px rgba(58, 134, 255, 0.2) !important;
}

/* Form elements */
input, textarea, select {
    background: rgba(45, 48, 65, 0.8) !important;
    border: 1px solid #3a3f50 !important;
    color: #f8f9fa !important;
    border-radius: 12px !important;
    padding: 12px 16px !important;
}

input:focus, textarea:focus, select:focus {
    border-color: #3a86ff !important;
    box-shadow: 0 0 0 3px rgba(58, 134, 255, 0.2) !important;
    outline: none !important;
}

/* Fix for tab content alignment */
.gr-tab-item {
    padding: 0 !important;
    margin: 0 !important;
}

/* Responsive adjustments */
@media (max-width: 768px) {
    .sidebar {
        width: 200px !important;
        min-width: 200px !important;
        max-width: 200px !important;
        padding: 20px 10px;
    }
    
    .content-area {
        margin-left: 200px !important;
        width: calc(100% - 200px) !important;
        padding: 20px !important;
    }
}

/* Scrollbar styling */
::-webkit-scrollbar {
    width: 8px;
    height: 8px;
}

::-webkit-scrollbar-track {
    background: rgba(45, 48, 65, 0.5);
    border-radius: 4px;
}

::-webkit-scrollbar-thumb {
    background: #3a3f50;
    border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
    background: #4a4f60;
}

.warning-box {
    background: rgba(245, 158, 11, 0.1) !important;
    border: 1px solid rgba(245, 158, 11, 0.3) !important;
    border-radius: 12px !important;
    padding: 15px !important;
    margin-top: 20px !important;
}

.diagnosis-report, .treatment-report {
    background: rgba(45, 48, 65, 0.8) !important;
    border: 1px solid rgba(58, 63, 80, 0.5) !important;
    border-radius: 12px !important;
}

.chat-input {
    background: rgba(45, 48, 65, 0.8) !important;
    border: 1px solid rgba(58, 63, 80, 0.5) !important;
    border-radius: 12px !important;
}

/* SVG Icon Styles for Buttons */
.nav-btn {
    padding-left: 44px !important; /* Space for icon */
    background-position: 12px center !important;
    background-repeat: no-repeat !important;
    background-size: 20px 20px !important;
}

.icon-chat {
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='%23adb5bd' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z'%3E%3C/path%3E%3C/svg%3E") !important;
}
.icon-diag {
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='%23adb5bd' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M22 12h-4l-3 9L9 3l-3 9H2'/%3E%3C/svg%3E") !important;
}
.icon-map {
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='%23adb5bd' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z'%3E%3C/path%3E%3Ccircle cx='12' cy='10' r='3'%3E%3C/circle%3E%3C/svg%3E") !important;
}
.icon-about {
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='%23adb5bd' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Ccircle cx='12' cy='12' r='10'%3E%3C/circle%3E%3Cline x1='12' y1='16' x2='12' y2='12'%3E%3C/line%3E%3Cline x1='12' y1='8' x2='12.01' y2='8'%3E%3C/line%3E%3C/svg%3E") !important;
}

/* Active State Icons */
.nav-btn-active.icon-chat {
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='%233a86ff' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z'%3E%3C/path%3E%3C/svg%3E") !important;
}
.nav-btn-active.icon-diag {
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='%233a86ff' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M22 12h-4l-3 9L9 3l-3 9H2'/%3E%3C/svg%3E") !important;
}
.nav-btn-active.icon-map {
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='%233a86ff' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z'%3E%3C/path%3E%3Ccircle cx='12' cy='10' r='3'%3E%3C/circle%3E%3C/svg%3E") !important;
}
.nav-btn-active.icon-about {
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='%233a86ff' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Ccircle cx='12' cy='12' r='10'%3E%3C/circle%3E%3Cline x1='12' y1='16' x2='12' y2='12'%3E%3C/line%3E%3Cline x1='12' y1='8' x2='12.01' y2='8'%3E%3C/line%3E%3C/svg%3E") !important;
}
"""

# --- App Layout ---

with gr.Blocks(css=custom_css, title="MedoraX - AI Medical Diagnostics") as demo:
    # Hidden inputs for location (accessible globally)
    lat_input = gr.Textbox(visible=False)
    lon_input = gr.Textbox(visible=False)
    
    with gr.Row(elem_id="main-container"):
        # Sidebar Navigation - Fixed width
        with gr.Column(scale=1, elem_classes="sidebar"):
            header_title = gr.HTML(f"""
                <div style='margin-bottom: 40px;'>
                    <div class='text-logo logo-header'>
                        <div class='logo-main'><span class='logo-medora'>MEDORA</span><span class='logo-x'>-X</span></div>
                        <div class='logo-sub'>AI Health Assistant</div>
                    </div>
                </div>
            """)
            
            nav_chat = gr.Button("SMART CONSULT", elem_classes="nav-btn nav-btn-active icon-chat")
            nav_diag = gr.Button("AI DIAGNOSTICS", elem_classes="nav-btn icon-diag")
            nav_map = gr.Button("NEARBY CARE", elem_classes="nav-btn icon-map")
            nav_about = gr.Button("ABOUT SYSTEM", elem_classes="nav-btn icon-about")
            
            gr.Markdown("---", elem_classes="divider")
            
            lang_dropdown = gr.Dropdown(
                choices=["English", "Hindi", "Marathi"], 
                value="English", 
                label="Language", 
                container=False,
                elem_classes="dropdown"
            )
            
            gr.Markdown("---", elem_classes="divider")
            
            footer_disclaimer = gr.HTML("""
                <div style='text-align: center; padding: 15px 5px; color: #8b9dc3; font-size: 0.75rem;'>
                    <p style='margin: 0;'>© 2026 MedoraX</p>
                    <p style='margin: 4px 0 0 0; font-size: 0.7rem;'>AI Medical Assistant</p>
                </div>
            """)

        # Main Content Area - Adjusted for sidebar
        with gr.Column(scale=4, elem_classes="content-area"):
            # TAB 1: SMART CHAT
            with gr.Column(visible=True) as chat_view:
                welcome_box = gr.HTML(f"""
                    <div style='text-align: center; padding: 40px 20px; max-width: 900px; margin: 0 auto;'>
                        <div class='text-logo logo-welcome' style='margin-bottom: 30px;'>
                            <div class='logo-main'><span class='logo-medora'>MEDORA</span><span class='logo-x'>-X</span></div>
                            <div class='logo-sub'>AI Health Assistant</div>
                        </div>
                        <h1 style='font-size: 3.2rem; font-weight: 800; margin-bottom: 20px; color: #ffffff; line-height: 1.1;'>
                            <span class='header-gradient'>Advanced Clinical Intelligence</span>
                        </h1>
                        <p style='font-size: 1.1rem; color: #adb5bd; line-height: 1.6; margin-bottom: 30px;'>
                            Your intelligent gateway to advanced clinical diagnostics. MedoraX combines state-of-the-art 
                            vision models with medical reasoning to provide instant clinical insights.
                        </p>
                        <div style='display: flex; justify-content: center; gap: 12px; margin-top: 20px; flex-wrap: wrap;'>
                            <div style='background: linear-gradient(135deg, #2d3041 0%, #3a3f50 100%); padding: 12px 20px; border-radius: 12px; border: 1px solid #3a3f50; font-size: 0.9rem; color: #f8f9fa; display: flex; align-items: center; gap: 8px;'>
                                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2v20M2 12h20"/></svg> MULTIMODAL AI
                            </div>
                            <div style='background: linear-gradient(135deg, #2d3041 0%, #3a3f50 100%); padding: 12px 20px; border-radius: 12px; border: 1px solid #3a3f50; font-size: 0.9rem; color: #f8f9fa; display: flex; align-items: center; gap: 8px;'>
                                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4.5 16.5c-1.5 1.26-2 5-2 5s3.74-.5 5-2c.71-.84.7-2.13-.09-2.91a2.18 2.18 0 0 0-2.91-.09z"/><path d="m12 15-3-3a22 22 0 0 1 2-3.95A12.88 12.88 0 0 1 22 2c0 2.72-.78 7.5-6 11a22.35 22.35 0 0 1-4 2z"/><path d="M9 12H4s.55-3.03 2-4c1.62-1.08 5 0 5 0"/><path d="M12 15v5s3.03-.55 4-2c1.08-1.62 0-5 0-5"/></svg> LOGICAL REASONING
                            </div>
                            <div style='background: linear-gradient(135deg, #2d3041 0%, #3a3f50 100%); padding: 12px 20px; border-radius: 12px; border: 1px solid #3a3f50; font-size: 0.9rem; color: #f8f9fa; display: flex; align-items: center; gap: 8px;'>
                                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M2 12h20"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/></svg> GLOBAL NETWORK
                            </div>
                        </div>
                    </div>
                """)
                
                with gr.Row():
                    with gr.Column(scale=8):
                        chatbot_ui = gr.Chatbot(height=500, type="messages", elem_classes="chatbot")
                        with gr.Row():
                            chat_input = gr.Textbox(
                                placeholder="Describe symptoms or ask for treatment suggestions...", 
                                container=False, 
                                scale=7, 
                                elem_classes="chat-input"
                            )
                            chat_submit = gr.Button("Ask MedoraX", variant="primary", scale=1, elem_classes="primary-btn")
                
                chat_submit.click(groq_chat, [chat_input, chatbot_ui, lang_dropdown], [chatbot_ui, chat_input])

            # TAB 2: ADVANCED DIAGNOSTICS
            with gr.Column(visible=False) as diag_view:
                gr.Markdown("## ADVANCED DIAGNOSTICS", elem_classes="section-title")
                
                with gr.Row():
                    with gr.Column(scale=1, elem_classes="matte-panel"):
                        diag_title = gr.Markdown("### CLINICAL ANALYSIS")
                        diag_sub = gr.Markdown("Upload medical image and describe symptoms via voice or text.")
                        
                        with gr.Tabs():
                            with gr.TabItem("VOICE INPUT"):
                                audio_input = gr.Audio(sources=["microphone"], type="filepath", label="Record Symptoms")
                            with gr.TabItem("TEXT INPUT"):
                                text_input = gr.Textbox(
                                    label="Text Description (if no voice)",
                                    placeholder="Describe your symptoms in detail...",
                                    lines=4
                                )
                        
                        image_input = gr.Image(type="filepath", label="Medical Image Upload")
                        analyze_btn = gr.Button("Analyze with AI", variant="primary", elem_classes="primary-btn")
                    
                    with gr.Column(scale=1, elem_classes="matte-panel"):
                        report_title = gr.Markdown("### DIAGNOSTIC REPORT")
                        transcription_output = gr.Textbox(label="Patient Description", lines=3)
                        analysis_output = gr.Textbox(label="Medical Assessment", lines=8, elem_classes="diagnosis-report")
                        
                        with gr.Row():
                            get_treatment_btn = gr.Button("GET TREATMENT SUGGESTIONS", variant="primary", elem_classes="treatment-btn", scale=1)
                            audio_output = gr.Audio(label="Audio Summary", autoplay=True, scale=1)
                        
                        treatment_output = gr.Textbox(label="💊 Treatment & Medication Suggestions", lines=10, elem_classes="treatment-report", visible=False)
                        
                        # Disclaimer box
                        disclaimer_box = gr.HTML("""
                            <div class='warning-box'>
                                <h4 style='margin:0 0 8px 0; color:#f59e0b; display:flex; align-items:center; gap:8px;'>
                                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>
                                    CRITICAL NOTICE
                                </h4>
                                <p style='margin:0; color:#d1d5db; font-size:0.9rem;'>
                                    MedoraX is an AI diagnostic assistant, not a licensed physician. 
                                    Always consult healthcare professionals before taking any medication. 
                                    Dosages should be determined by qualified doctors.
                                </p>
                            </div>
                        """)

                # Connect the analyze button
                analyze_btn.click(
                    process_inputs, 
                    [audio_input, image_input, text_input, lang_dropdown], 
                    [transcription_output, analysis_output, audio_output, treatment_output]
                ).then(
                    fn=lambda: gr.update(visible=True),
                    outputs=[treatment_output]
                )
                
                # Connect treatment button
                get_treatment_btn.click(
                    get_treatment_suggestions_for_diagnosis,
                    [analysis_output, transcription_output, lang_dropdown],
                    [treatment_output]
                ).then(
                    fn=lambda: gr.update(visible=True),
                    outputs=[treatment_output]
                )

            # TAB 3: NEARBY CARE
            with gr.Column(visible=False) as map_view:
                gr.Markdown("## HOSPITAL FINDER", elem_classes="section-title")
                
                with gr.Row(elem_classes="matte-panel"):
                    manual_location = gr.Textbox(
                        placeholder="Enter city, area or zip code (e.g. Pune, Panvel)",
                        label="Search Location",
                        container=False,
                        scale=4
                    )
                    manual_btn = gr.Button("Find Nearby Hospitals", variant="primary", scale=1, elem_classes="primary-btn")

                # Status display
                status_display = gr.Markdown("### Status: Enter a location to start")
                
                # Map display area
                map_display = gr.HTML(f"""
                    <div style='text-align: center; padding: 40px 20px; color: #adb5bd; 
                                background: linear-gradient(145deg, #2d3041 0%, #252836 100%); 
                                border-radius: 16px; border: 2px dashed #3a3f50; margin: 20px 0;'>
                        <div class='text-logo' style='margin-bottom: 20px; opacity: 0.5;'>
                            <div class='logo-main' style='font-size: 1.5rem;'><span class='logo-medora'>MEDORA</span><span class='logo-x'>-X</span></div>
                        </div>
                        <div style='font-size: 2.5rem; margin-bottom: 20px; color: #3a3f50;'>
                            <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#adb5bd" stroke-width="1.5"><circle cx="12" cy="12" r="10"/><path d="M12 2a14.5 14.5 0 0 0 0 20 14.5 14.5 0 0 0 0-20"/><path d="M2 12h20"/></svg>
                        </div>
                        <h3 style='color: #f8f9fa; margin-bottom: 12px;'>HOSPITAL FINDER</h3>
                        <p>Enter a city or area above to see nearby hospitals and their contact info.</p>
                    </div>
                """)
                
                # Hospitals list display area
                hospitals_display = gr.HTML()
                
                def find_care_flow(query):
                    if not query or len(query.strip()) < 3:
                        return gr.update(), gr.update(value="<div class='matte-panel'>❌ Please enter a valid location (at least 3 characters).</div>"), "### Status: ❌ Invalid location"
                    
                    print(f"DEBUG: Search Flow Triggered for: '{query}'")
                    res_map, res_cards, res_status = find_hospitals_nearby(address=query)
                    return res_map, res_cards, res_status

                manual_btn.click(
                    fn=lambda: "### Status: 🔍 Searching hospitals...",
                    outputs=status_display
                ).then(
                    fn=find_care_flow,
                    inputs=[manual_location],
                    outputs=[map_display, hospitals_display, status_display]
                )
                
                manual_location.submit(
                    fn=lambda: "### Status: 🔍 Searching hospitals...",
                    outputs=status_display
                ).then(
                    fn=find_care_flow,
                    inputs=[manual_location],
                    outputs=[map_display, hospitals_display, status_display]
                )
            
            # TAB 4: ABOUT
            with gr.Column(visible=False) as about_view:
                gr.HTML(f"""
                    <div style='max-width: 1000px; margin: 0 auto; padding: 40px 20px;'>
                        <div style='text-align: center; margin-bottom: 50px;'>
                            <div class='text-logo logo-welcome' style='margin-bottom: 30px;'>
                                <div class='logo-main'><span class='logo-medora'>MEDORA</span><span class='logo-x'>-X</span></div>
                                <div class='logo-sub'>AI Health Assistant</div>
                            </div>
                            <h1 style='font-size: 2.5rem; font-weight: 800; margin-bottom: 16px; color: #ffffff;'>
                                Redefining Modern Diagnostics
                            </h1>
                            <p style='font-size: 1.1rem; color: #adb5bd; line-height: 1.6; max-width: 700px; margin: 0 auto;'>
                                MedoraX (v2.0) is a comprehensive AI health assistant designed to bridge the gap between 
                                advanced technology and accessible medical intelligence.
                            </p>
                        </div>

                        <div class='matte-panel pulse-red' style='background: linear-gradient(145deg, #2a0505 0%, #1a0505 100%); border: 1px solid #7f1d1d; margin-bottom: 40px;'>
                            <h3 style='font-size: 1.4rem; font-weight: 700; color: #ef4444; margin-bottom: 12px; display: flex; align-items: center; gap: 10px;'>
                                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg> 
                                SAFETY PROTOCOLS
                            </h3>
                            <p style='color: #f8f9fa; line-height: 1.6; font-size: 1rem;'>
                                <strong>MedoraX is an experimental AI tool and not a substitute for clinical judgment.</strong><br>
                                If you are experiencing severe symptoms such as difficulty breathing, intense chest pain, or 
                                heavy bleeding, please contact emergency services immediately.
                            </p>
                        </div>
                        
                        <div style='display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 25px;'>
                            <div class='matte-panel medical-card'>
                                <h3 style='color: #ffffff; margin-bottom: 16px; font-size: 1.3rem; display:flex; align-items:center; gap:10px;'>
                                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>
                                    VISION AI
                                </h3>
                                <p style='color: #adb5bd; line-height: 1.6;'>State-of-the-art visual analysis for dermatological, orthopedic, and general medical imagery.</p>
                            </div>
                            
                            <div class='matte-panel medical-card' style='border-left-color: #3a86ff;'>
                                <h3 style='color: #ffffff; margin-bottom: 16px; font-size: 1.3rem; display:flex; align-items:center; gap:10px;'>
                                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 16a4 4 0 1 0 0-8 4 4 0 0 0 0 8z"/><path d="M3 6h18"/><path d="M3 12h18"/><path d="M3 18h18"/></svg>
                                    MEDICAL REASONING
                                </h3>
                                <p style='color: #adb5bd; line-height: 1.6;'>Large Language Model integration for symptom triage and cross-referencing treatment suggestions.</p>
                            </div>
                            
                            <div class='matte-panel medical-card' style='border-left-color: #3a86ff;'>
                                <h3 style='color: #ffffff; margin-bottom: 16px; font-size: 1.3rem; display:flex; align-items:center; gap:10px;'>
                                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="1 6 1 22 8 18 16 22 23 18 23 2 16 6 8 2 1 6"/><line x1="8" y1="2" x2="8" y2="18"/><line x1="16" y1="6" x2="16" y2="22"/></svg>
                                    SMART MAPPING
                                </h3>
                                <p style='color: #adb5bd; line-height: 1.6;'>Intelligent geolocation to find the nearest specialized healthcare facilities and pharmacies.</p>
                            </div>
                        </div>
                    </div>
                """)

    # --- Navigation Logic ---
    def show_chat():
        return [
            gr.update(visible=True), gr.update(visible=False), gr.update(visible=False), gr.update(visible=False),
            gr.update(elem_classes="nav-btn nav-btn-active icon-chat"), gr.update(elem_classes="nav-btn icon-diag"), 
            gr.update(elem_classes="nav-btn icon-map"), gr.update(elem_classes="nav-btn icon-about")
        ]
    
    def show_diag():
        return [
            gr.update(visible=False), gr.update(visible=True), gr.update(visible=False), gr.update(visible=False),
            gr.update(elem_classes="nav-btn icon-chat"), gr.update(elem_classes="nav-btn nav-btn-active icon-diag"), 
            gr.update(elem_classes="nav-btn icon-map"), gr.update(elem_classes="nav-btn icon-about")
        ]
    
    def show_map():
        return [
            gr.update(visible=False), gr.update(visible=False), gr.update(visible=True), gr.update(visible=False),
            gr.update(elem_classes="nav-btn icon-chat"), gr.update(elem_classes="nav-btn icon-diag"), 
            gr.update(elem_classes="nav-btn nav-btn-active icon-map"), gr.update(elem_classes="nav-btn icon-about")
        ]
    
    def show_about():
        return [
            gr.update(visible=False), gr.update(visible=False), gr.update(visible=False), gr.update(visible=True),
            gr.update(elem_classes="nav-btn icon-chat"), gr.update(elem_classes="nav-btn icon-diag"), 
            gr.update(elem_classes="nav-btn icon-map"), gr.update(elem_classes="nav-btn nav-btn-active icon-about")
        ]

    # Connect navigation buttons
    nav_chat.click(show_chat, outputs=[chat_view, diag_view, map_view, about_view, nav_chat, nav_diag, nav_map, nav_about])
    nav_diag.click(show_diag, outputs=[chat_view, diag_view, map_view, about_view, nav_chat, nav_diag, nav_map, nav_about])
    nav_map.click(show_map, outputs=[chat_view, diag_view, map_view, about_view, nav_chat, nav_diag, nav_map, nav_about])
    nav_about.click(show_about, outputs=[chat_view, diag_view, map_view, about_view, nav_chat, nav_diag, nav_map, nav_about])

    # Language Change Event
    def switch_language(lang):
        t = TRANSLATIONS.get(lang, TRANSLATIONS["English"])
        title_text = t['title']
        return [
            gr.update(value=f"""<div style='margin-bottom: 40px;'>
                    <div class='text-logo logo-header'>
                        <div class='logo-main'><span class='logo-medora'>{title_text if lang != 'English' else 'MEDORA'}</span><span class='logo-x'>-X</span></div>
                        <div class='logo-sub'>AI Health Assistant</div>
                    </div>
                </div>"""),
            gr.update(value=t["diag_tab"]),
            gr.update(value=t["map_tab"]),
            gr.update(value=t["about_tab"]),
            gr.update(value=f"""<div style='text-align: center; padding: 40px 20px; max-width: 900px; margin: 0 auto;'>
                    <div class='text-logo logo-welcome' style='margin-bottom: 30px;'>
                        <div class='logo-main'><span class='logo-medora'>{title_text if lang != 'English' else 'MEDORA'}</span><span class='logo-x'>-X</span></div>
                        <div class='logo-sub'>AI Health Assistant</div>
                    </div>
                    <h1 style='font-size: 2.8rem; font-weight: 800; margin-bottom: 20px; color: #f8fafc; line-height: 1.1;'>
                        {t['welcome']}
                    </h1>
                    <p style='font-size: 1.1rem; color: #adb5bd; line-height: 1.6; margin-bottom: 30px;'>
                        {t['sub_welcome']}
                    </p>
                </div>"""),
            gr.update(placeholder=t["chat_placeholder"]),
            gr.update(value=t["ask_btn"]),
            gr.update(value=f"### {t['upload_title']}"),
            gr.update(value=t["upload_sub"]),
            gr.update(value=t["analyze_btn"]),
            gr.update(value=t["get_treatment_btn"]),
            gr.update(value=f"### {t['analysis_report']}"),
            gr.update(label=t["transcription_label"]),
            gr.update(label=t["insight_label"]),
            gr.update(label=t["treatment_label"]),
            gr.update(label=t["voice_summary"]),
            gr.update(value=f"<div style='text-align: center; padding: 15px 5px; color: #8b9dc3; font-size: 0.75rem;'><p style='margin: 0;'>© 2026 MedoraX. {t['disclaimer']}</p></div>"),
            gr.update(value=t["chat_tab"]),
            gr.update(label=t["text_input_label"]),
            gr.update(placeholder=t["text_input_placeholder"]),
            gr.update(label=t["voice_tab"]),
            gr.update(label=t["text_tab"])
        ]

    lang_dropdown.change(
        switch_language, 
        inputs=[lang_dropdown], 
        outputs=[header_title, nav_diag, nav_map, nav_about, welcome_box, chat_input, chat_submit, diag_title, diag_sub, analyze_btn, get_treatment_btn, report_title, transcription_output, analysis_output, treatment_output, audio_output, footer_disclaimer, nav_chat, text_input, text_input, audio_input, text_input]
    )

demo.launch(debug=True, show_api=False, share=False, favicon_path="favicon.svg")