# 🏥 MedoraX-AI Clinical Assistant

> An AI-powered multimodal healthcare diagnostic system providing real-time medical guidance through voice, image, and text.

---

## 📌 About the Project

MedoraX is a comprehensive AI-powered clinical assistant designed to make healthcare guidance accessible to everyone — anytime, anywhere. It enables users to describe symptoms via voice, upload medical images for analysis, and receive structured diagnostic insights and treatment recommendations, all through a conversational web interface.

The platform is specifically built with multilingual support (English, Hindi, and Marathi) to serve India's linguistically diverse population, including users in rural or underserved areas where immediate medical consultation may not be available.

> ⚠️ **Disclaimer:** MedoraX is an AI diagnostic assistant and not a licensed physician. Always consult a qualified healthcare professional before making medical decisions.

---

## ✨ Key Features

- **🎤 Voice-Based Symptom Input** — Record symptoms in English, Hindi, or Marathi using Whisper-large-v3 for speech-to-text transcription
- **🖼️ Medical Image Analysis** — Upload X-rays, skin condition photos, or lab reports for AI-powered visual diagnostics using Llama-4-scout
- **💬 AI Chat Consultation** — Ask medical questions and receive structured, evidence-based responses via Llama-3.3-70b
- **🗺️ Hospital Finder** — GPS-based nearby hospital search with ratings, contact info, and turn-by-turn directions via Google Maps & Places API
- **🌬️ Air Quality Monitoring** — Real-time AQI data and health recommendations via Google Air Quality API
- **🚨 Emergency Detection** — Automated keyword detection for critical symptoms triggering immediate hospital location
- **🔊 Text-to-Speech Output** — AI responses delivered as audio in the user's chosen language via Edge TTS and gTTS
- **🌐 Multilingual UI** — Complete interface translation in English, Hindi, and Marathi

---

## 🛠️ Technology Stack

### Frontend
| Technology | Purpose |
|---|---|
| Gradio 4.x | Web interface framework with real-time interactive components |
| CSS3 | Medical-themed responsive design with custom styling |
| Python 3.8+ with Asyncio | Backend logic, async processing, and API orchestration |

### AI & APIs
| Service | Model / API | Role |
|---|---|---|
| Groq API | Whisper-large-v3 | Voice transcription (95%+ accuracy) |
| Groq API | Llama-4-scout-17b | Medical image analysis |
| Groq API | Llama-3.3-70b-versatile | Treatment generation & chat |
| Google Maps API | Maps JavaScript API | Interactive hospital map rendering |
| Google Places API | Places API | Hospital search, ratings, directions |
| Google Air Quality API | Current Conditions | Real-time AQI & health recommendations |

### Voice Processing
| Library | Role |
|---|---|
| `speech_recognition` | Microphone audio capture |
| `edge_tts` | Neural TTS (language-specific voices) |
| `gTTS` | Fallback text-to-speech |
| `pydub` | Audio format conversion |

### Image Processing
| Library | Role |
|---|---|
| `Pillow (PIL)` | Image resizing, format conversion, base64 encoding |

### Deployment
| Platform | Role |
|---|---|
| Hugging Face Spaces | Hosting and model integration |
| Folium | Interactive map rendering |

---

## 🏗️ System Architecture

MedoraX is structured into five core modules:

```
GradioApp
├── VoiceOfPatient     → record_audio(), transcribe()
├── BrainOfDoctor      → encode_image(), analyze_image()
├── VoiceOfDoctor      → text_to_speech()
└── NearbyCare         → geocode_address(), get_hospitals(), create_map()
```

The client browser communicates with the Gradio web interface hosted on Hugging Face Spaces. The backend asynchronously calls Groq AI services and Google APIs over HTTPS. A three-tier caching system (image cache, TTS cache, place details cache) optimizes response times to 4–7 seconds.

---

## 🔁 How It Works

1. **User selects language** (English / Hindi / Marathi) and input mode (voice, image, or text)
2. **Voice input** → Recorded audio is transcribed via Groq Whisper API
3. **Image input** → Medical image is encoded and sent to Llama-4-scout for visual diagnosis
4. **Text/Chat input** → Query is processed by Llama-3.3-70b for a structured medical response
5. **Emergency detection** → Critical keywords trigger automatic nearby hospital search
6. **Output** → Diagnostic result is displayed as text and played back as audio in the selected language

