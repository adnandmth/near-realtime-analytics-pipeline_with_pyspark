import os
import random
import time
import uuid
import boto3
import csv
import json

from confluent_kafka import SerializingProducer
import simplejson as json
from datetime import datetime, timedelta
from config import configuration

# Initialize a Kinesis client
KINESIS_CLIENT = boto3.client('kinesis', region_name='ap-southeast-1')  # replace with your region

# Define the Kinesis stream name
STREAM_NAME = 'kinesis-kafka-demo'

LONDON_COORDINATES = {"latitude": 51.5074, "longitude": -0.1278}
BIRMINGHAM_COORDINATES = {"latitude": 52.4862, "longitude": -1.8904}

# Calculate movement increments
LATITUDE_INCREMENT = (BIRMINGHAM_COORDINATES['latitude'] - LONDON_COORDINATES['latitude']) / 100
LONGITUDE_INCREMENT = (BIRMINGHAM_COORDINATES['longitude'] - LONDON_COORDINATES['longitude']) / 100 

random.seed(42)
start_time = datetime.now()
start_location = LONDON_COORDINATES.copy()

def get_next_time():
    global start_time
    start_time += timedelta(seconds=random.randint(30, 60))  # update frequency
    return start_time

def generate_gps_data(device_id, timestamp, vehicle_type='private'):
    return {
        'id': str(uuid.uuid4()),
        'deviceId': device_id,
        'timestamp': timestamp,
        'speed': random.uniform(0, 40),  # km/h
        'direction': 'North-East',
        'vehicleType': vehicle_type
    }

def simulate_vehicle_movement():
    global start_location
    
    # move towards birmingham
    start_location['latitude'] += LATITUDE_INCREMENT
    start_location['longitude'] += LONGITUDE_INCREMENT
    
    # add some randomness to simulate actual road travel
    start_location['latitude'] += random.uniform(-0.0005, 0.0005)
    start_location['longitude'] += random.uniform(-0.0005, 0.0005)
    
    return start_location

def generate_vehicle_data(device_id):
    location = simulate_vehicle_movement()
    
    return {
        'id': str(uuid.uuid4()),
        'deviceId': device_id,
        'timestamp': get_next_time().isoformat(),
        'location': (location['latitude'], location['longitude']),
        'speed': random.uniform(10, 40),
        'direction': 'North-East',
        'make': 'BMW',
        'model': 'C500',
        'year': 2024,
        'fuelType': 'Hybrid'
    }
    
def json_serializer(obj):
    if isinstance(obj, uuid.UUID):
        return str(obj)
    raise TypeError(f'Object of type {obj.__class__.__name__} is not JSON serializable')
    
def simulate_journey(device_id):
    while True:
        vehicle_data = generate_vehicle_data(device_id)
        gps_data = generate_gps_data(device_id, vehicle_data['timestamp'])
        
        print(f'vehicle_data:: {vehicle_data}')
        print(f'gps_data:: {gps_data}')
        
        if (vehicle_data['location'][0] >= BIRMINGHAM_COORDINATES['latitude']
                and vehicle_data['location'][1] <= BIRMINGHAM_COORDINATES['longitude']):
            print('Vehicle has reached Birmingham. Simulation ending...')
            break
        
        send_account_data_to_kinesis(vehicle_data)
        send_account_data_to_kinesis(gps_data)
        
        time.sleep(3)

# Function to produce events to Kinesis
def produce_event_to_kinesis(event_data, partition_key):
    
    print(configuration.get('AWS_ACCESS_KEY'))
    print(configuration.get('AWS_SECRET_KEY'))
    
    response = KINESIS_CLIENT.put_record(
        StreamName=STREAM_NAME,
        Data=event_data,
        PartitionKey=partition_key
    )
    return response

def send_account_data_to_kinesis(data):
    # Convert each row to JSON format
    event_data = json.dumps(data, default=json_serializer).encode('utf-8')
    # Use a relevant partition key; it could be any unique value, like an ID or timestamp
    final_partition_key = data['id']
    # Produce event to Kinesis
    produce_event_to_kinesis(event_data, final_partition_key)
    print(f"Sent event: {event_data}")
            

if __name__ == "__main__":
    try:
        simulate_journey('Vehicle-CodeWithYu-123')

    except KeyboardInterrupt:
        print('Simulation ended by the user')
    except Exception as e:
        print(f'Unexpected Error occurred: {e}')