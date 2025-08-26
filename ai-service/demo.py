#!/usr/bin/env python3
"""
Delivery ETA Prediction Demo Script
This script demonstrates the key functionality of the ETA prediction system
"""

import requests
import json
import time
from utils import MANILA_LANDMARKS

BASE_URL = "http://localhost:5000"

def print_header(title):
    print(f"\n{'='*50}")
    print(f"🚚 {title}")
    print(f"{'='*50}")

def check_service_health():
    """Check if the AI service is running"""
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Service Status: {data['status']}")
            print(f"🤖 Model Trained: {data['model_trained']}")
            return data['model_trained']
        else:
            print(f"❌ Service not responding (Status: {response.status_code})")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Cannot connect to service: {e}")
        return False

def train_model():
    """Train the ML model"""
    print("\n🧠 Training ML Model...")
    try:
        response = requests.post(f"{BASE_URL}/train_model")
        if response.status_code == 200:
            data = response.json()
            if data['success']:
                results = data['results']
                print(f"✅ Model trained successfully!")
                print(f"📊 MAE: {results['mae']:.2f} minutes")
                print(f"📈 Training samples: {results['samples_trained']}")
                print(f"🧪 Test samples: {results['test_samples']}")
                return True
            else:
                print(f"❌ Training failed: {data.get('error', 'Unknown error')}")
                return False
        else:
            print(f"❌ Training request failed (Status: {response.status_code})")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Training request failed: {e}")
        return False

def predict_eta(current_lat, current_lng, dropoff_lat, dropoff_lng, location_name=""):
    """Make an ETA prediction"""
    payload = {
        "current_lat": current_lat,
        "current_lng": current_lng,
        "dropoff_lat": dropoff_lat,
        "dropoff_lng": dropoff_lng
    }
    
    try:
        response = requests.post(f"{BASE_URL}/predict_eta", json=payload)
        if response.status_code == 200:
            data = response.json()
            print(f"\n📍 Route: {location_name}")
            print(f"🕐 ETA: {data['eta_minutes']} minutes")
            print(f"📏 Distance: {data['distance_km']} km")
            print(f"📢 Message: {data['message']}")
            print(f"⏰ Timestamp: {data['timestamp']}")
            return data
        else:
            error_data = response.json() if response.content else {}
            print(f"❌ Prediction failed: {error_data.get('error', 'Unknown error')}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"❌ Prediction request failed: {e}")
        return None

def demo_landmark_routes():
    """Demonstrate predictions between Manila landmarks"""
    print_header("Manila Landmark Route Predictions")
    
    routes = [
        ("Manila to Makati CBD", "manila", "makati_cbd"),
        ("BGC to Ortigas", "bgc", "ortigas"),
        ("Quezon City to BGC", "quezon_city", "bgc"),
        ("Makati CBD to Pasig", "makati_cbd", "pasig"),
        ("Ortigas to Manila", "ortigas", "manila")
    ]
    
    for route_name, start_key, end_key in routes:
        start_coords = MANILA_LANDMARKS[start_key]
        end_coords = MANILA_LANDMARKS[end_key]
        
        predict_eta(
            start_coords[0], start_coords[1],
            end_coords[0], end_coords[1],
            route_name
        )
        time.sleep(1)  # Be nice to the API

def demo_proximity_scenarios():
    """Demonstrate different proximity scenarios"""
    print_header("Proximity-Based Notification Scenarios")
    
    # Base location (Manila)
    manila_lat, manila_lng = MANILA_LANDMARKS['manila']
    
    scenarios = [
        ("Very Close (500m)", manila_lat + 0.004, manila_lng + 0.004),  # ~500m
        ("Nearby (1.5km)", manila_lat + 0.013, manila_lng + 0.013),    # ~1.5km
        ("Medium Distance (5km)", manila_lat + 0.045, manila_lng + 0.045),  # ~5km
        ("Far Distance (15km)", manila_lat + 0.135, manila_lng + 0.135),    # ~15km
    ]
    
    for scenario_name, dropoff_lat, dropoff_lng in scenarios:
        predict_eta(manila_lat, manila_lng, dropoff_lat, dropoff_lng, scenario_name)
        time.sleep(1)

def demo_driver_analytics():
    """Demonstrate driver analytics functionality"""
    print_header("Driver Analytics Demo")
    
    drivers = ["DRV001", "DRV002", "DRV003"]
    
    for driver_id in drivers:
        try:
            response = requests.post(f"{BASE_URL}/driver_analytics", json={"driver_id": driver_id})
            if response.status_code == 200:
                data = response.json()
                print(f"\n👨‍💼 Driver: {data['driver_id']}")
                print(f"⏱️ Avg Delivery Time: {data['avg_delivery_time']:.1f} minutes")
                print(f"✅ Completion Rate: {data['completion_rate']:.1%}")
                print(f"⭐ Customer Rating: {data['customer_rating']:.1f}/5.0")
                print(f"📦 Total Deliveries: {data['total_deliveries']}")
                print(f"⚠️ Violations: {data['violations_count']}")
                print(f"🧪 Drug Test: {data['last_drug_test']}")
                print(f"📄 Credentials: {data['credential_status']}")
            else:
                print(f"❌ Failed to get analytics for {driver_id}")
        except requests.exceptions.RequestException as e:
            print(f"❌ Analytics request failed: {e}")
        
        time.sleep(1)

def show_available_landmarks():
    """Display available Manila landmarks"""
    print_header("Available Manila Landmarks")
    
    for name, (lat, lng) in MANILA_LANDMARKS.items():
        formatted_name = name.replace('_', ' ').title()
        print(f"📍 {formatted_name}: {lat}, {lng}")

def main():
    """Main demo function"""
    print_header("Delivery ETA Prediction System Demo")
    print("🚀 Starting comprehensive demonstration...")
    
    # Check service health
    model_trained = check_service_health()
    
    # Train model if needed
    if not model_trained:
        if not train_model():
            print("❌ Cannot proceed without trained model")
            return
    
    # Show available landmarks
    show_available_landmarks()
    
    # Run demonstrations
    demo_landmark_routes()
    demo_proximity_scenarios()
    demo_driver_analytics()
    
    print_header("Demo Complete")
    print("🎉 All demonstrations completed successfully!")
    print("\n💡 Try the web interfaces:")
    print("   🌐 Simple HTML: http://localhost:5000")
    print("   ⚛️ React App: http://localhost:3000/eta")
    print("   📊 Metabase: http://localhost:3001")

if __name__ == "__main__":
    main()
