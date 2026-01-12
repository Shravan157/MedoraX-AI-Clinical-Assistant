
import os
import requests
import folium
from folium import plugins
from geopy.distance import geodesic
import html
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
GOOGLE_MAPS_API_KEY = os.environ.get("GOOGLE_MAPS_API_KEY", "AIzaSyAmDAgwmjuvNNOv1K7d1UF7SbMlDAsAmXs")
if GOOGLE_MAPS_API_KEY == "AIzaSyAmDAgwmjuvNNOv1K7d1UF7SbMlDAsAmXs":
    print("⚠️ Warning: Using default Google Maps API Key. Please set GOOGLE_MAPS_API_KEY environment variable.")
else:
    print(f"✅ Nearby Care Service using API Key: {GOOGLE_MAPS_API_KEY[:10]}...")

def geocode_address(address):
    """Convert an address string to coordinates using Google Geocoding API"""
    try:
        url = "https://maps.googleapis.com/maps/api/geocode/json"
        params = {"address": address, "key": GOOGLE_MAPS_API_KEY}
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        if data.get("status") == "OK":
            loc = data["results"][0]["geometry"]["location"]
            return loc["lat"], loc["lng"]
        return None, None
    except Exception as e:
        print(f"Error geocoding address '{address}': {e}")
        return None, None

def get_location_from_ip():
    """Fallback to IP-based location if GPS is unavailable"""
    try:
        # Using a reliable IP geolocation service
        response = requests.get("https://ipapi.co/json/", timeout=5)
        data = response.json()
        print(f"DEBUG: IP Location obtained: {data.get('latitude')}, {data.get('longitude')}")
        return data.get("latitude"), data.get("longitude")
    except Exception as e:
        print(f"Error getting IP location: {e}")
        return None, None

def get_hospitals_from_google(lat, lon, radius_km=10):
    """
    Fetch hospitals from Google Maps Places API with detailed information
    """
    try:
        lat, lon = float(lat), float(lon)
        url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
        
        params = {
            'location': f'{lat},{lon}',
            'radius': radius_km * 1000,
            'type': 'hospital',
            'keyword': 'hospital clinic medical emergency',
            'key': GOOGLE_MAPS_API_KEY
        }
        
        response = requests.get(url, params=params, timeout=15)
        data = response.json()
        
        if data.get('status') not in ['OK', 'ZERO_RESULTS']:
            print(f"Google Maps API Error: {data.get('status')} - {data.get('error_message', '')}")
            return []
            
        def get_phone(place_id):
            try:
                detail_url = "https://maps.googleapis.com/maps/api/place/details/json"
                detail_params = {
                    'place_id': place_id,
                    'fields': 'formatted_phone_number',
                    'key': GOOGLE_MAPS_API_KEY
                }
                res = requests.get(detail_url, params=detail_params, timeout=5).json()
                return res.get('result', {}).get('formatted_phone_number', 'Not available')
            except:
                return 'Not available'

        hospitals = []
        user_loc = (lat, lon)
        
        # Process all results (Google typically returns 20 per request)
        for place in data.get('results', []):
            p_lat = place['geometry']['location']['lat']
            p_lon = place['geometry']['location']['lng']
            p_loc = (p_lat, p_lon)
            
            # Calculate real distance
            dist = geodesic(user_loc, p_loc).kilometers
            pid = place.get('place_id', '')
            
            hospitals.append({
                'name': place.get('name', 'Healthcare Facility'),
                'lat': p_lat,
                'lon': p_lon,
                'address': place.get('vicinity', 'Address not available'),
                'rating': place.get('rating', 'N/A'),
                'user_ratings_total': place.get('user_ratings_total', 0),
                'distance': round(dist, 1), # Rounded to 1 decimal for better readability
                'place_id': pid,
                'open_now': place.get('opening_hours', {}).get('open_now', None),
                'phone': get_phone(pid)
            })
                
        return sorted(hospitals, key=lambda x: x['distance'])
    except Exception as e:
        print(f"Error fetching hospitals: {e}")
        return []

