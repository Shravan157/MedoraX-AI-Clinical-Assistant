# # if you dont use pipenv uncomment the following:
# from dotenv import load_dotenv
# load_dotenv()

# import os
# import gradio as gr
# import requests
# import json
# import re
# from groq import Groq

# from brain_of_the_doctor import encode_image, analyze_image_with_query
# from voice_of_the_patient import record_audio, transcribe_with_groq
# from voice_of_the_doctor import text_to_speech_with_gtts, text_to_speech_with_elevenlabs

# # --- Import for Maps ---
# import folium
# from folium import plugins
# from geopy.distance import geodesic

# # --- Configuration ---
# GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
# GOOGLE_MAPS_API_KEY = os.environ.get("GOOGLE_MAPS_API_KEY")  # Add this to your .env file
# client = Groq(api_key=GROQ_API_KEY)

# # --- Translations ---
# TRANSLATIONS = {
#     "English": {
#         "title": "MEDIBOT",
#         "chat_tab": "💬 Smart Consult",
#         "diag_tab": "🔍 AI Diagnostics",
#         "map_tab": "🗺️ Nearby Care",
#         "about_tab": "ℹ️ About",
#         "welcome": "Your Health. Our Intelligence.",
#         "sub_welcome": "Empowering patients with instant, reliable, and multi-language medical guidance.",
#         "chat_placeholder": "How can I help you today?",
#         "ask_btn": "Ask MediBot",
#         "emergency_btn": "🚨 Find Nearby Hospitals",
#         "upload_title": "📸 Clinical Upload",
#         "upload_sub": "Upload an image of the concern and record symptoms.",
#         "analyze_btn": "Analyze with AI Doctor",
#         "analysis_report": "🤖 Analysis Report",
#         "transcription_label": "Transcribed Symptoms",
#         "insight_label": "Medical Insight",
#         "voice_summary": "Voice Summary",
#         "disclaimer": "Disclaimer: MediBot is an AI assistant, not a licensed doctor. Always seek professional help for critical health issues.",
#         "map_title": "Local Healthcare Facilities",
#         "map_desc": "Automatically finding the nearest hospitals and clinics for you.",
#         "find_best_btn": "✨ Find Best Care Nearby",
#         "fetching_msg": "🔍 Identifying top healthcare facilities in your area...",
#     },
#     "Hindi": {
#         "title": "मेडिबॉट",
#         "chat_tab": "💬 स्मार्ट चैट",
#         "diag_tab": "🔍 एआई निदान",
#         "map_tab": "🗺️ पास के अस्पताल",
#         "about_tab": "ℹ️ जानकारी",
#         "welcome": "आपका स्वास्थ्य। हमारी बुद्धिमत्ता।",
#         "sub_welcome": "मरीजों को तत्काल, विश्वसनीय और बहुभाषी चिकित्सा मार्गदर्शन के साथ सशक्त बनाना।",
#         "chat_placeholder": "मैं आज आपकी कैसे मदद कर सकता हूँ?",
#         "ask_btn": "मेडिबॉट से पूछें",
#         "emergency_btn": "🚨 पास के अस्पताल खोजें",
#         "upload_title": "📸 क्लिनिकल अपलोड",
#         "upload_sub": "चिंता वाले क्षेत्र की छवि अपलोड करें और लक्षण रिकॉर्ड करें।",
#         "analyze_btn": "एआई डॉक्टर के साथ विश्लेषण करें",
#         "analysis_report": "🤖 विश्लेषण रिपोर्ट",
#         "transcription_label": "श्रुतलेख लक्षण",
#         "insight_label": "चिकित्सा अंतर्दृष्टि",
#         "voice_summary": "आवाज़ सारांश",
#         "disclaimer": "अस्वीकरण: मेडिबॉट एक एआई सहायक है, लाइसेंस प्राप्त डॉक्टर नहीं। गंभीर स्वास्थ्य समस्याओं के लिए हमेशा पेशेवर मदद लें।",
#         "map_title": "स्थानीय स्वास्थ्य सुविधाएं",
#         "map_desc": "आपके क्षेत्र के आधार पर पास के अस्पतालों और क्लीनिकों को दिखा रहा है।",
#         "find_best_btn": "✨ सबसे अच्छी देखभाल खोजें",
#         "fetching_msg": "🔍 आपके क्षेत्र में शीर्ष स्वास्थ्य सुविधाओं की पहचान की जा रही है...",
#     },
#     "Marathi": {
#         "title": "मेडिबॉट",
#         "chat_tab": "💬 स्मार्ट चॅट",
#         "diag_tab": "🔍 एआय निदान",
#         "map_tab": "🗺️ जवळची रुग्णालये",
#         "about_tab": "ℹ️ माहिती",
#         "welcome": "तुमचे आरोग्य. आमची बुद्धिमत्ता.",
#         "sub_welcome": "रुग्णांना त्वरित, विश्वसनीय आणि बहुभाषिक वैद्यकीय मार्गदर्शनासह सक्षम करणे.",
#         "chat_placeholder": "मी तुम्हाला आज कशी मदत करू शकतो?",
#         "ask_btn": "मेडिबॉटला विचारा",
#         "emergency_btn": "🚨 जवळची रुग्णालये शोधा",
#         "upload_title": "📸 क्लिनिकल अपलोड",
#         "upload_sub": "तपासणीसाठी फोटो अपलोड करा आणि लक्षणे सांगा.",
#         "analyze_btn": "एआय डॉक्टरांसह विश्लेषण करा",
#         "analysis_report": "🤖 विश्लेषण अहवाल",
#         "transcription_label": "लक्षणे",
#         "insight_label": "वैद्यकीय माहिती",
#         "voice_summary": "ध्वनी सारांश",
#         "disclaimer": "डिस्क्लेमर: मेडिबॉट हा एआय असिस्टंट आहे, डॉक्टर नाही. गंभीर आरोग्य समस्यांसाठी नेहमी डॉक्टरांचा सल्ला घ्या.",
#         "map_title": "स्थानिक आरोग्य सुविधा",
#         "map_desc": "तुमच्या क्षेत्रातील जवळची रुग्णालये आणि दवाखाने दर्शवित आहे.",
#         "find_best_btn": "✨ सर्वोत्तम निगा शोधा",
#         "fetching_msg": "🔍 तुमच्या क्षेत्रातील टॉप आरोग्य सुविधा शोधत आहोत...",
#     }
# }

# # --- Logic Functions ---
# def get_hospitals_from_google_maps(lat, lon, radius_km=5):
#     """
#     Fetch hospitals from Google Maps Places API
#     """
#     try:
#         lat = float(lat)
#         lon = float(lon)
        
#         # Google Maps Places API endpoint
#         url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
        
#         params = {
#             'location': f'{lat},{lon}',
#             'radius': radius_km * 1000,  # Convert km to meters
#             'type': 'hospital',
#             'keyword': 'hospital clinic medical emergency healthcare',
#             'key': GOOGLE_MAPS_API_KEY
#         }
        
#         # Make request
#         response = requests.get(url, params=params, timeout=30)
        
#         # Check if response is valid
#         if response.status_code != 200:
#             print(f"Google Maps API error: HTTP {response.status_code}")
#             return []
        
#         data = response.json()
        
#         if data.get('status') != 'OK':
#             print(f"Google Maps API status: {data.get('status')}")
#             return []
        
#         hospitals = []
#         user_location = (lat, lon)
        
#         for place in data.get('results', [])[:10]:  # Limit to 10 results
#             place_lat = place['geometry']['location']['lat']
#             place_lon = place['geometry']['location']['lng']
            
#             # Calculate accurate distance
#             place_location = (place_lat, place_lon)
#             distance = geodesic(user_location, place_location).kilometers
            
#             # Get place details (phone number, address, etc.)
#             place_id = place['place_id']
#             place_details = get_place_details(place_id)
            
#             hospitals.append({
#                 'name': place.get('name', 'Healthcare Facility'),
#                 'lat': place_lat,
#                 'lon': place_lon,
#                 'distance': round(distance, 2),
#                 'phone': place_details.get('phone', 'Not listed'),
#                 'address': place_details.get('address', 'Address not available'),
#                 'opening_hours': place_details.get('opening_hours', 'Check for hours'),
#                 'website': place_details.get('website', ''),
#                 'place_id': place_id
#             })
        
