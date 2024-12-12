import os
import random
import time
import uuid

from confluent_kafka import SerializingProducer
import simplejson as json
from datetime import datetime, timedelta

# Environment Variables for configuration
KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'broker:29092')
CORE3_ASIA = os.getenv('CORE3_ASIA', 'core3-asia')
BI_IDEAL_DATA = os.getenv('BI_IDEAL_DATA', 'bi-ideal-date')
    
def json_serializer(obj):
    if isinstance(obj, uuid.UUID):
        return str(obj)
    raise TypeError(f'Object of type {obj.__class__.__name__} is not JSON serializable')


def delivery_report(err, msg):
    if err is not None:
        print(f'Message delivery failed: {err}')
    else:
        print(f'Message delivered to {msg.topic()} [{msg.partition()}]')
        
def produce_data_to_kafka(producer, topic, data):
    producer.produce(
        topic,
        key=str(data['id']),
        value=json.dumps(data, default=json_serializer).encode('utf-8'),
        on_delivery=delivery_report
    )

    producer.flush()
    
def simulate_journey(producer, device_id):
    while True:

        produce_data_to_kafka(producer, VEHICLE_TOPIC, vehicle_data)
        produce_data_to_kafka(producer, GPS_TOPIC, gps_data)
        
        time.sleep(3)

if __name__ == "__main__":
    producer_config = {
        'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS,
        'error_cb': lambda err: print(f'Kafka error: {err}')
    }
    producer = SerializingProducer(producer_config)
    
    try:
        simulate_journey(producer, 'Vehicle-CodeWithYu-123')

    except KeyboardInterrupt:
        print('Simulation ended by the user')
    except Exception as e:
        print(f'Unexpected Error occurred: {e}')