def create_folium_map(lat, lon, hospitals, address=None):
    """
    Create an interactive Folium map
    """
    try:
        lat, lon = float(lat), float(lon)
        m = folium.Map(
            location=[lat, lon],
            zoom_start=14,
            tiles='OpenStreetMap',
            control_scale=True
        )
        
        # Search Reference Marker
        folium.CircleMarker(
            location=[lat, lon],
            radius=12,
            popup=f'📍 <b>Hospitals being searched around:</b><br>{address if address else "General Area"}',
            color='#1d4ed8', # Strong Blue
            fill=True,
            fillColor='#3b82f6',
            fillOpacity=0.6,
            weight=3
        ).add_to(m)
        
        # Hospital Markers
        for idx, h in enumerate(hospitals, 1):
            status_color = "green" if h['open_now'] is True else ("red" if h['open_now'] is False else "gray")
            status_text = "Open Now" if h['open_now'] is True else ("Closed" if h['open_now'] is False else "Hours Unknown")
            
            popup_html = f"""
            <div style='font-family: Poppins, sans-serif; min-width: 200px;'>
                <h4 style='margin:0 0 5px 0; color:#0d9488;'>🏥 {h['name']}</h4>
                <p style='margin:2px 0; font-size:0.85rem;'><b>Dist:</b> {h['distance']} km</p>
                <p style='margin:2px 0; font-size:0.85rem;'><b>Rating:</b> ⭐ {h['rating']} ({h['user_ratings_total']})</p>
                <p style='margin:2px 0; font-size:0.85rem; color:{status_color}; text-shadow: 0 0 1px silver;'>● {status_text}</p>
                <p style='margin:2px 0; font-size:0.85rem;'><b>📞:</b> <a href='tel:{h['phone']}' style='color:#2dd4bf; text-decoration:none;'>{h['phone']}</a></p>
                <p style='margin:5px 0; font-size:0.8rem; color:#666;'>{h['address']}</p>
                <a href='https://www.google.com/maps/dir/?api=1&destination={h['lat']},{h['lon']}' 
                   target='_blank' style='display:inline-block; margin-top:5px; color:#2dd4bf; text-decoration:none; font-weight:600;'>
                   Get Directions →
                </a>
            </div>
            """
            
            folium.Marker(
                location=[h['lat'], h['lon']],
                popup=folium.Popup(popup_html, max_width=300),
                icon=folium.Icon(color='red', icon='plus-square', prefix='fa'),
                tooltip=f"{h['name']} ({h['distance']} km)"
            ).add_to(m)
            
        plugins.Fullscreen().add_to(m)
        return m._repr_html_(), lat, lon
    except Exception as e:
        print(f"Error creating map: {e}")
        return None

def find_hospitals_nearby(lat=None, lon=None, address=None):
    """
    Main integrated function for finding hospitals by GPS or Address
    """
    if address:
        print(f"DEBUG: Geocoding address: {address}")
        lat, lon = geocode_address(address)
    
    if not lat or not lon:
        print("DEBUG: GPS missing, trying IP location...")
        lat, lon = get_location_from_ip()
    
    if not lat or not lon:
        return "<div class='glass-panel' style='text-align:center;'>❌ Location required. Please click GPS button OR enter a city manually.</div>", "", "### Status: ❌ No location"
        
    try:
        hospitals = get_hospitals_from_google(lat, lon)
        
        if not hospitals:
            return (
                "<div class='glass-panel' style='text-align:center;'><h3>No hospitals found nearby.</h3><p>Try increasing the search area or checking your connection.</p></div>",
                "",
                "### Status: ⚠️ No results"
            )
            
        map_html, center_lat, center_lon = create_folium_map(lat, lon, hospitals, address)
        
        import html
        map_iframe = f"""
        <div style='border-radius:20px; overflow:hidden; box-shadow:0 12px 48px rgba(0,0,0,0.3); border:1px solid rgba(45,212,191,0.2);'>
            <iframe srcdoc="{html.escape(map_html)}" width="100%" height="500px" style="border:none;"></iframe>
        </div>
        <p style='font-size:0.8rem; color:#94a3b8; text-align:center; margin-top:10px;'>
            📏 Distances shown are aerial (straight-line) from <b>{address if address else "your location"}</b>.
        </p>
        """
        
        cards_html = "<div style='display:grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap:20px; margin-top:30px;'>"
        for idx, h in enumerate(hospitals, 1):
            cards_html += f"""
            <div class='glass-panel' style='padding:20px; transition:all 0.3s ease;'>
                <div style='display:flex; justify-content:space-between; align-items:start;'>
                    <h3 style='margin:0; color:#2dd4bf; font-size:1.1rem;'>{idx}. {h['name']}</h3>
                    <span style='background:rgba(45,212,191,0.1); color:#2dd4bf; padding:4px 12px; border-radius:20px; font-size:0.8rem; font-weight:700;'>{h['distance']} km</span>
                </div>
                <p style='color:#94a3b8; font-size:0.9rem; margin:10px 0;'>📍 {h['address']}</p>
                <p style='color:#2dd4bf; font-size:0.95rem; margin:10px 0; font-weight:600;'>📞 {h['phone']}</p>
                <div style='display:flex; justify-content:space-between; align-items:center; margin-top:15px;'>
                    <span style='color:#f59e0b; font-weight:600;'>⭐ {h['rating']}</span>
                    <div style='display:flex; gap:15px;'>
                        <a href='tel:{h['phone']}' 
                           style='color:#2dd4bf; text-decoration:none; font-weight:700; font-size:0.9rem; background:rgba(45,212,191,0.1); padding:6px 12px; border-radius:8px;'>
                           📞 Call
                        </a>
                        <a href='https://www.google.com/maps/dir/?api=1&destination={h['lat']},{h['lon']}' 
                           target='_blank' style='color:#2dd4bf; text-decoration:none; font-weight:700; font-size:0.9rem; padding:6px 0;'>
                           Directions →
                        </a>
                    </div>
                </div>
            </div>
            """
        cards_html += "</div>"
        
        return map_iframe, cards_html, f"### Status: ✅ Found {len(hospitals)} hospitals near you"
        
    except Exception as e:
        print(f"Critical error: {e}")
        return f"<div class='glass-panel'>Error: {str(e)}</div>", "", "### Status: ❌ Error occurred"