#         # Sort by distance
#         hospitals.sort(key=lambda x: x['distance'])
#         return hospitals
        
#     except requests.exceptions.RequestException as e:
#         print(f"Network error fetching hospitals: {e}")
#         return []
#     except Exception as e:
#         print(f"Error fetching hospitals: {e}")
#         return []

# def get_place_details(place_id):
#     """
#     Get detailed information about a place from Google Maps
#     """
#     try:
#         url = "https://maps.googleapis.com/maps/api/place/details/json"
        
#         params = {
#             'place_id': place_id,
#             'fields': 'formatted_phone_number,formatted_address,website,opening_hours',
#             'key': GOOGLE_MAPS_API_KEY
#         }
        
#         response = requests.get(url, params=params, timeout=10)
#         data = response.json()
        
#         if data.get('status') != 'OK':
#             return {}
        
#         result = data.get('result', {})
        
#         # Format opening hours
#         opening_hours = 'Check for hours'
#         if 'opening_hours' in result and 'weekday_text' in result['opening_hours']:
#             opening_hours = ' | '.join(result['opening_hours']['weekday_text'][:3])
        
#         return {
#             'phone': result.get('formatted_phone_number', 'Not listed'),
#             'address': result.get('formatted_address', 'Address not available'),
#             'website': result.get('website', ''),
#             'opening_hours': opening_hours
#         }
        
#     except Exception as e:
#         print(f"Error getting place details: {e}")
#         return {
#             'phone': 'Not listed',
#             'address': 'Address not available',
#             'website': '',
#             'opening_hours': 'Check for hours'
#         }
        
# def create_hospital_map(lat, lon):
#     """
#     Create an interactive Folium map with user location and nearby hospitals
#     """
#     try:
#         lat, lon = float(lat), float(lon)
        
#         # Create map centered on user location
#         m = folium.Map(
#             location=[lat, lon],
#             zoom_start=14,
#             tiles='OpenStreetMap',
#             control_scale=True,
#             width='100%',
#             height=400
#         )
        
#         # Add user location marker (Cyan)
#         folium.CircleMarker(
#             location=[lat, lon],
#             radius=12,
#             popup='📍 <b>Your Current Location</b>',
#             color='#2dd4bf',
#             fill=True,
#             fillColor='#2dd4bf',
#             fillOpacity=0.8,
#             weight=3
#         ).add_to(m)
        
#         # Get nearby hospitals from Google Maps
#         hospitals = get_hospitals_from_google_maps(lat, lon, radius_km=10)
        
#         if not hospitals:
#             # Add a message to the map if no hospitals found
#             folium.Marker(
#                 location=[lat, lon],
#                 icon=folium.DivIcon(
#                     html=f"""
#                     <div style="background: rgba(0,0,0,0.7); color: white; padding: 10px; border-radius: 5px;">
#                         <b>No hospitals found in 10km radius</b><br>
#                         <small>Try increasing search radius</small>
#                     </div>
#                     """
#                 )
#             ).add_to(m)
        
#         # Add hospital markers (Red)
#         for idx, hospital in enumerate(hospitals, 1):
#             popup_html = f"""
#             <div style='font-family: sans-serif; min-width: 220px;'>
#                 <h4 style='margin: 0 0 8px 0; color: #dc2626;'>🏥 {hospital['name']}</h4>
#                 <p style='margin: 4px 0; font-size: 0.9rem;'><b>Distance:</b> {hospital['distance']} km</p>
#                 <p style='margin: 4px 0; font-size: 0.8rem; color: #555;'>{hospital['address']}</p>
#                 <p style='margin: 4px 0; font-size: 0.8rem;'><b>Phone:</b> {hospital['phone']}</p>
#                 <p style='margin: 4px 0; font-size: 0.8rem;'><b>Hours:</b> {hospital['opening_hours']}</p>
#                 <p style='margin-top: 8px;'>
#                     <a href='https://www.google.com/maps/dir/?api=1&destination={hospital['lat']},{hospital['lon']}' 
#                        target='_blank' style='color: #2dd4bf; text-decoration: none; font-weight: bold;'>
#                        🗺️ Get Directions on Google Maps
#                     </a>
#                 </p>
#             </div>
#             """
            
#             folium.Marker(
#                 location=[hospital['lat'], hospital['lon']],
#                 popup=folium.Popup(popup_html, max_width=300),
#                 icon=folium.Icon(color='red', icon='plus', prefix='fa'),
#                 tooltip=f"{idx}. {hospital['name']} ({hospital['distance']} km)"
#             ).add_to(m)
        
#         # Add fullscreen button
#         plugins.Fullscreen().add_to(m)
        
#         # Add a minimap
#         plugins.MiniMap().add_to(m)
        
#         return m._repr_html_(), hospitals
        
#     except Exception as e:
#         print(f"Error creating map: {e}")
#         return None, []
        
# def format_hospital_cards(hospitals):
#     """
#     Format hospital data into HTML cards
#     """
#     if not hospitals:
#         return """
#         <div style='text-align: center; padding: 40px; color: #f59e0b; background: rgba(245, 158, 11, 0.1); border-radius: 12px; border: 1px solid rgba(245, 158, 11, 0.3);'>
#             <h3 style='margin: 0 0 12px 0;'>⚠️ No Hospitals Found</h3>
#             <p style='margin: 0;'>No healthcare facilities found within 10km. Try increasing search radius.</p>
#         </div>
#         """
    
#     cards_html = "<div style='display: grid; gap: 16px; margin-top: 20px;'>"
    
#     for idx, hospital in enumerate(hospitals, 1):
#         phone_link = f"<a href='tel:{hospital['phone']}' style='color: #2dd4bf; text-decoration: none;'>{hospital['phone']}</a>" if hospital['phone'] != 'Not listed' else hospital['phone']
        
#         directions_url = f"https://www.google.com/maps/dir/?api=1&destination={hospital['lat']},{hospital['lon']}"
        
#         cards_html += f"""
#         <div style='background: rgba(26, 31, 53, 0.85); border: 1px solid rgba(45, 212, 191, 0.2); border-radius: 12px; padding: 20px; transition: all 0.3s ease;'>
#             <div style='display: flex; justify-content: space-between; align-items: start; margin-bottom: 12px;'>
#                 <h3 style='margin: 0; color: #2dd4bf; font-size: 1.2rem;'>
#                     {idx}. 🏥 {hospital['name']}
#                 </h3>
#                 <span style='background: rgba(45, 212, 191, 0.2); color: #2dd4bf; padding: 4px 12px; border-radius: 20px; font-size: 0.85rem; font-weight: 600;'>
#                     {hospital['distance']} km
#                 </span>
#             </div>
#             <div style='color: #94a3b8; line-height: 1.8;'>
#                 <p style='margin: 8px 0;'><strong style='color: #cbd5e1;'>📍 Address:</strong> {hospital['address']}</p>
#                 <p style='margin: 8px 0;'><strong style='color: #cbd5e1;'>📞 Phone:</strong> {phone_link}</p>
#                 <p style='margin: 8px 0;'><strong style='color: #cbd5e1;'>🕒 Hours:</strong> {hospital['opening_hours']}</p>
#                 <div style='margin-top: 12px;'>
#                     <a href='{directions_url}' target='_blank' 
#                        style='color: #2dd4bf; text-decoration: none; font-weight: 600; border: 1px solid #2dd4bf; 
#                               padding: 6px 12px; border-radius: 6px; font-size: 0.9rem; display: inline-block;'>
#                         🗺️ Get Directions on Google Maps
#                     </a>
#                 </div>
#             </div>
#         </div>
#         """
    
#     cards_html += "</div>"
#     return cards_html

# def get_best_hospitals(lat, lon):
#     """
#     Main function to get formatted hospital data with map
#     """
#     if not lat or not lon or lat == "" or lon == "":
#         return (
#             """
#             <div style='text-align: center; padding: 40px; color: #f43f5e; background: rgba(244, 63, 94, 0.1); border-radius: 12px; border: 1px solid rgba(244, 63, 94, 0.3);'>
#                 <h3 style='margin: 0 0 12px 0;'>❌ Location Not Available</h3>
#                 <p style='margin: 0;'>Please allow location access in your browser to find nearby hospitals.</p>
#             </div>
#             """,
#             "### Status: ❌ Location permission required"
#         )
    
