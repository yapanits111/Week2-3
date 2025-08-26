from geopy.distance import geodesic
import datetime
import numpy as np

def calculate_distance(lat1, lng1, lat2, lng2):
    """
    Calculate distance between two points using Haversine formula
    """
    return geodesic((lat1, lng1), (lat2, lng2)).km

def get_time_features():
    """
    Get current time features for prediction
    """
    now = datetime.datetime.now()
    return {
        'hour': now.hour,
        'weekday': now.weekday()
    }

def generate_proximity_message(distance_km, eta_minutes):
    """
    Generate proximity-based notification message
    """
    if distance_km < 0.5:  # Less than 500m
        return "Delivery arriving very soon!"
    elif distance_km < 2:  # Less than 2km
        return "Delivery nearby, preparing for arrival"
    elif eta_minutes < 5:
        return "Arriving soon!"
    elif eta_minutes < 15:
        return "On the way - arriving shortly"
    else:
        return "Delivery in progress"

def validate_coordinates(lat, lng):
    """
    Validate latitude and longitude values
    """
    try:
        lat = float(lat)
        lng = float(lng)
        
        if not (-90 <= lat <= 90):
            return False, "Latitude must be between -90 and 90"
        
        if not (-180 <= lng <= 180):
            return False, "Longitude must be between -180 and 180"
            
        return True, None
    except (ValueError, TypeError):
        return False, "Coordinates must be numeric values"

def calculate_eta_with_traffic(base_eta, hour):
    """
    Adjust ETA based on traffic patterns
    """
    # Rush hour multiplier
    if 7 <= hour <= 9 or 17 <= hour <= 19:
        return base_eta * 1.5
    # Late night discount
    elif 22 <= hour or hour <= 6:
        return base_eta * 0.8
    else:
        return base_eta

def format_eta_response(eta_minutes, distance_km, message, timestamp=None):
    """
    Format the ETA response in a consistent structure
    """
    if timestamp is None:
        timestamp = datetime.datetime.now().isoformat()
    
    return {
        'eta_minutes': round(float(eta_minutes), 2),
        'distance_km': round(float(distance_km), 2),
        'message': message,
        'timestamp': timestamp
    }

class DeliveryDataGenerator:
    """
    Utility class for generating synthetic delivery data
    """
    
    def __init__(self, manila_bounds=True):
        if manila_bounds:
            self.lat_range = (14.5, 14.7)
            self.lng_range = (120.9, 121.1)
        else:
            # Global bounds
            self.lat_range = (-90, 90)
            self.lng_range = (-180, 180)
    
    def generate_random_coordinate(self):
        """Generate a random coordinate within bounds"""
        lat = np.random.uniform(*self.lat_range)
        lng = np.random.uniform(*self.lng_range)
        return lat, lng
    
    def generate_delivery_route(self):
        """Generate a realistic delivery route"""
        pickup_lat, pickup_lng = self.generate_random_coordinate()
        dropoff_lat, dropoff_lng = self.generate_random_coordinate()
        
        distance = calculate_distance(pickup_lat, pickup_lng, dropoff_lat, dropoff_lng)
        
        # Generate realistic travel time based on distance
        base_time_per_km = 3  # minutes
        hour = np.random.randint(0, 24)
        weekday = np.random.randint(0, 7)
        
        # Traffic factors
        traffic_multiplier = 1.5 if 7 <= hour <= 9 or 17 <= hour <= 19 else 1.0
        weekend_multiplier = 0.8 if weekday >= 5 else 1.0
        
        travel_time = distance * base_time_per_km * traffic_multiplier * weekend_multiplier
        travel_time += np.random.normal(0, 2)  # Add noise
        travel_time = max(travel_time, 1)  # Minimum 1 minute
        
        return {
            'pickup_lat': pickup_lat,
            'pickup_lng': pickup_lng,
            'dropoff_lat': dropoff_lat,
            'dropoff_lng': dropoff_lng,
            'distance_km': distance,
            'hour': hour,
            'weekday': weekday,
            'travel_time_minutes': travel_time
        }

# Manila landmarks for testing
MANILA_LANDMARKS = {
    'makati_cbd': (14.5547, 121.0244),
    'bgc': (14.5176, 121.0509),
    'ortigas': (14.5866, 121.0611),
    'quezon_city': (14.6760, 121.0437),
    'manila': (14.5995, 120.9842),
    'pasig': (14.5764, 121.0851),
    'mandaluyong': (14.5774, 121.0359),
    'taguig': (14.5243, 121.0792),
    'paranaque': (14.4793, 121.0198),
    'las_pinas': (14.4304, 121.0098)
}
