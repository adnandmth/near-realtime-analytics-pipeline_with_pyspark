import random
import uuid
import time
import json
from datetime import datetime, timedelta

# Coordinates for simulation
LONDON_COORDINATES = {"latitude": 51.5074, "longitude": -0.1278}
BIRMINGHAM_COORDINATES = {"latitude": 52.4862, "longitude": -1.8904}
LATITUDE_INCREMENT = (BIRMINGHAM_COORDINATES['latitude'] - LONDON_COORDINATES['latitude']) / 100
LONGITUDE_INCREMENT = (BIRMINGHAM_COORDINATES['longitude'] - LONDON_COORDINATES['longitude']) / 100

random.seed(42)
start_time = datetime.now()
start_location = LONDON_COORDINATES.copy()

def get_next_time():
    global start_time
    start_time += timedelta(seconds=random.randint(30, 60))
    return start_time

def simulate_vehicle_movement():
    global start_location
    start_location['latitude'] += LATITUDE_INCREMENT + random.uniform(-0.0005, 0.0005)
    start_location['longitude'] += LONGITUDE_INCREMENT + random.uniform(-0.0005, 0.0005)
    return start_location

def generate_vehicle_data(device_id):
    current_timestamp_ms = int(time.time() * 1000)
    location = simulate_vehicle_movement()
    
    json_data = {
        "timestamp": current_timestamp_ms,
        "country": "id",
        "service": "kinesis-connector",
        "table": "vehicle_movement",
        "event": "insert",
        "record": {
            "id": str(uuid.uuid4()),
            "deviceId": device_id,
            "timestamp": get_next_time().isoformat(),
            "location": location,  # Use location as a dictionary,
            "speed": random.uniform(10, 40),
            "direction": 'North-East',
            "make": 'BMW',
            "model": 'C500',
            "year": 2024,
            "fuelType": 'Hybrid'
        }
    }
    
    return json_data