#     try:
#         # Create interactive map
#         map_html, hospitals = create_hospital_map(lat, lon)
        
#         if map_html:
#             # Format hospital cards
#             hospital_cards = format_hospital_cards(hospitals)
            
#             # Combine map and cards
#             full_html = f"""
#             <div style='margin-bottom: 24px;'>
#                 <h3 style='color: #2dd4bf; margin-bottom: 16px;'>📍 Interactive Map</h3>
#                 <div style='border-radius: 16px; overflow: hidden; box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);'>
#                     {map_html}
#                 </div>
#                 <p style='color: #94a3b8; margin-top: 12px; font-size: 0.9rem; text-align: center;'>
#                     💡 <strong>Cyan marker</strong> = Your location • <strong>Red markers</strong> = Hospitals • Click markers for details
#                 </p>
#             </div>
            
#             <div>
#                 <h3 style='color: #2dd4bf; margin-bottom: 16px;'>🏥 Nearby Healthcare Facilities</h3>
#                 <p style='color: #94a3b8; margin-bottom: 16px;'>Found {len(hospitals)} facilities within 10km radius:</p>
#                 {hospital_cards}
#             </div>
#             """
            
#             return (
#                 full_html,
#                 f"### Status: ✅ Found {len(hospitals)} hospitals near you"
#             )
#         else:
#             raise Exception("Failed to create map")
            
#     except Exception as e:
#         print(f"Error in get_best_hospitals: {e}")
#         # Fallback to Google Maps search link
#         google_maps_url = f"https://www.google.com/maps/search/hospital/@{lat},{lon},14z"
#         return (
#             f"""
#             <div style='text-align: center; padding: 40px;'>
#                 <h3 style='color: #2dd4bf; margin-bottom: 16px;'>📍 Your Location</h3>
#                 <div style='background: rgba(26, 31, 53, 0.85); border-radius: 12px; padding: 20px; margin-bottom: 20px;'>
#                     <p style='color: #94a3b8; margin: 8px 0;'><strong>Latitude:</strong> {lat[:7]}</p>
#                     <p style='color: #94a3b8; margin: 8px 0;'><strong>Longitude:</strong> {lon[:7]}</p>
#                 </div>
#                 <p style='color: #94a3b8; margin-bottom: 20px;'>Search for hospitals on Google Maps:</p>
#                 <a href='{google_maps_url}' target='_blank' 
#                    style='display: inline-block; padding: 12px 24px; background: #2dd4bf; color: white; 
#                           border-radius: 8px; text-decoration: none; font-weight: 600;'>
#                     🏥 Search Hospitals on Google Maps
#                 </a>
#             </div>
#             """,
#             "### Status: 🔍 Using Google Maps Search"
#         )

# def groq_chat(message, history, language):
#     """
#     Chat with Groq (Llama-3.3-70b) with Medical Persona
#     """
#     if not message:
#         return history + [{"role": "assistant", "content": ""}]
    
#     lang_map = {
#         "Hindi": "Respond primarily in Hindi (हिंदी). Use Devnagari script.",
#         "Marathi": "Respond primarily in Marathi (मराठी). Use Devnagari script.",
#         "English": "Respond in English."
#     }
#     lang_instruction = lang_map.get(language, "Respond in English.")
    
#     system_instruction = (
#         f"You are MediBot, a professional AI medical assistant. "
#         f"{lang_instruction} Provide concise, evidence-based medical advice. "
#         f"Maintain a calm, reassuring tone. "
#         f"CRITICAL: Always advise seeing a doctor for serious symptoms."
#     )

#     try:
#         messages = [{"role": "system", "content": system_instruction}]
#         for h in history:
#             messages.append({"role": h["role"], "content": h["content"]})
        
#         messages.append({"role": "user", "content": message})
        
#         response = client.chat.completions.create(
#             model="llama-3.3-70b-versatile",
#             messages=messages,
#             temperature=0.4,
#             max_tokens=1024,
#         )
#         history.append({"role": "user", "content": message})
#         history.append({"role": "assistant", "content": response.choices[0].message.content})
#         return history, ""
#     except Exception as e:
#         print(f"Chat Error: {e}")
#         history.append({"role": "user", "content": message})
#         history.append({"role": "assistant", "content": f"Error: {str(e)}"})
#         return history, ""

# def process_inputs(audio_filepath, image_filepath):
#     system_prompt="""You have to act as a professional doctor. Use the image provided to identify if there is any medical condition."""
#     if not audio_filepath and not image_filepath:
#          return "No input.", "No input.", None

#     speech_to_text_output = ""
#     if audio_filepath:
#         try:
#             speech_to_text_output = transcribe_with_groq(GROQ_API_KEY=GROQ_API_KEY, 
#                                                          audio_filepath=audio_filepath,
#                                                          stt_model="whisper-large-v3")
#         except: speech_to_text_output = "Transcription failed."
    
#     if image_filepath:
#         query_text = system_prompt + (" " + speech_to_text_output if speech_to_text_output else "")
#         try:
#             doctor_response = analyze_image_with_query(query=query_text, encoded_image=encode_image(image_filepath), model="meta-llama/llama-4-scout-17b-16e-instruct") 
#         except Exception as e:
#             doctor_response = f"Analysis Error: {str(e)}"
#     else:
#         doctor_response = "I need an image for diagnosis."

#     output_audio_path = "final.mp3"
#     cleaned_response = re.sub(r'[*#_`~]', '', doctor_response) if doctor_response else ""
#     try:
#         text_to_speech_with_elevenlabs(input_text=cleaned_response, output_filepath=output_audio_path)
#     except:
#         text_to_speech_with_gtts(input_text=cleaned_response, output_filepath=output_audio_path)
#     return speech_to_text_output, doctor_response, output_audio_path

# def update_ui_language(lang):
#     t = TRANSLATIONS.get(lang, TRANSLATIONS["English"])
#     return [
#         gr.update(value=f"<div style='font-size: 2rem; font-weight: 800; color: #2dd4bf; padding: 20px 15px; letter-spacing: 1px;'>{t['title']}</div>"),
#         gr.update(label=t["diag_tab"]),
#         gr.update(label=t["map_tab"]),
#         gr.update(label=t["about_tab"]),
#         gr.update(value=f"<div style='text-align: center; padding: 40px 20px;'><h1 style='font-size: 3.2rem; font-weight: 800; margin-bottom: 20px; color: #f8fafc; line-height: 1.2;'>{t['welcome']}</h1><p style='font-size: 1.15rem; color: #94a3b8; line-height: 1.7; max-width: 700px; margin: 0 auto;'>{t['sub_welcome']}</p></div>"),
#         gr.update(placeholder=t["chat_placeholder"]),
#         gr.update(value=t["ask_btn"]),
#         gr.update(value=f"### {t['upload_title']}"),
#         gr.update(value=t["upload_sub"]),
#         gr.update(value=t["analyze_btn"]),
#         gr.update(value=f"### {t['analysis_report']}"),
#         gr.update(label=t["transcription_label"]),
#         gr.update(label=t["insight_label"]),
#         gr.update(label=t["voice_summary"]),
#         gr.update(value=f"<div style='text-align: center; padding: 30px 20px; color: #64748b; font-size: 0.9rem; border-top: 1px solid rgba(45, 212, 191, 0.1); margin-top: 40px;'><p style='margin: 0;'>© 2026 MediBot. {t['disclaimer']}</p></div>"),
#         gr.update(label=t["chat_tab"]),
#         gr.update(value=t["find_best_btn"])
#     ]

# # --- UI Assets ---
# custom_css = """
# @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap');

# :root { 
#     --primary: #2dd4bf; 
#     --primary-dark: #0d9488; 
#     --primary-light: #5eead4;
#     --bg-dark: #0a0f1e; 
#     --bg-card: #1a1f35;
#     --card-bg: rgba(26, 31, 53, 0.85);
#     --text-primary: #f8fafc;
#     --text-secondary: #94a3b8;
#     --text-muted: #64748b;
#     --border: rgba(45, 212, 191, 0.15);
#     --shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.4);
# }

