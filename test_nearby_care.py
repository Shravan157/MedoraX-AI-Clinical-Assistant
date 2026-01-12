"""
Quick test script for the Nearby Care feature
"""

def test_hospital_finder():
    """Test the hospital finding functionality"""
    print("🧪 Testing Nearby Care Feature...\n")
    
    # Test coordinates (Mumbai, India)
    test_lat = "19.0760"
    test_lon = "72.8777"
    
    print(f"📍 Test Location: {test_lat}, {test_lon} (Mumbai)")
    print("-" * 50)
    
    try:
        # Import the functions
        import sys
        sys.path.append('.')
        
        # Test 1: Check if dependencies are installed
        print("\n✓ Test 1: Checking dependencies...")
        try:
            import folium
            import geopy
            print("  ✅ folium installed:", folium.__version__)
            print("  ✅ geopy installed:", geopy.__version__)
        except ImportError as e:
            print(f"  ❌ Missing dependency: {e}")
            return False
        
        # Test 2: Test hospital fetching
        print("\n✓ Test 2: Fetching hospitals from OpenStreetMap...")
        from gradio_app import get_hospitals_from_osm
        
        hospitals = get_hospitals_from_osm(test_lat, test_lon, radius_km=5)
        
        if hospitals:
            print(f"  ✅ Found {len(hospitals)} hospitals")
            print("\n  Top 3 Hospitals:")
            for i, h in enumerate(hospitals[:3], 1):
                print(f"    {i}. {h['name']}")
                print(f"       Distance: {h['distance']:.2f} km")
                print(f"       Phone: {h['phone']}")
                print(f"       Address: {h['address']}")
                print()
        else:
            print("  ⚠️ No hospitals found (this might be normal for some locations)")
        
        # Test 3: Test map creation
        print("✓ Test 3: Creating interactive map...")
        from gradio_app import create_hospital_map
        
        map_html, hospitals = create_hospital_map(test_lat, test_lon)
        
        if map_html:
            print("  ✅ Map created successfully")
            print(f"  ✅ Map HTML length: {len(map_html)} characters")
        else:
            print("  ❌ Failed to create map")
            return False
        
        # Test 4: Test hospital cards formatting
        print("\n✓ Test 4: Formatting hospital cards...")
        from gradio_app import format_hospital_cards
        
        cards_html = format_hospital_cards(hospitals)
        
        if cards_html:
            print("  ✅ Hospital cards formatted successfully")
            print(f"  ✅ Cards HTML length: {len(cards_html)} characters")
        else:
            print("  ❌ Failed to format cards")
            return False
        
        # Test 5: Test main function
        print("\n✓ Test 5: Testing main get_best_hospitals function...")
        from gradio_app import get_best_hospitals
        
        result_html, status = get_best_hospitals(test_lat, test_lon)
        
        if result_html and "Error" not in result_html:
            print("  ✅ Main function works correctly")
            print(f"  ✅ Status: {status}")
        else:
            print("  ❌ Main function failed")
            return False
        
        print("\n" + "=" * 50)
        print("🎉 All tests passed! Nearby Care feature is working.")
        print("=" * 50)
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_hospital_finder()
    exit(0 if success else 1)
