import os
import requests
import folium
from folium import plugins
from geopy.distance import geodesic
import html
from dotenv import load_dotenv
from typing import Optional, Tuple, List, Dict
import time

# Load environment variables
load_dotenv()

# Configuration
GOOGLE_MAPS_API_KEY = os.environ.get("GOOGLE_MAPS_API_KEY", "AIzaSyAmDAgwmjuvNNOv1K7d1UF7SbMlDAsAmXs")
if GOOGLE_MAPS_API_KEY == "AIzaSyAmDAgwmjuvNNOv1K7d1UF7SbMlDAsAmXs":
    print("⚠️ Warning: Using default Google Maps API Key. Please set GOOGLE_MAPS_API_KEY environment variable.")
else:
    print(f"✅ Nearby Care Service using API Key: {GOOGLE_MAPS_API_KEY[:10]}...")

# Cache for place details to avoid redundant API calls
_place_details_cache = {}

# Air Quality API function
def get_air_quality(lat: float, lon: float) -> Optional[Dict]:
    """
    Fetch air quality data from Google Air Quality API
    Returns AQI, category, and health recommendations
    """
    try:
        url = "https://airquality.googleapis.com/v1/currentConditions:lookup"
        
        payload = {
            "location": {
                "latitude": lat,
                "longitude": lon
            },
            "extraComputations": [
                "HEALTH_RECOMMENDATIONS",
                "LOCAL_AQI"
            ],
            "languageCode": "en"
        }
        
        headers = {
            "Content-Type": "application/json"
        }
        
        params = {"key": GOOGLE_MAPS_API_KEY}
        
        response = requests.post(url, json=payload, headers=headers, params=params, timeout=8)
        response.raise_for_status()
        data = response.json()
        
        if 'indexes' in data and data['indexes']:
            aqi_data = data['indexes'][0]
            result = {
                'aqi': aqi_data.get('aqi', 'N/A'),
                'category': aqi_data.get('category', 'Unknown'),
                'color': aqi_data.get('color', {}).get('red', 0),
                'health_recommendations': data.get('healthRecommendations', {}).get('generalPopulation', '')
            }
            print(f"✅ Air quality data fetched: AQI {result['aqi']} - {result['category']}")
            return result
        return None
        
    except requests.RequestException as e:
        print(f"⚠️ Network error fetching air quality: {e}")
        return None
    except Exception as e:
        print(f"⚠️ Error fetching air quality data: {e}")
        return None

def get_aqi_color(aqi: int) -> Tuple[str, str]:
    """
    Get color code and label based on AQI value (US EPA AQI Scale)
    """
    if aqi <= 50:
        return "#00e400", "Good"
    elif aqi <= 100:
        return "#ffff00", "Moderate"
    elif aqi <= 150:
        return "#ff7e00", "Unhealthy for Sensitive Groups"
    elif aqi <= 200:
        return "#ff0000", "Unhealthy"
    elif aqi <= 300:
        return "#8f3f97", "Very Unhealthy"
    else:
        return "#7e0023", "Hazardous"

def create_air_quality_display(air_quality: Dict) -> str:
    """
    Create a simple air quality display for the UI
    """
    if not air_quality:
        return ""
    
    aqi = air_quality.get('aqi', 'N/A')
    category = air_quality.get('category', 'Unknown')
    color, label = get_aqi_color(aqi if isinstance(aqi, int) else 0)
    recommendation = air_quality.get('health_recommendations', '')
    
    return f"""
    <div style='background: linear-gradient(135deg, {color}20, {color}40); 
                border: 2px solid {color}; 
                border-radius: 12px; 
                padding: 15px; 
                margin-bottom: 20px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.1);'>
        <div style='display: flex; justify-content: space-between; align-items: center;'>
            <div>
                <h3 style='margin: 0 0 5px 0; color:#2dd4bf; font-size: 1.1rem;'>🌍 Air Quality Index</h3>
                <div style='display: flex; align-items: baseline; gap: 10px;'>
                    <div style='font-size: 2.5rem; font-weight: 700; color:{color};'>{aqi}</div>
                    <div>
                        <div style='font-size: 1.1rem; font-weight: 600; color:{color};'>{category}</div>
                        <div style='color: #64748b; font-size: 0.9rem;'>{label}</div>
                    </div>
                </div>
            </div>
            <div style='width: 40px; height: 40px; border-radius: 50%; background: {color};'></div>
        </div>
        {f'<p style="color: #64748b; font-size: 0.9rem; margin-top: 10px; margin-bottom: 0;">{html.escape(recommendation)}</p>' if recommendation else ''}
    </div>
    """