# .hidden-component {
#     display: none !important;
# }

# * {
#     font-family: 'Poppins', -apple-system, BlinkMacSystemFont, sans-serif !important;
# }

# body, .gradio-container { 
#     background: linear-gradient(135deg, var(--bg-dark) 0%, #0f1729 100%) !important;
#     color: var(--text-primary) !important;
#     min-height: 100vh;
# }

# .glass-panel { 
#     background: var(--card-bg);
#     backdrop-filter: blur(16px) saturate(180%);
#     -webkit-backdrop-filter: blur(16px) saturate(180%);
#     border: 1px solid var(--border);
#     border-radius: 20px;
#     padding: 32px;
#     box-shadow: var(--shadow);
#     transition: all 0.3s ease;
# }

# .glass-panel:hover {
#     border-color: var(--primary);
#     box-shadow: 0 12px 48px 0 rgba(45, 212, 191, 0.15);
# }

# .primary-btn { 
#     background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%) !important;
#     color: white !important;
#     border: none !important;
#     border-radius: 12px !important;
#     font-weight: 600 !important;
#     padding: 12px 28px !important;
#     font-size: 15px !important;
#     letter-spacing: 0.3px !important;
#     cursor: pointer;
#     transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
#     box-shadow: 0 4px 12px rgba(45, 212, 191, 0.25) !important;
# }

# .primary-btn:hover {
#     transform: translateY(-2px) !important;
#     box-shadow: 0 8px 24px rgba(45, 212, 191, 0.4) !important;
# }

# .primary-btn:active {
#     transform: translateY(0) !important;
# }

# /* Enhanced Tab Styling */
# .tabs {
#     border-bottom: 2px solid var(--border) !important;
#     margin-bottom: 24px !important;
# }

# .tab-nav button {
#     color: var(--text-secondary) !important;
#     font-weight: 500 !important;
#     font-size: 15px !important;
#     padding: 14px 24px !important;
#     transition: all 0.3s ease !important;
#     border-radius: 8px 8px 0 0 !important;
# }

# .tab-nav button:hover {
#     color: var(--primary-light) !important;
#     background: rgba(45, 212, 191, 0.05) !important;
# }

# .tab-nav button.selected {
#     color: var(--primary) !important;
#     background: rgba(45, 212, 191, 0.1) !important;
#     border-bottom: 3px solid var(--primary) !important;
#     font-weight: 600 !important;
# }

# /* Chatbot Styling */
# .chatbot {
#     border-radius: 16px !important;
#     border: 1px solid var(--border) !important;
#     background: var(--bg-card) !important;
# }

# /* Input Fields */
# input, textarea, .input-field {
#     background: rgba(255, 255, 255, 0.05) !important;
#     border: 1px solid var(--border) !important;
#     border-radius: 12px !important;
#     color: var(--text-primary) !important;
#     padding: 12px 16px !important;
#     transition: all 0.3s ease !important;
# }

# input:focus, textarea:focus {
#     border-color: var(--primary) !important;
#     box-shadow: 0 0 0 3px rgba(45, 212, 191, 0.1) !important;
#     outline: none !important;
# }

# /* Headers */
# h1, h2, h3, h4 {
#     color: var(--text-primary) !important;
#     font-weight: 700 !important;
#     letter-spacing: -0.5px !important;
# }

# /* Feature Cards */
# .feature-card {
#     background: var(--card-bg);
#     border: 1px solid var(--border);
#     border-radius: 16px;
#     padding: 28px;
#     transition: all 0.3s ease;
#     height: 100%;
# }

# .feature-card:hover {
#     transform: translateY(-4px);
#     border-color: var(--primary);
#     box-shadow: 0 12px 32px rgba(45, 212, 191, 0.2);
# }

# .feature-icon {
#     font-size: 2.5rem;
#     margin-bottom: 16px;
#     display: inline-block;
# }

# footer { 
#     display: none !important; 
# }

# /* Scrollbar */
# ::-webkit-scrollbar {
#     width: 10px;
# }

# ::-webkit-scrollbar-track {
#     background: var(--bg-dark);
# }

# ::-webkit-scrollbar-thumb {
#     background: var(--primary-dark);
#     border-radius: 5px;
# }

# ::-webkit-scrollbar-thumb:hover {
#     background: var(--primary);
# }
# """

# # --- App Layout ---

# with gr.Blocks(css=custom_css, title="MediBot - AI Healthcare Assistant") as demo:
    
#     # Hidden State for Location
#     user_lat = gr.State(None)
#     user_lon = gr.State(None)

#     with gr.Row(variant="compact"):
#         with gr.Column(scale=4):
#             header_title = gr.HTML("<div style='font-size: 2rem; font-weight: 800; color: #2dd4bf; padding: 20px 15px; letter-spacing: 1px;'>MEDIBOT</div>")
#         with gr.Column(scale=1):
#             lang_dropdown = gr.Dropdown(choices=["English", "Hindi", "Marathi"], value="English", label="Select Language", container=False)
    
#     with gr.Tabs() as tabs_container:
        
#         # TAB 1: SMART CHAT
#         with gr.TabItem("💬 Smart Consult") as chat_tab:
#             welcome_box = gr.HTML("""
#                 <div style='text-align: center; padding: 40px 20px;'>
#                     <h1 style='font-size: 3.2rem; font-weight: 800; margin-bottom: 20px; color: #f8fafc; line-height: 1.2;'>
#                         Your Health. Our Intelligence.
#                     </h1>
#                     <p style='font-size: 1.15rem; color: #94a3b8; line-height: 1.7; max-width: 700px; margin: 0 auto;'>
#                         Empowering patients with instant, reliable, and multi-language medical guidance powered by advanced AI.
#                     </p>
#                 </div>
#             """)
            
#             with gr.Row():
#                 with gr.Column(scale=8):
#                     chatbot_ui = gr.Chatbot(height=480, type="messages", elem_classes="chatbot")
#                     with gr.Row():
#                         chat_input = gr.Textbox(placeholder="How can I help you today?", container=False, scale=7, elem_classes="input-field")
#                         chat_submit = gr.Button("Ask MediBot", variant="primary", scale=1, elem_classes="primary-btn")
            
#             chat_submit.click(groq_chat, [chat_input, chatbot_ui, lang_dropdown], [chatbot_ui, chat_input])

#         # TAB 2: ADVANCED DIAGNOSTICS
#         with gr.TabItem("🔍 AI Diagnostics") as diag_tab:
#             with gr.Row():
#                 with gr.Column(scale=1, elem_classes="glass-panel"):
#                     diag_title = gr.Markdown("### 📸 Clinical Upload")
#                     diag_sub = gr.Markdown("Upload an image of the concern and record symptoms.")
#                     audio_input = gr.Audio(sources=["microphone"], type="filepath")
#                     image_input = gr.Image(type="filepath")
#                     analyze_btn = gr.Button("Analyze with AI Doctor", variant="primary", elem_classes="primary-btn")
                
#                 with gr.Column(scale=1, elem_classes="glass-panel"):
#                     report_title = gr.Markdown("### 🤖 Analysis Report")
#                     transcription_output = gr.Textbox(label="Transcribed Symptoms", lines=2)
#                     analysis_output = gr.Textbox(label="Medical Insight", lines=10)
#                     audio_output = gr.Audio(label="Voice Summary", autoplay=True)

#             analyze_btn.click(process_inputs, [audio_input, image_input], [transcription_output, analysis_output, audio_output])

#         # TAB 3: MAPS - Nearby Healthcare
#         with gr.TabItem("🗺️ Nearby Care") as map_tab:
#             map_title = gr.Markdown("## 🏥 Local Healthcare Facilities")
#             map_desc = gr.Markdown("Automatically finding the nearest hospitals and clinics for you.")
            
#             with gr.Row():
#                 with gr.Column(scale=2):
#                     with gr.Row():
#                         with gr.Column(scale=1):
#                             get_location_btn = gr.Button(
#                                 "📍 Get My Location",
#                                 variant="primary",
#                                 elem_classes="primary-btn"
#                             )
#                         with gr.Column(scale=1):
#                             find_hospitals_btn = gr.Button(
#                                 "✨ Find Best Care Nearby",
#                                 variant="primary",
#                                 elem_classes="primary-btn"
#                             )
                
