from kafka import KafkaProducer
import json
import uuid

TOPIC_NAME = 'test4-topic'
BROKER = ['broker1:9092', 'broker2:9092', 'broker3:9092']  # change if using a remote or multi-broker setup

# Create Kafka producer
producer = KafkaProducer(
    bootstrap_servers=BROKER,
    value_serializer=lambda v: json.dumps(v, default=lambda o: str(o)).encode('utf-8'),
    key_serializer=lambda k: str(k).encode('utf-8')  # for partitioning
)

def send_account_data_to_kafka(data):
    key = data['record']['id']  # used to assign a partition
    print(f"type of data: {type(data)}")
    
    producer.send(
        topic=TOPIC_NAME,
        key=key,           # for partitioning
        value=data         # gets serialized by value_serializer
    )
    producer.flush()  # ensures data is sent immediately
    print(f"Sent: {data}")