def geocode_address(address: str) -> Tuple[Optional[float], Optional[float]]:
    """
    Convert an address string to coordinates using Google Geocoding API
    Enhanced with better error handling and result validation
    """
    if not address or not address.strip():
        return None, None
    
    try:
        url = "https://maps.googleapis.com/maps/api/geocode/json"
        params = {
            "address": address.strip(),
            "key": GOOGLE_MAPS_API_KEY
        }
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if data.get("status") == "OK" and data.get("results"):
            loc = data["results"][0]["geometry"]["location"]
            lat, lng = loc["lat"], loc["lng"]
            print(f"✅ Geocoded '{address}' to: ({lat}, {lng})")
            return lat, lng
        else:
            print(f"⚠️ Geocoding failed for '{address}': {data.get('status')}")
            return None, None
    except requests.RequestException as e:
        print(f"❌ Network error geocoding address '{address}': {e}")
        return None, None
    except Exception as e:
        print(f"❌ Error geocoding address '{address}': {e}")
        return None, None

def get_location_from_ip() -> Tuple[Optional[float], Optional[float]]:
    """
    Fallback to IP-based location with multiple services for reliability
    """
    services = [
        ("https://ipapi.co/json/", lambda d: (d.get("latitude"), d.get("longitude"))),
        ("https://ipwho.is/", lambda d: (d.get("latitude"), d.get("longitude"))),
        ("http://ip-api.com/json/", lambda d: (d.get("lat"), d.get("lon")))
    ]
    
    for service_url, extractor in services:
        try:
            response = requests.get(service_url, timeout=5)
            response.raise_for_status()
            data = response.json()
            lat, lon = extractor(data)
            
            if lat and lon:
                print(f"✅ IP Location obtained from {service_url}: ({lat}, {lon})")
                return float(lat), float(lon)
        except Exception as e:
            print(f"⚠️ Failed to get location from {service_url}: {e}")
            continue
    
    print("❌ All IP geolocation services failed")
    return None, None

def get_place_details_batch(place_ids: List[str]) -> Dict[str, Dict]:
    """
    Fetch place details for multiple places efficiently with caching
    """
    results = {}
    uncached_ids = [pid for pid in place_ids if pid not in _place_details_cache]
    
    # Return cached results immediately
    for pid in place_ids:
        if pid in _place_details_cache:
            results[pid] = _place_details_cache[pid]
    
    # Fetch uncached details
    detail_url = "https://maps.googleapis.com/maps/api/place/details/json"
    
    for place_id in uncached_ids:
        try:
            params = {
                'place_id': place_id,
                'fields': 'formatted_phone_number,international_phone_number,website,opening_hours',
                'key': GOOGLE_MAPS_API_KEY
            }
            response = requests.get(detail_url, params=params, timeout=5)
            response.raise_for_status()
            data = response.json()
            
            if data.get('status') == 'OK':
                result = data.get('result', {})
                details = {
                    'phone': result.get('formatted_phone_number') or result.get('international_phone_number', 'Not available'),
                    'website': result.get('website', None),
                    'opening_hours': result.get('opening_hours', {})
                }
                _place_details_cache[place_id] = details
                results[place_id] = details
            else:
                results[place_id] = {'phone': 'Not available', 'website': None, 'opening_hours': {}}
            
            # Small delay to avoid rate limiting
            time.sleep(0.1)
        except Exception as e:
            print(f"⚠️ Error fetching details for place {place_id}: {e}")
            results[place_id] = {'phone': 'Not available', 'website': None, 'opening_hours': {}}
    
    return results