#                 with gr.Column(scale=1):
#                     status_display = gr.Markdown("### Status: Ready")
            
#             # Hidden location inputs
#             with gr.Row(visible=False):
#                 lat_input = gr.Textbox(label="Latitude")
#                 lon_input = gr.Textbox(label="Longitude")
            
#             # Results display
#             results_html = gr.HTML(
#                 value="""
#                 <div style='text-align: center; padding: 40px 20px; color: #94a3b8; background: rgba(26, 31, 53, 0.4); border-radius: 20px; border: 2px dashed rgba(45, 212, 191, 0.2);'>
#                     <div style='font-size: 3rem; margin-bottom: 20px;'>🏥</div>
#                     <h3 style='color: #f8fafc; margin-bottom: 12px;'>Healthcare Finder</h3>
#                     <p>Click "Get My Location" to start finding nearby hospitals and clinics.</p>
#                 </div>
#                 """
#             )

#             # JavaScript to get location
#             get_location_js = """
#             async () => {
#                 return new Promise((resolve) => {
#                     if (!navigator.geolocation) {
#                         alert("Geolocation is not supported by your browser.");
#                         resolve(["", ""]);
#                         return;
#                     }
                    
#                     navigator.geolocation.getCurrentPosition(
#                         (position) => {
#                             resolve([
#                                 position.coords.latitude.toString(),
#                                 position.coords.longitude.toString()
#                             ]);
#                         },
#                         (error) => {
#                             let message = "Could not get location: ";
#                             switch(error.code) {
#                                 case 1:
#                                     message += "Permission denied. Please allow location access.";
#                                     break;
#                                 case 2:
#                                     message += "Position unavailable.";
#                                     break;
#                                 case 3:
#                                     message += "Request timed out.";
#                                     break;
#                                 default:
#                                     message += "Unknown error.";
#                             }
#                             alert(message);
#                             resolve(["", ""]);
#                         },
#                         { 
#                             enableHighAccuracy: true,
#                             timeout: 10000,
#                             maximumAge: 0
#                         }
#                     );
#                 });
#             }
#             """

#             # Function to handle hospital finding
#             def find_nearby_hospitals(lat, lon):
#                 """
#                 Use your existing get_best_hospitals function
#                 """
#                 if not lat or not lon or lat == "" or lon == "":
#                     return {
#                         "html": """
#                         <div style='text-align: center; padding: 40px; color: #f43f5e; background: rgba(244, 63, 94, 0.1); border-radius: 12px;'>
#                             <h3>❌ Location Required</h3>
#                             <p>Please get your location first.</p>
#                         </div>
#                         """,
#                         "status": "### Status: ❌ Need location"
#                     }
                
#                 try:
#                     # Use your existing get_best_hospitals function
#                     map_html, status = get_best_hospitals(lat, lon)
#                     return {
#                         "html": map_html,
#                         "status": status
#                     }
#                 except Exception as e:
#                     print(f"Error in find_nearby_hospitals: {e}")
#                     # Fallback to simple display
#                     google_maps_url = f"https://www.google.com/maps/search/hospital/@{lat},{lon},14z"
#                     return {
#                         "html": f"""
#                         <div style='text-align: center; padding: 40px;'>
#                             <h3 style='color: #2dd4bf; margin-bottom: 16px;'>📍 Your Location</h3>
#                             <div style='background: rgba(26, 31, 53, 0.85); border-radius: 12px; padding: 20px; margin-bottom: 20px;'>
#                                 <p style='color: #94a3b8; margin: 8px 0;'><strong>Latitude:</strong> {lat[:7]}</p>
#                                 <p style='color: #94a3b8; margin: 8px 0;'><strong>Longitude:</strong> {lon[:7]}</p>
#                             </div>
#                             <p style='color: #94a3b8; margin-bottom: 20px;'>Search for hospitals on Google Maps:</p>
#                             <a href='{google_maps_url}' target='_blank' 
#                                style='display: inline-block; padding: 12px 24px; background: #2dd4bf; color: white; 
#                                       border-radius: 8px; text-decoration: none; font-weight: 600;'>
#                                 🏥 Search Hospitals on Google Maps
#                             </a>
#                         </div>
#                         """,
#                         "status": "### Status: 🔍 Using Google Maps Search"
#                     }

#             # Connect button events
#             get_location_btn.click(
#                 None,
#                 None,
#                 [lat_input, lon_input],
#                 js=get_location_js
#             ).then(
#                 fn=lambda lat, lon: f"### Status: ✅ Location: {lat[:7]}, {lon[:7]}" if lat and lon else "### Status: ❌ No location",
#                 inputs=[lat_input, lon_input],
#                 outputs=status_display
#             )

#             find_hospitals_btn.click(
#                 fn=lambda: "### Status: 🔍 Searching for hospitals...",
#                 outputs=status_display
#             ).then(
#                 fn=lambda lat, lon: find_nearby_hospitals(lat, lon)["html"],
#                 inputs=[lat_input, lon_input],
#                 outputs=results_html
#             ).then(
#                 fn=lambda lat, lon: find_nearby_hospitals(lat, lon)["status"],
#                 inputs=[lat_input, lon_input],
#                 outputs=status_display
#             )
        
#         # TAB 4: ABOUT
#         with gr.TabItem("ℹ️ About") as about_tab:
#             gr.HTML("""
#                 <div style='max-width: 1000px; margin: 0 auto; padding: 40px 20px;'>
#                     <div style='text-align: center; margin-bottom: 50px;'>
#                         <h1 style='font-size: 2.8rem; font-weight: 800; color: #2dd4bf; margin-bottom: 16px;'>
#                             About MediBot
#                         </h1>
#                         <p style='font-size: 1.15rem; color: #94a3b8; line-height: 1.7; max-width: 700px; margin: 0 auto;'>
#                             An advanced AI-powered healthcare companion designed to bridge the gap between patients and quality medical information.
#                         </p>
#                     </div>

#                     <div style='margin-bottom: 50px;'>
#                         <h2 style='font-size: 2rem; font-weight: 700; color: #f8fafc; margin-bottom: 30px; text-align: center;'>
#                             Core Features
#                         </h2>
                        
#                         <div style='display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 24px;'>
#                             <div class='feature-card'>
#                                 <div class='feature-icon'>💬</div>
#                                 <h3 style='font-size: 1.3rem; color: #2dd4bf; margin-bottom: 12px;'>Intelligent Consultation</h3>
#                                 <p style='color: #94a3b8; line-height: 1.6;'>
#                                     Get instant answers to your health questions powered by advanced Large Language Models (LLMs). 
#                                     Our AI understands context and provides evidence-based medical guidance 24/7.
#                                 </p>
#                             </div>

#                             <div class='feature-card'>
#                                 <div class='feature-icon'>🔍</div>
#                                 <h3 style='font-size: 1.3rem; color: #2dd4bf; margin-bottom: 12px;'>Visual Diagnostics</h3>
#                                 <p style='color: #94a3b8; line-height: 1.6;'>
#                                     Upload medical images for preliminary AI-driven analysis. Our multimodal AI can identify potential 
#                                     skin conditions, injuries, and other visual symptoms with detailed explanations.
#                                 </p>
#                             </div>

#                             <div class='feature-card'>
#                                 <div class='feature-icon'>🎙️</div>
#                                 <h3 style='font-size: 1.3rem; color: #2dd4bf; margin-bottom: 12px;'>Voice-Enabled Interface</h3>
#                                 <p style='color: #94a3b8; line-height: 1.6;'>
#                                     Describe your symptoms naturally using voice input. MediBot transcribes and analyzes your 
#                                     description, then provides audio responses for accessibility.
#                                 </p>
#                             </div>

#                             <div class='feature-card'>
#                                 <div class='feature-icon'>🌐</div>
#                                 <h3 style='font-size: 1.3rem; color: #2dd4bf; margin-bottom: 12px;'>Multilingual Support</h3>
#                                 <p style='color: #94a3b8; line-height: 1.6;'>
#                                     Full interface and conversation support in English, Hindi (हिंदी), and Marathi (मराठी). 
#                                     The entire UI adapts to your selected language for seamless interaction.
#                                 </p>
#                             </div>