---

## 🌍 Target Users

- **General Public** — Individuals seeking preliminary AI-powered medical diagnostics
- **Patients & Caregivers** — People managing chronic conditions or monitoring symptoms
- **Non-English Speakers** — Hindi and Marathi speakers requiring healthcare guidance in their native language
- **Rural Communities** — Users in areas with limited access to immediate medical facilities
- **Emergency Situations** — Users needing rapid hospital location and navigation

---

## ⚙️ Installation & Setup

### Prerequisites
- Python 3.8+
- Node.js (for any front-end development)
- A Hugging Face account (for deployment)

### Environment Variables
Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key_here
GOOGLE_MAPS_API_KEY=your_google_maps_api_key_here
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

Key packages include:
```
gradio>=4.0
groq
pillow
pydub
edge-tts
gTTS
speechrecognition
folium
geopy
requests
python-dotenv
aiohttp
```

### Run Locally

```bash
python app.py
```

The application will launch at `http://localhost:7860`.

### Deploy to Hugging Face Spaces

Upload all project files (Python modules, `requirements.txt`, `.env` config) to a Hugging Face Space configured with the Gradio SDK. The app deploys automatically on file update.

---

## 📁 Project Structure

```
medorax/
├── app.py                    # Main Gradio application & UI
├── brain_of_the_doctor.py    # Image encoding & AI vision analysis
├── voice_of_the_patient.py   # Audio recording & speech transcription
├── voice_of_the_doctor.py    # Text-to-speech output (multilingual)
├── nearby_care.py            # Hospital finder, geocoding & air quality
├── requirements.txt
└── .env                      # API keys (not committed to repo)
```

---

## 📊 Supported Languages

| Language | Voice Input | Voice Output | UI |
|---|---|---|---|
| English | ✅ | ✅ (en-US-AriaNeural) | ✅ |
| Hindi (हिंदी) | ✅ | ✅ (hi-IN-SwaraNeural) | ✅ |
| Marathi (मराठी) | ✅ | ✅ (mr-IN-AarohiNeural) | ✅ |

---

## 🔮 Future Scope

- **More Indian Languages** — Tamil, Telugu, Gujarati, Bengali, Kannada
- **Wearable Device Integration** — Real-time vitals monitoring (heart rate, blood pressure, glucose, SpO₂)
- **Telemedicine Connectivity** — Direct video consultations with verified doctors
- **Medical History Tracking** — Secure storage of past consultations and diagnoses
- **Offline Mode** — Basic diagnostics without internet using cached AI models
- **Specialized Modules** — Dermatology, ophthalmology, cardiology, and radiology diagnostics
- **Mental Health Support** — Emotionally intelligent conversational AI with mood tracking
- **Blockchain Health Records** — HIPAA-compliant, end-to-end encrypted medical data
- **Pharmacy & Lab Finder** — Locate nearby pharmacies and diagnostic labs

---

## 🎓 Academic Details

| Field | Details |
|---|---|
| Project Title | MedoraX-AI Clinical Assistant |
| Student | Prajakta Vilas Nigudse |
| Seat No. | 26CS603032 |
| Degree | B.Sc. Computer Science (Semester VI) |
| Guide | Ms. Aishwarya Mokal |
| Institution | Pillai HOC College of Arts, Science & Commerce (Autonomous), Rasayani |
| University | University of Mumbai |
| Academic Year | 2025–26 |

---

## 📚 References

1. Healthcare Chatbot using NLP Techniques — JUIT Final Year Project Report
2. Medical Chatbot for Patients — GitHub Repository (May 2024)
3. Chatbot for Health Care and Oncology Applications — NCBI PMC, 2021 (PMCID: PMC8669584)
4. Google Maps API Documentation — https://developers.google.com/maps/documentation
5. National Ambulance Helpline Numbers (India) — Emergency: **102** / **108**

---

## 📄 License

This project was developed as an academic submission. Please contact the author for usage permissions.