def get_hospitals_from_google(lat: float, lon: float, radius_km: float = 10) -> List[Dict]:
    """
    Fetch hospitals from Google Maps Places API with detailed information
    Enhanced with pagination support and better filtering
    """
    try:
        lat, lon = float(lat), float(lon)
        url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
        
        params = {
            'location': f'{lat},{lon}',
            'radius': radius_km * 1000,
            'type': 'hospital',
            'key': GOOGLE_MAPS_API_KEY
        }
        
        all_results = []
        next_page_token = None
        
        # Fetch up to 60 results (3 pages of 20 each)
        for page in range(3):
            if page > 0:
                if not next_page_token:
                    break
                params['pagetoken'] = next_page_token
                # Google requires a short delay between paginated requests
                time.sleep(2)
            
            response = requests.get(url, params=params, timeout=15)
            response.raise_for_status()
            data = response.json()
            
            if data.get('status') not in ['OK', 'ZERO_RESULTS']:
                print(f"⚠️ Google Maps API Error: {data.get('status')} - {data.get('error_message', '')}")
                if page == 0:
                    return []
                break
            
            all_results.extend(data.get('results', []))
            next_page_token = data.get('next_page_token')
            
            if not next_page_token:
                break
        
        print(f"✅ Found {len(all_results)} hospitals from Google Maps API")
        
        # Extract place IDs for batch detail fetching
        place_ids = [place.get('place_id') for place in all_results if place.get('place_id')]
        place_details = get_place_details_batch(place_ids)
        
        hospitals = []
        user_loc = (lat, lon)
        
        for place in all_results:
            p_lat = place['geometry']['location']['lat']
            p_lon = place['geometry']['location']['lng']
            p_loc = (p_lat, p_lon)
            
            # Calculate real distance
            dist = geodesic(user_loc, p_loc).kilometers
            pid = place.get('place_id', '')
            
            # Get detailed information
            details = place_details.get(pid, {})
            opening_hours = details.get('opening_hours', {})
            
            # Filter out closed/non-operational places
            business_status = place.get('business_status', 'OPERATIONAL')
            if business_status == 'CLOSED_PERMANENTLY':
                continue
            
            hospitals.append({
                'name': place.get('name', 'Healthcare Facility'),
                'lat': p_lat,
                'lon': p_lon,
                'address': place.get('vicinity', 'Address not available'),
                'rating': place.get('rating', 'N/A'),
                'user_ratings_total': place.get('user_ratings_total', 0),
                'distance': round(dist, 1),
                'place_id': pid,
                'open_now': opening_hours.get('open_now'),
                'phone': details.get('phone', 'Not available'),
                'website': details.get('website'),
                'business_status': business_status
            })
        
        # Sort by distance and filter duplicates
        hospitals = sorted(hospitals, key=lambda x: x['distance'])
        
        # Remove duplicates based on name and location proximity
        unique_hospitals = []
        seen_locations = set()
        
        for h in hospitals:
            loc_key = (round(h['lat'], 4), round(h['lon'], 4))
            if loc_key not in seen_locations:
                seen_locations.add(loc_key)
                unique_hospitals.append(h)
        
        print(f"✅ Returning {len(unique_hospitals)} unique hospitals")
        return unique_hospitals
        
    except requests.RequestException as e:
        print(f"❌ Network error fetching hospitals: {e}")
        return []
    except Exception as e:
        print(f"❌ Error fetching hospitals: {e}")
        return []

def get_pharmacies_from_google(lat: float, lon: float, radius_km: float = 5) -> List[Dict]:
    """
    Fetch nearby pharmacies from Google Maps Places API
    """
    try:
        lat, lon = float(lat), float(lon)
        url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
        
        params = {
            'location': f'{lat},{lon}',
            'radius': radius_km * 1000,
            'type': 'pharmacy',
            'keyword': 'pharmacy drugstore',
            'key': GOOGLE_MAPS_API_KEY
        }
        
        response = requests.get(url, params=params, timeout=15)
        response.raise_for_status()
        data = response.json()
        
        if data.get('status') not in ['OK', 'ZERO_RESULTS']:
            print(f"⚠️ Google Maps API Error for pharmacies: {data.get('status')}")
            return []
        
        pharmacies = []
        user_loc = (lat, lon)
        
        for place in data.get('results', []):
            p_lat = place['geometry']['location']['lat']
            p_lon = place['geometry']['location']['lng']
            p_loc = (p_lat, p_lon)
            
            dist = geodesic(user_loc, p_loc).kilometers
            
            pharmacies.append({
                'name': place.get('name', 'Pharmacy'),
                'lat': p_lat,
                'lon': p_lon,
                'address': place.get('vicinity', 'Address not available'),
                'rating': place.get('rating', 'N/A'),
                'distance': round(dist, 1),
                'open_now': place.get('opening_hours', {}).get('open_now', None)
            })
        
        return sorted(pharmacies, key=lambda x: x['distance'])[:5]  # Return top 5
        
    except Exception as e:
        print(f"⚠️ Error fetching pharmacies: {e}")
        return []