#                             <div class='feature-card'>
#                                 <div class='feature-icon'>🗺️</div>
#                                 <h3 style='font-size: 1.3rem; color: #2dd4bf; margin-bottom: 12px;'>Healthcare Locator</h3>
#                                 <p style='color: #94a3b8; line-height: 1.6;'>
#                                     Integrated map feature to find nearby hospitals, clinics, and healthcare facilities using Google Maps. 
#                                     Get immediate access to emergency care when you need it most.
#                                 </p>
#                             </div>

#                             <div class='feature-card'>
#                                 <div class='feature-icon'>🔒</div>
#                                 <h3 style='font-size: 1.3rem; color: #2dd4bf; margin-bottom: 12px;'>Privacy First</h3>
#                                 <p style='color: #94a3b8; line-height: 1.6;'>
#                                     Your health data is processed securely. We prioritize patient privacy and data protection 
#                                     in every interaction, ensuring confidential and safe consultations.
#                                 </p>
#                             </div>
#                         </div>
#                     </div>

#                     <div style='background: rgba(26, 31, 53, 0.85); border: 1px solid rgba(45, 212, 191, 0.15); border-radius: 20px; padding: 40px; margin-bottom: 40px;'>
#                         <h2 style='font-size: 1.8rem; font-weight: 700; color: #f8fafc; margin-bottom: 20px;'>
#                             How It Works
#                         </h2>
#                         <div style='color: #94a3b8; line-height: 1.8; font-size: 1.05rem;'>
#                             <p style='margin-bottom: 16px;'>
#                                 <strong style='color: #2dd4bf;'>1. Smart Consult:</strong> Ask any health-related question in natural language. 
#                                 Our AI analyzes your query and provides comprehensive, evidence-based responses.
#                             </p>
#                             <p style='margin-bottom: 16px;'>
#                                 <strong style='color: #2dd4bf;'>2. AI Diagnostics:</strong> Upload a photo of your concern (skin condition, injury, etc.) 
#                                 and optionally record your symptoms. Our multimodal AI analyzes both inputs for accurate insights.
#                             </p>
#                             <p style='margin-bottom: 16px;'>
#                                 <strong style='color: #2dd4bf;'>3. Nearby Care:</strong> Use the integrated map to locate healthcare facilities 
#                                 in your area for immediate professional consultation. Powered by Google Maps for accurate results.
#                             </p>
#                             <p>
#                                 <strong style='color: #2dd4bf;'>4. Language Selection:</strong> Switch between English, Hindi, and Marathi 
#                                 to interact in your preferred language.
#                             </p>
#                         </div>
#                     </div>

#                     <div style='background: linear-gradient(135deg, rgba(45, 212, 191, 0.1) 0%, rgba(13, 148, 136, 0.1) 100%); 
#                                 border: 2px solid rgba(45, 212, 191, 0.3); border-radius: 16px; padding: 32px; text-align: center;'>
#                         <h3 style='font-size: 1.5rem; font-weight: 700; color: #2dd4bf; margin-bottom: 12px;'>
#                             ⚠️ Important Disclaimer
#                         </h3>
#                         <p style='color: #cbd5e1; line-height: 1.7; font-size: 1.05rem;'>
#                             MediBot is an AI-powered assistant designed to provide general medical information and guidance. 
#                             It is <strong>not a substitute for professional medical advice, diagnosis, or treatment</strong>. 
#                             Always consult with qualified healthcare professionals for serious health concerns or emergencies.
#                         </p>
#                     </div>
#                 </div>
#             """)

#     footer_disclaimer = gr.HTML("""
#         <div style='text-align: center; padding: 30px 20px; color: #64748b; font-size: 0.9rem; border-top: 1px solid rgba(45, 212, 191, 0.1); margin-top: 40px;'>
#             <p style='margin: 0;'>© 2026 MediBot. Powered by Advanced AI Technology.</p>
#             <p style='margin: 8px 0 0 0;'>For emergencies, always call your local emergency services immediately.</p>
#         </div>
#     """)

#     # Language Change Event
#     def switch_language(lang):
#         t = TRANSLATIONS.get(lang, TRANSLATIONS["English"])
#         # Return updates for all UI elements in the correct order
#         return [
#             gr.update(value=f"<div style='font-size: 2rem; font-weight: 800; color: #2dd4bf; padding: 20px 15px; letter-spacing: 1px;'>{t['title']}</div>"),  # header_title
#             gr.update(label=t["diag_tab"]),  # diag_tab
#             gr.update(label=t["map_tab"]),  # map_tab
#             gr.update(label=t["about_tab"]),  # about_tab
#             gr.update(value=f"<div style='text-align: center; padding: 40px 20px;'><h1 style='font-size: 3.2rem; font-weight: 800; margin-bottom: 20px; color: #f8fafc; line-height: 1.2;'>{t['welcome']}</h1><p style='font-size: 1.15rem; color: #94a3b8; line-height: 1.7; max-width: 700px; margin: 0 auto;'>{t['sub_welcome']}</p></div>"),  # welcome_box
#             gr.update(placeholder=t["chat_placeholder"]),  # chat_input
#             gr.update(value=t["ask_btn"]),  # chat_submit
#             gr.update(value=f"### {t['upload_title']}"),  # diag_title
#             gr.update(value=t["upload_sub"]),  # diag_sub
#             gr.update(value=t["analyze_btn"]),  # analyze_btn
#             gr.update(value=f"### {t['analysis_report']}"),  # report_title
#             gr.update(label=t["transcription_label"]),  # transcription_output
#             gr.update(label=t["insight_label"]),  # analysis_output
#             gr.update(label=t["voice_summary"]),  # audio_output
#             gr.update(value=f"<div style='text-align: center; padding: 30px 20px; color: #64748b; font-size: 0.9rem; border-top: 1px solid rgba(45, 212, 191, 0.1); margin-top: 40px;'><p style='margin: 0;'>© 2026 MediBot. {t['disclaimer']}</p></div>"),  # footer_disclaimer
#             gr.update(label=t["chat_tab"]),  # chat_tab
#             gr.update(value=t["find_best_btn"])  # find_hospitals_btn
#         ]

#     lang_dropdown.change(
#         switch_language, 
#         inputs=[lang_dropdown], 
#         outputs=[header_title, diag_tab, map_tab, about_tab, welcome_box, chat_input, chat_submit, diag_title, diag_sub, analyze_btn, report_title, transcription_output, analysis_output, audio_output, footer_disclaimer, chat_tab, find_hospitals_btn]
#     )

# demo.launch(debug=True, show_api=False, favicon_path="favicon.svg")
# if you dont use pipenv uncomment the following:
# # if you dont use pipenv uncomment the following:
# from dotenv import load_dotenv
# load_dotenv()

# # if you dont use pipenv uncomment the following:
# from dotenv import load_dotenv
# load_dotenv()

import os
import gradio as gr
import requests
import json
import re
from groq import Groq
from dotenv import load_dotenv

# Import isolated nearby care service
from nearby_care import find_hospitals_nearby

# Load environment variables
load_dotenv()

from brain_of_the_doctor import encode_image, analyze_image_with_query
from voice_of_the_patient import record_audio, transcribe_with_groq
from voice_of_the_doctor import text_to_speech_with_gtts, text_to_speech_with_elevenlabs

# --- Configuration ---
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
GOOGLE_MAPS_API_KEY = os.environ.get("GOOGLE_MAPS_API_KEY", "AIzaSyAmDAgwmjuvNNOv1K7d1UF7SbMlDAsAmXs")
client = Groq(api_key=GROQ_API_KEY)

print(f"Starting MediBot with Google Maps API...")
print(f"API Key (first 10 chars): {GOOGLE_MAPS_API_KEY[:10]}...")

