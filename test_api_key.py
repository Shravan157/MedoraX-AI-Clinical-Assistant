
import requests
import os

key = "AIzaSyAmDAgwmjuvNNOv1K7d1UF7SbMlDAsAmXs"
url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
params = {
    'location': '28.6139,77.2090',
    'radius': 1000,
    'type': 'hospital',
    'key': key
}
try:
    response = requests.get(url, params=params, timeout=10)
    print(f"Status: {response.status_code}")
    print(f"Data status: {response.json().get('status')}")
    if response.json().get('error_message'):
        print(f"Error: {response.json().get('error_message')}")
except Exception as e:
    print(f"Error: {e}")