def create_folium_map(lat: float, lon: float, hospitals: List[Dict], 
                     pharmacies: List[Dict] = None, address: Optional[str] = None, 
                     air_quality: Optional[Dict] = None) -> Tuple[Optional[str], float, float]:
    """
    Create an interactive Folium map with enhanced styling
    Now includes pharmacies and air quality info
    """
    try:
        lat, lon = float(lat), float(lon)
        m = folium.Map(
            location=[lat, lon],
            zoom_start=13,
            tiles='OpenStreetMap',
            control_scale=True
        )
        
        # Add air quality circle overlay if available
        if air_quality and isinstance(air_quality.get('aqi'), int):
            aqi_color, _ = get_aqi_color(air_quality['aqi'])
            folium.Circle(
                location=[lat, lon],
                radius=3000,  # 3km radius
                color=aqi_color,
                fill=True,
                fillColor=aqi_color,
                fillOpacity=0.1,
                weight=2,
                popup=f"<b>Air Quality Zone</b><br>AQI: {air_quality.get('aqi', 'N/A')} - {air_quality.get('category', 'Unknown')}"
            ).add_to(m)
        
        # Add search location marker with air quality info
        popup_text = f'📍 <b>Your Location</b><br>{address if address else "Current Position"}'        
        if air_quality:
            popup_text += f"<br><br><b>Air Quality:</b><br>AQI: {air_quality.get('aqi', 'N/A')}<br>{air_quality.get('category', 'Unknown')}"
        
        folium.CircleMarker(
            location=[lat, lon],
            radius=12,
            popup=popup_text,
            color='#1d4ed8',
            fill=True,
            fillColor='#3b82f6',
            fillOpacity=0.6,
            weight=3
        ).add_to(m)
        
        # Add hospital markers
        for idx, h in enumerate(hospitals, 1):
            status_color = "green" if h['open_now'] is True else ("red" if h['open_now'] is False else "gray")
            status_text = "🟢 Open Now" if h['open_now'] is True else ("🔴 Closed" if h['open_now'] is False else "⚪ Hours Unknown")
            
            popup_html = f"""
            <div style='font-family: system-ui, -apple-system, sans-serif; min-width: 250px; max-width: 300px;'>
                <h4 style='margin:0 0 8px 0; color:#0d9488; font-size:1.1rem;'>🏥 {html.escape(h['name'])}</h4>
                <hr style='margin: 8px 0; border: none; border-top: 1px solid #e2e8f0;'>
                <p style='margin:4px 0; font-size:0.9rem;'><b>Distance:</b> {h['distance']} km</p>
                <p style='margin:4px 0; font-size:0.9rem;'><b>Rating:</b> ⭐ {h['rating']} ({h['user_ratings_total']} reviews)</p>
                <p style='margin:4px 0; font-size:0.9rem;'><b>Status:</b> <span style='color:{status_color};'>{status_text}</span></p>
                <p style='margin:4px 0; font-size:0.9rem;'><b>Phone:</b> <a href='tel:{h['phone']}' style='color:#2dd4bf; text-decoration:none;'>{html.escape(h['phone'])}</a></p>
                {f"<p style='margin:4px 0; font-size:0.9rem;'><b>Website:</b> <a href='{h['website']}' target='_blank' style='color:#2dd4bf;'>Visit</a></p>" if h.get('website') else ''}
                <p style='margin:6px 0 8px 0; font-size:0.85rem; color:#64748b;'>{html.escape(h['address'])}</p>
                <a href='https://www.google.com/maps/dir/?api=1&destination={h['lat']},{h['lon']}' 
                   target='_blank' style='display:inline-block; margin-top:8px; padding: 6px 12px; background:#2dd4bf; color:white; text-decoration:none; border-radius:6px; font-weight:600; font-size:0.9rem;'>
                   🗺️ Get Directions
                </a>
            </div>
            """
            
            folium.Marker(
                location=[h['lat'], h['lon']],
                popup=folium.Popup(popup_html, max_width=320),
                icon=folium.Icon(color='red', icon='plus-square', prefix='fa'),
                tooltip=f"🏥 {h['name']} ({h['distance']} km)"
            ).add_to(m)
        
        # Add pharmacy markers
        if pharmacies:
            for pharmacy in pharmacies:
                popup_html = f"""
                <div style='font-family: system-ui, -apple-system, sans-serif; min-width: 250px; max-width: 300px;'>
                    <h4 style='margin:0 0 8px 0; color:#10b981; font-size:1.1rem;'>💊 {html.escape(pharmacy['name'])}</h4>
                    <hr style='margin: 8px 0; border: none; border-top: 1px solid #e2e8f0;'>
                    <p style='margin:4px 0; font-size:0.9rem;'><b>Distance:</b> {pharmacy['distance']} km</p>
                    <p style='margin:4px 0; font-size:0.9rem;'><b>Rating:</b> ⭐ {pharmacy['rating']}</p>
                    <p style='margin:6px 0 8px 0; font-size:0.85rem; color:#64748b;'>{html.escape(pharmacy['address'])}</p>
                    <a href='https://www.google.com/maps/dir/?api=1&destination={pharmacy['lat']},{pharmacy['lon']}' 
                       target='_blank' style='display:inline-block; margin-top:8px; padding: 6px 12px; background:#10b981; color:white; text-decoration:none; border-radius:6px; font-weight:600; font-size:0.9rem;'>
                       🗺️ Get Directions
                    </a>
                </div>
                """
                
                folium.Marker(
                    location=[pharmacy['lat'], pharmacy['lon']],
                    popup=folium.Popup(popup_html, max_width=320),
                    icon=folium.Icon(color='green', icon='shopping-cart', prefix='fa'),
                    tooltip=f"💊 {pharmacy['name']} ({pharmacy['distance']} km)"
                ).add_to(m)
        
        plugins.Fullscreen().add_to(m)
        
        return m._repr_html_(), lat, lon
    except Exception as e:
        print(f"❌ Error creating map: {e}")
        return None, lat, lon