# --- Translations ---
TRANSLATIONS = {
    "English": {
        "title": "MEDIBOT",
        "chat_tab": "💬 Smart Consult",
        "diag_tab": "🔍 AI Diagnostics",
        "map_tab": "🗺️ Nearby Care",
        "about_tab": "ℹ️ About",
        "welcome": "Your Health. Our Intelligence.",
        "sub_welcome": "Empowering patients with instant, reliable, and multi-language medical guidance.",
        "chat_placeholder": "How can I help you today?",
        "ask_btn": "Ask MediBot",
        "emergency_btn": "🚨 Find Nearby Hospitals",
        "upload_title": "📸 Clinical Upload",
        "upload_sub": "Upload an image of the concern and record symptoms.",
        "analyze_btn": "Analyze with AI Doctor",
        "analysis_report": "🤖 Analysis Report",
        "transcription_label": "Transcribed Symptoms",
        "insight_label": "Medical Insight",
        "voice_summary": "Voice Summary",
        "disclaimer": "Disclaimer: MediBot is an AI assistant, not a licensed doctor. Always seek professional help for critical health issues.",
        "map_title": "Local Healthcare Facilities",
        "map_desc": "Find nearby hospitals using Google Maps.",
        "find_best_btn": "📍 Get My Location",
        "fetching_msg": "🔍 Searching hospitals...",
    },
    "Hindi": {
        "title": "मेडिबॉट",
        "chat_tab": "💬 स्मार्ट चैट",
        "diag_tab": "🔍 एआई निदान",
        "map_tab": "🗺️ पास के अस्पताल",
        "about_tab": "ℹ️ जानकारी",
        "welcome": "आपका स्वास्थ्य। हमारी बुद्धिमत्ता।",
        "sub_welcome": "मरीजों को तत्काल, विश्वसनीय और बहुभाषी चिकित्सा मार्गदर्शन के साथ सशक्त बनाना।",
        "chat_placeholder": "मैं आज आपकी कैसे मदद कर सकता हूँ?",
        "ask_btn": "मेडिबॉट से पूछें",
        "emergency_btn": "🚨 पास के अस्पताल खोजें",
        "upload_title": "📸 क्लिनिकल अपलोड",
        "upload_sub": "चिंता वाले क्षेत्र की छवि अपलोड करें और लक्षण रिकॉर्ड करें।",
        "analyze_btn": "एआई डॉक्टर के साथ विश्लेषण करें",
        "analysis_report": "🤖 विश्लेषण रिपोर्ट",
        "transcription_label": "श्रुतलेख लक्षण",
        "insight_label": "चिकित्सा अंतर्दृष्टि",
        "voice_summary": "आवाज़ सारांश",
        "disclaimer": "अस्वीकरण: मेडिबॉट एक एआई सहायक है, लाइसेंस प्राप्त डॉक्टर नहीं। गंभीर स्वास्थ्य समस्याओं के लिए हमेशा पेशेवर मदद लें।",
        "map_title": "स्थानीय स्वास्थ्य सुविधाएं",
        "map_desc": "Google Maps का उपयोग करके पास के अस्पताल खोजें।",
        "find_best_btn": "📍 मेरा स्थान प्राप्त करें",
        "fetching_msg": "🔍 अस्पताल खोज रहे हैं...",
    },
    "Marathi": {
        "title": "मेडिबॉट",
        "chat_tab": "💬 स्मार्ट चॅट",
        "diag_tab": "🔍 एआय निदान",
        "map_tab": "🗺️ जवळची रुग्णालये",
        "about_tab": "ℹ️ माहिती",
        "welcome": "तुमचे आरोग्य. आमची बुद्धिमत्ता।",
        "sub_welcome": "रुग्णांना त्वरित, विश्वसनीय आणि बहुभाषिक वैद्यकीय मार्गदर्शनासह सक्षम करणे।",
        "chat_placeholder": "मी तुम्हाला आज कशी मदत करू शकतो?",
        "ask_btn": "मेडिबॉटला विचारा",
        "emergency_btn": "🚨 जवळची रुग्णालये शोधा",
        "upload_title": "📸 क्लिनिकल अपलोड",
        "upload_sub": "तपासणीसाठी फोटो अपलोड करा और लक्षणे सांगा।",
        "analyze_btn": "एआय डॉक्टरांसह विश्लेषण करा",
        "analysis_report": "🤖 विश्लेषण अहवाल",
        "transcription_label": "लक्षणे",
        "insight_label": "वैद्यकीय माहिती",
        "voice_summary": "ध्वनी सारांश",
        "disclaimer": "डिस्क्लेमर: मेडिबॉट हा एआय असिस्टंट आहे, डॉक्टर नाही। गंभीर आरोग्य समस्यांसाठी नेहमी डॉक्टरांचा सल्ला घ्या।",
        "map_title": "स्थानिक आरोग्य सुविधा",
        "map_desc": "Google Maps वापरून जवळची रुग्णालये शोधा।",
        "find_best_btn": "📍 माझे स्थान मिळवा",
        "fetching_msg": "🔍 रुग्णालये शोधत आहे...",
    }
}

