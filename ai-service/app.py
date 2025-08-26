from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
from geopy.distance import geodesic
import joblib
import datetime
import redis
import json
import os
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)
CORS(app)

# Redis connection
redis_client = redis.Redis(host=os.getenv('REDIS_HOST', 'localhost'), port=6379, decode_responses=True)

# PostgreSQL connection
def get_db_connection():
    return psycopg2.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        database=os.getenv('DB_NAME', 'logistics_db'),
        user=os.getenv('DB_USER', 'postgres'),
        password=os.getenv('DB_PASSWORD', 'password'),
        cursor_factory=RealDictCursor
    )

class ETAPredictor:
    def __init__(self):
        self.model = None
        self.is_trained = False
        
    def generate_sample_data(self, n_samples=1000):
        """Generate sample delivery data for training"""
        np.random.seed(42)
        
        # Manila area coordinates
        lat_range = (14.5, 14.7)
        lng_range = (120.9, 121.1)
        
        data = []
        for i in range(n_samples):
            pickup_lat = np.random.uniform(*lat_range)
            pickup_lng = np.random.uniform(*lng_range)
            dropoff_lat = np.random.uniform(*lat_range)
            dropoff_lng = np.random.uniform(*lng_range)
            
            # Calculate distance
            distance = geodesic((pickup_lat, pickup_lng), (dropoff_lat, dropoff_lng)).km
            
            # Generate realistic travel time based on distance and time factors
            hour = np.random.randint(0, 24)
            weekday = np.random.randint(0, 7)
            
            # Base time per km (with traffic factors)
            base_time_per_km = 3  # minutes
            traffic_multiplier = 1.5 if 7 <= hour <= 9 or 17 <= hour <= 19 else 1.0  # Rush hour
            weekend_multiplier = 0.8 if weekday >= 5 else 1.0
            
            travel_time = distance * base_time_per_km * traffic_multiplier * weekend_multiplier
            travel_time += np.random.normal(0, 2)  # Add noise
            travel_time = max(travel_time, 1)  # Minimum 1 minute
            
            data.append({
                'order_id': f'ORDER_{i+1:04d}',
                'pickup_lat': pickup_lat,
                'pickup_lng': pickup_lng,
                'dropoff_lat': dropoff_lat,
                'dropoff_lng': dropoff_lng,
                'distance_km': distance,
                'hour': hour,
                'weekday': weekday,
                'travel_time_minutes': travel_time
            })
        
        return pd.DataFrame(data)
    
    def train_model(self):
        """Train the ETA prediction model"""
        # Generate sample data
        df = self.generate_sample_data()
        
        # Features and target
        X = df[['distance_km', 'hour', 'weekday']]
        y = df['travel_time_minutes']
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Train model
        self.model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.model.fit(X_train, y_train)
        
        # Evaluate
        predictions = self.model.predict(X_test)
        mae = mean_absolute_error(y_test, predictions)
        
        # Save model
        joblib.dump(self.model, 'model.pkl')
        self.is_trained = True
        
        return {
            'mae': mae,
            'samples_trained': len(df),
            'test_samples': len(X_test)
        }
    
    def predict_eta(self, current_lat, current_lng, dropoff_lat, dropoff_lng):
        """Predict ETA for delivery"""
        if not self.is_trained:
            return None
            
        distance = geodesic((current_lat, current_lng), (dropoff_lat, dropoff_lng)).km
        hour = datetime.datetime.now().hour
        weekday = datetime.datetime.now().weekday()
        
        features = [[distance, hour, weekday]]
        eta_minutes = self.model.predict(features)[0]
        
        return max(eta_minutes, 1)  # Minimum 1 minute

# Initialize predictor
predictor = ETAPredictor()

@app.route('/')
def index():
    """Serve the HTML interface"""
    return '''
    <!DOCTYPE html>
    <html>
    <head><title>ETA Tracker</title></head>
    <body>
        <h1>🚚 ETA Delivery Tracker</h1>
        <p>AI-powered delivery time estimation</p>
        <p><a href="/health">Health Check</a></p>
        <p>Use the API endpoints:</p>
        <ul>
            <li>POST /predict_eta - Predict delivery time</li>
            <li>POST /train_model - Train the model</li>
            <li>GET /health - Health status</li>
        </ul>
    </body>
    </html>
    '''

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'model_trained': predictor.is_trained})

@app.route('/train_model', methods=['POST'])
def train_model():
    """Train the ETA prediction model"""
    try:
        results = predictor.train_model()
        return jsonify({
            'success': True,
            'message': 'Model trained successfully',
            'results': results
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/predict_eta', methods=['POST'])
def predict_eta():
    """Predict ETA for delivery"""
    try:
        data = request.json
        
        if not predictor.is_trained:
            return jsonify({'error': 'Model not trained yet. Call /train_model first.'}), 400
        
        required_fields = ['current_lat', 'current_lng', 'dropoff_lat', 'dropoff_lng']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400
        
        eta = predictor.predict_eta(
            data['current_lat'],
            data['current_lng'],
            data['dropoff_lat'],
            data['dropoff_lng']
        )
        
        # Generate proximity-based message
        distance = geodesic(
            (data['current_lat'], data['current_lng']), 
            (data['dropoff_lat'], data['dropoff_lng'])
        ).km
        
        if distance < 0.5:  # Less than 500m
            message = "Delivery arriving very soon!"
        elif distance < 2:  # Less than 2km
            message = "Delivery nearby, preparing for arrival"
        elif eta < 5:
            message = "Arriving soon!"
        elif eta < 15:
            message = "On the way - arriving shortly"
        else:
            message = "Delivery in progress"
        
        # Cache result in Redis
        cache_key = f"eta:{data['current_lat']}:{data['current_lng']}:{data['dropoff_lat']}:{data['dropoff_lng']}"
        cache_data = {
            'eta_minutes': round(eta, 2),
            'message': message,
            'distance_km': round(distance, 2),
            'timestamp': datetime.datetime.now().isoformat()
        }
        redis_client.setex(cache_key, 300, json.dumps(cache_data))  # Cache for 5 minutes
        
        return jsonify(cache_data)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/driver_analytics', methods=['POST'])
def driver_analytics():
    """Analyze driver performance for profiling"""
    try:
        data = request.json
        driver_id = data.get('driver_id')
        
        if not driver_id:
            return jsonify({'error': 'driver_id required'}), 400
        
        # This would normally pull from database
        # For now, generate sample analytics
        analytics = {
            'driver_id': driver_id,
            'avg_delivery_time': np.random.uniform(15, 45),
            'completion_rate': np.random.uniform(0.8, 0.99),
            'customer_rating': np.random.uniform(3.5, 5.0),
            'total_deliveries': np.random.randint(50, 500),
            'violations_count': np.random.randint(0, 5),
            'last_drug_test': 'negative',
            'credential_status': 'valid'
        }
        
        return jsonify(analytics)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Try to load existing model
    try:
        predictor.model = joblib.load('model.pkl')
        predictor.is_trained = True
        print("Loaded existing model")
    except FileNotFoundError:
        print("No existing model found. Train model using /train_model endpoint")
    
    app.run(host='0.0.0.0', port=5000, debug=True)