def find_hospitals_nearby(lat: Optional[float] = None, lon: Optional[float] = None, 
                         address: Optional[str] = None, radius_km: float = 10,
                         include_air_quality: bool = True, include_pharmacies: bool = True) -> Tuple[str, str, str]:
    """
    Main integrated function for finding hospitals by GPS or Address
    Now with optional air quality and pharmacy data
    """
    location_source = "unknown"
    
    # Priority 1: Use provided coordinates
    if lat and lon:
        try:
            lat, lon = float(lat), float(lon)
            location_source = "GPS coordinates"
            print(f"✅ Using provided coordinates: ({lat}, {lon})")
        except (ValueError, TypeError):
            lat, lon = None, None
    
    # Priority 2: Geocode address
    if (not lat or not lon) and address:
        lat, lon = geocode_address(address)
        if lat and lon:
            location_source = f"address '{address}'"
    
    # Priority 3: IP-based location
    if not lat or not lon:
        print("⚠️ No GPS or address provided, trying IP location...")
        lat, lon = get_location_from_ip()
        if lat and lon:
            location_source = "IP address"
    
    # If still no location
    if not lat or not lon:
        error_html = """
        <div class='matte-panel' style='text-align:center; padding:40px;'>
            <h2 style='color:#ef4444; margin-bottom:20px;'>❌ Location Required</h2>
            <p style='color:#adb5bd; font-size:1.1rem;'>
                Please either:<br>
                • Click the GPS button to share your location<br>
                • Enter a city name or address manually
            </p>
        </div>
        """
        return error_html, "", "### Status: ❌ No location available"
    
    print(f"✅ Using location from {location_source}: ({lat}, {lon})")
    
    try:
        # Fetch air quality data if enabled
        air_quality = None
        if include_air_quality:
            print("🌍 Fetching air quality data...")
            air_quality = get_air_quality(lat, lon)
        
        # Fetch hospitals
        hospitals = get_hospitals_from_google(lat, lon, radius_km)
        
        # Fetch pharmacies if enabled
        pharmacies = []
        if include_pharmacies:
            print("💊 Fetching nearby pharmacies...")
            pharmacies = get_pharmacies_from_google(lat, lon, min(5, radius_km))
        
        if not hospitals:
            warning_html = f"""
            <div class='matte-panel' style='text-align:center; padding:40px;'>
                <h2 style='color:#f59e0b; margin-bottom:20px;'>⚠️ No Hospitals Found</h2>
                <p style='color:#adb5bd; font-size:1.1rem;'>
                    No hospitals found within {radius_km}km of {location_source}.<br>
                    Try increasing the search radius or checking a different location.
                </p>
            </div>
            """
            return warning_html, "", f"### Status: ⚠️ No results within {radius_km}km"
        
        # Create air quality display
        air_quality_html = create_air_quality_display(air_quality) if air_quality else ""
        
        # Create map with optional pharmacy markers
        map_html, center_lat, center_lon = create_folium_map(lat, lon, hospitals, pharmacies, address, air_quality)
        
        if not map_html:
            return "<div class='matte-panel'>Error creating map</div>", "", "### Status: ❌ Map error"
        
        map_iframe = f"""
        {air_quality_html}
        <div style='border-radius:20px; overflow:hidden; box-shadow:0 12px 48px rgba(0,0,0,0.3); border:1px solid rgba(58, 134, 255, 0.2);'>
            <iframe srcdoc="{html.escape(map_html)}" width="100%" height="550px" style="border:none;"></iframe>
        </div>
        <p style='font-size:0.85rem; color:#adb5bd; text-align:center; margin-top:12px;'>
            📍 Showing hospitals near <b>{address if address else location_source}</b> • 📏 Distances are straight-line measurements
            {f' • 💊 {len(pharmacies)} nearby pharmacies' if pharmacies else ''}
        </p>
        """
        
        # Create hospital cards with matte-panel class
        cards_html = "<div style='display:grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap:20px; margin-top:30px;'>"
        
        for idx, h in enumerate(hospitals[:20], 1):  # Limit to top 20 for UI performance
            status_indicator = "🟢" if h['open_now'] is True else ("🔴" if h['open_now'] is False else "⚪")
            
            cards_html += f"""
            <div class='matte-panel' style='padding:20px; transition:all 0.3s ease; border: 1px solid #3a3f50;'>
                <div style='display:flex; justify-content:space-between; align-items:start; margin-bottom:12px;'>
                    <h3 style='margin:0; color:#3a86ff; font-size:1.1rem; flex:1;'>{idx}. {html.escape(h['name'])}</h3>
                    <span style='background:rgba(58, 134, 255, 0.15); color:#3a86ff; padding:6px 14px; border-radius:20px; font-size:0.85rem; font-weight:700; white-space:nowrap; margin-left:10px;'>
                        {h['distance']} km
                    </span>
                </div>
                
                <p style='color:#adb5bd; font-size:0.9rem; margin:8px 0; line-height:1.4;'>📍 {html.escape(h['address'])}</p>
                
                <div style='display:flex; gap:15px; margin:12px 0; flex-wrap:wrap;'>
                    <span style='color:#f59e0b; font-weight:600; font-size:0.95rem;'>⭐ {h['rating']}</span>
                    <span style='color:#adb5bd; font-size:0.9rem;'>({h['user_ratings_total']} reviews)</span>
                    <span style='font-size:0.95rem;'>{status_indicator}</span>
                </div>
                
                <p style='color:#3a86ff; font-size:0.95rem; margin:10px 0; font-weight:600;'>
                    📞 <a href='tel:{h['phone']}' style='color:#3a86ff; text-decoration:none;'>{html.escape(h['phone'])}</a>
                </p>
                
                <div style='display:flex; gap:12px; margin-top:16px; flex-wrap:wrap;'>
                    <a href='tel:{h['phone']}' 
                       style='color:#fff; background:#3a86ff; text-decoration:none; font-weight:700; font-size:0.9rem; padding:8px 16px; border-radius:8px; display:inline-block;'>
                       📞 Call Now
                    </a>
                    <a href='https://www.google.com/maps/dir/?api=1&destination={h['lat']},{h['lon']}' 
                       target='_blank' style='color:#3a86ff; text-decoration:none; font-weight:700; font-size:0.9rem; padding:8px 16px; border:2px solid #3a86ff; border-radius:8px; display:inline-block;'>
                       🗺️ Directions
                    </a>
                    {f"<a href='{h['website']}' target='_blank' style='color:#3a86ff; text-decoration:none; font-weight:700; font-size:0.9rem; padding:8px 16px; border:2px solid #3a86ff; border-radius:8px; display:inline-block;'>🌐 Website</a>" if h.get('website') else ''}
                </div>
            </div>
            """
        
        cards_html += "</div>"
        
        # Add pharmacy section if available
        if pharmacies:
            cards_html += """
            <div style='margin-top: 40px;'>
                <h2 style='color:#10b981; margin-bottom: 20px;'>💊 Nearby Pharmacies</h2>
                <div style='display:grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap:20px;'>
            """
            
            for pharmacy in pharmacies:
                status_indicator = "🟢 Open" if pharmacy['open_now'] is True else ("🔴 Closed" if pharmacy['open_now'] is False else "⚪ Hours Unknown")
                status_color = "#10b981" if pharmacy['open_now'] is True else ("#ef4444" if pharmacy['open_now'] is False else "#adb5bd")
                
                cards_html += f"""
                <div class='matte-panel' style='padding:20px; border: 1px solid #3a3f50; border-left: 4px solid #10b981;'>
                    <div style='display:flex; justify-content:space-between; align-items:start; margin-bottom:12px;'>
                        <h3 style='margin:0; color:#10b981; font-size:1.1rem; flex:1;'>💊 {html.escape(pharmacy['name'])}</h3>
                        <span style='background:rgba(16,185,129,0.15); color:#10b981; padding:6px 14px; border-radius:20px; font-size:0.85rem; font-weight:700;'>
                            {pharmacy['distance']} km
                        </span>
                    </div>
                    
                    <p style='color:#adb5bd; font-size:0.9rem; margin:8px 0; line-height:1.4;'>📍 {html.escape(pharmacy['address'])}</p>
                    
                    <div style='display:flex; gap:15px; margin:12px 0; align-items:center;'>
                        <span style='color:#f59e0b; font-weight:600; font-size:0.95rem;'>⭐ {pharmacy['rating']}</span>
                        <span style='color:{status_color}; font-size:0.9rem; font-weight:600;'>{status_indicator}</span>
                    </div>
                    
                    <div style='margin-top:16px;'>
                        <a href='https://www.google.com/maps/dir/?api=1&destination={pharmacy['lat']},{pharmacy['lon']}' 
                           target='_blank' style='color:#10b981; text-decoration:none; font-weight:700; font-size:0.9rem; padding:8px 16px; border:2px solid #10b981; border-radius:8px; display:inline-block;'>
                           🗺️ Get Directions
                        </a>
                    </div>
                </div>
                """
            
            cards_html += """
                </div>
            </div>
            """
        
        if len(hospitals) > 20:
            cards_html += f"<p style='text-align:center; color:#adb5bd; margin-top:20px; font-size:0.9rem;'>Showing 20 of {len(hospitals)} hospitals found</p>"
        
        # Status message with air quality info
        aqi_info = ""
        if air_quality:
            aqi_info = f" • 🌍 AQI: {air_quality.get('aqi', 'N/A')}"
        
        status = f"### Status: ✅ Found {len(hospitals)} hospitals{aqi_info} • Location: {location_source}"
        
        return map_iframe, cards_html, status
        
    except Exception as e:
        print(f"❌ Critical error: {e}")
        error_html = f"""
        <div class='matte-panel' style='padding:30px; text-align:center; border: 1px solid #3a3f50;'>
            <h3 style='color:#ef4444;'>❌ Error Occurred</h3>
            <p style='color:#adb5bd;'>{html.escape(str(e))}</p>
        </div>
        """
        return error_html, "", f"### Status: ❌ Error: {str(e)}"