def groq_chat(message, history, language):
    """
    Chat with Groq (Llama-3.3-70b) with Medical Persona
    """
    if not message:
        return history + [{"role": "assistant", "content": ""}]
    
    lang_map = {
        "Hindi": "Respond primarily in Hindi (हिंदी). Use Devnagari script.",
        "Marathi": "Respond primarily in Marathi (मराठी). Use Devnagari script.",
        "English": "Respond in English."
    }
    lang_instruction = lang_map.get(language, "Respond in English.")
    
    system_instruction = (
        f"You are MediBot, a professional AI medical assistant. "
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

def process_inputs(audio_filepath, image_filepath):
    system_prompt="""You have to act as a professional doctor. Use the image provided to identify if there is any medical condition."""
    if not audio_filepath and not image_filepath:
         return "No input.", "No input.", None

    speech_to_text_output = ""
    if audio_filepath:
        try:
            speech_to_text_output = transcribe_with_groq(GROQ_API_KEY=GROQ_API_KEY, 
                                                         audio_filepath=audio_filepath,
                                                         stt_model="whisper-large-v3")
        except: speech_to_text_output = "Transcription failed."
    
    if image_filepath:
        query_text = system_prompt + (" " + speech_to_text_output if speech_to_text_output else "")
        try:
            doctor_response = analyze_image_with_query(query=query_text, encoded_image=encode_image(image_filepath), model="meta-llama/llama-4-scout-17b-16e-instruct") 
        except Exception as e:
            doctor_response = f"Analysis Error: {str(e)}"
    else:
        doctor_response = "I need an image for diagnosis."

    output_audio_path = "final.mp3"
    cleaned_response = re.sub(r'[*#_`~]', '', doctor_response) if doctor_response else ""
    try:
        text_to_speech_with_elevenlabs(input_text=cleaned_response, output_filepath=output_audio_path)
    except:
        text_to_speech_with_gtts(input_text=cleaned_response, output_filepath=output_audio_path)
    return speech_to_text_output, doctor_response, output_audio_path

# --- UI CSS ---
custom_css = """
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap');

:root { 
    --primary: #2dd4bf; 
    --primary-dark: #0d9488; 
    --primary-light: #5eead4;
    --bg-dark: #0a0f1e; 
    --bg-card: #1a1f35;
    --card-bg: rgba(26, 31, 53, 0.85);
    --text-primary: #f8fafc;
    --text-secondary: #94a3b8;
    --text-muted: #64748b;
    --border: rgba(45, 212, 191, 0.15);
    --shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.4);
}

* {
    font-family: 'Poppins', -apple-system, BlinkMacSystemFont, sans-serif !important;
}

body, .gradio-container { 
    background: linear-gradient(135deg, var(--bg-dark) 0%, #0f1729 100%) !important;
    color: var(--text-primary) !important;
    min-height: 100vh;
}

.glass-panel { 
    background: var(--card-bg);
    backdrop-filter: blur(16px) saturate(180%);
    -webkit-backdrop-filter: blur(16px) saturate(180%);
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 32px;
    box-shadow: var(--shadow);
}

.primary-btn { 
    background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    font-weight: 600 !important;
    padding: 12px 28px !important;
    font-size: 15px !important;
    cursor: pointer;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    box-shadow: 0 4px 12px rgba(45, 212, 191, 0.25) !important;
}

.primary-btn:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 24px rgba(45, 212, 191, 0.4) !important;
}

.tab-nav button.selected {
    color: var(--primary) !important;
    border-bottom: 3px solid var(--primary) !important;
}

.chatbot {
    border-radius: 16px !important;
    border: 1px solid var(--border) !important;
    background: var(--bg-card) !important;
}

input, textarea, .input-field {
    background: rgba(255, 255, 255, 0.05) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    color: var(--text-primary) !important;
    padding: 12px 16px !important;
}

footer { 
    display: none !important; 
}
"""

# --- App Layout ---

with gr.Blocks(css=custom_css, title="MediBot - AI Healthcare Assistant") as demo:
    # Hidden inputs for location (accessible globally)
    lat_input = gr.Textbox(visible=False)
    lon_input = gr.Textbox(visible=False)
    
    with gr.Row(variant="compact"):
        with gr.Column(scale=4):
            header_title = gr.HTML("<div style='font-size: 2rem; font-weight: 800; color: #2dd4bf; padding: 20px 15px; letter-spacing: 1px;'>MEDIBOT</div>")
        with gr.Column(scale=1):
            lang_dropdown = gr.Dropdown(choices=["English", "Hindi", "Marathi"], value="English", label="Select Language", container=False)
    
    with gr.Tabs() as tabs_container:
        
        # TAB 1: SMART CHAT
        with gr.TabItem("💬 Smart Consult") as chat_tab:
            welcome_box = gr.HTML("""
                <div style='text-align: center; padding: 40px 20px;'>
                    <h1 style='font-size: 3.2rem; font-weight: 800; margin-bottom: 20px; color: #f8fafc; line-height: 1.2;'>
                        Your Health. Our Intelligence.
                    </h1>
                    <p style='font-size: 1.15rem; color: #94a3b8; line-height: 1.7; max-width: 700px; margin: 0 auto;'>
                        Empowering patients with instant, reliable, and multi-language medical guidance powered by advanced AI.
                    </p>
                </div>
            """)
            
            with gr.Row():
                with gr.Column(scale=8):
                    chatbot_ui = gr.Chatbot(height=480, type="messages", elem_classes="chatbot")
                    with gr.Row():
                        chat_input = gr.Textbox(placeholder="How can I help you today?", container=False, scale=7, elem_classes="input-field")
                        chat_submit = gr.Button("Ask MediBot", variant="primary", scale=1, elem_classes="primary-btn")
            
            chat_submit.click(groq_chat, [chat_input, chatbot_ui, lang_dropdown], [chatbot_ui, chat_input])

        # TAB 2: ADVANCED DIAGNOSTICS
        with gr.TabItem("🔍 AI Diagnostics") as diag_tab:
            with gr.Row():
                with gr.Column(scale=1, elem_classes="glass-panel"):
                    diag_title = gr.Markdown("### 📸 Clinical Upload")
                    diag_sub = gr.Markdown("Upload an image of the concern and record symptoms.")
                    audio_input = gr.Audio(sources=["microphone"], type="filepath")
                    image_input = gr.Image(type="filepath")
                    analyze_btn = gr.Button("Analyze with AI Doctor", variant="primary", elem_classes="primary-btn")
                
                with gr.Column(scale=1, elem_classes="glass-panel"):
                    report_title = gr.Markdown("### 🤖 Analysis Report")
                    transcription_output = gr.Textbox(label="Transcribed Symptoms", lines=2)
                    analysis_output = gr.Textbox(label="Medical Insight", lines=10)
                    audio_output = gr.Audio(label="Voice Summary", autoplay=True)

            analyze_btn.click(process_inputs, [audio_input, image_input], [transcription_output, analysis_output, audio_output])

        # TAB 3: GOOGLE MAPS WITH API - SIMPLIFIED
        with gr.TabItem("🗺️ Nearby Care") as map_tab:
            gr.Markdown("## 🏥 Hospital Finder")
            
            with gr.Row(elem_classes="glass-panel"):
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
            map_display = gr.HTML("""
                <div style='text-align: center; padding: 40px 20px; color: #94a3b8; 
                            background: rgba(26, 31, 53, 0.4); border-radius: 20px; 
                            border: 2px dashed rgba(45, 212, 191, 0.2);'>
                    <div style='font-size: 3rem; margin-bottom: 20px;'>🗺️</div>
                    <h3 style='color: #f8fafc; margin-bottom: 12px;'>Hospital Finder</h3>
                    <p>Enter a city or area above to see nearby hospitals and their contact info.</p>
                </div>
            """)
            
            # Hospitals list display area
            hospitals_display = gr.HTML()
            
            def find_care_flow(query):
                if not query or len(query.strip()) < 3:
                    return gr.update(), gr.update(value="<div class='glass-panel'>❌ Please enter a valid location (at least 3 characters).</div>"), "### Status: ❌ Invalid location"
                
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
        with gr.TabItem("ℹ️ About") as about_tab:
            gr.HTML("""
                <div style='max-width: 1000px; margin: 0 auto; padding: 40px 20px;'>
                    <div style='text-align: center; margin-bottom: 50px;'>
                        <h1 style='font-size: 2.8rem; font-weight: 800; color: #2dd4bf; margin-bottom: 16px;'>
                            About MediBot
                        </h1>
                        <p style='font-size: 1.15rem; color: #94a3b8; line-height: 1.7; max-width: 700px; margin: 0 auto;'>
                            An advanced AI-powered healthcare companion.
                        </p>
                    </div>

                    <div style='background: rgba(45, 212, 191, 0.1); border-radius: 16px; padding: 32px; text-align: center;'>
                        <h3 style='font-size: 1.5rem; font-weight: 700; color: #2dd4bf; margin-bottom: 12px;'>
                            ⚠️ Important Disclaimer
                        </h3>
                        <p style='color: #cbd5e1; line-height: 1.7; font-size: 1.05rem;'>
                            MediBot is an AI-powered assistant for general medical information. 
                            It is <strong>not a substitute for professional medical advice</strong>. 
                            Always consult with qualified healthcare professionals.
                        </p>
                    </div>
                </div>
            """)

    footer_disclaimer = gr.HTML("""
        <div style='text-align: center; padding: 30px 20px; color: #64748b; font-size: 0.9rem; border-top: 1px solid rgba(45, 212, 191, 0.1); margin-top: 40px;'>
            <p style='margin: 0;'>© 2026 MediBot. Powered by Advanced AI & Google Maps.</p>
        </div>
    """)

    # Language Change Event
    def switch_language(lang):
        t = TRANSLATIONS.get(lang, TRANSLATIONS["English"])
        return [
            gr.update(value=f"<div style='font-size: 2rem; font-weight: 800; color: #2dd4bf; padding: 20px 15px; letter-spacing: 1px;'>{t['title']}</div>"),
            gr.update(label=t["diag_tab"]),
            gr.update(label=t["map_tab"]),
            gr.update(label=t["about_tab"]),
            gr.update(value=f"<div style='text-align: center; padding: 40px 20px;'><h1 style='font-size: 3.2rem; font-weight: 800; margin-bottom: 20px; color: #f8fafc; line-height: 1.2;'>{t['welcome']}</h1><p style='font-size: 1.15rem; color: #94a3b8; line-height: 1.7; max-width: 700px; margin: 0 auto;'>{t['sub_welcome']}</p></div>"),
            gr.update(placeholder=t["chat_placeholder"]),
            gr.update(value=t["ask_btn"]),
            gr.update(value=f"### {t['upload_title']}"),
            gr.update(value=t["upload_sub"]),
            gr.update(value=t["analyze_btn"]),
            gr.update(value=f"### {t['analysis_report']}"),
            gr.update(label=t["transcription_label"]),
            gr.update(label=t["insight_label"]),
            gr.update(label=t["voice_summary"]),
            gr.update(value=f"<div style='text-align: center; padding: 30px 20px; color: #64748b; font-size: 0.9rem; border-top: 1px solid rgba(45, 212, 191, 0.1); margin-top: 40px;'><p style='margin: 0;'>© 2026 MediBot. {t['disclaimer']}</p></div>"),
            gr.update(label=t["chat_tab"])
        ]

    lang_dropdown.change(
        switch_language, 
        inputs=[lang_dropdown], 
        outputs=[header_title, diag_tab, map_tab, about_tab, welcome_box, chat_input, chat_submit, diag_title, diag_sub, analyze_btn, report_title, transcription_output, analysis_output, audio_output, footer_disclaimer, chat_tab]
    )

demo.launch(debug=True, show_api=False, share=False, favicon_path="favicon.svg")