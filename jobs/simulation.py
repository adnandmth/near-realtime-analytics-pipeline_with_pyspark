import random
import uuid
import time
import json
from datetime import datetime, timedelta

# List of countries to simulate machine deployment
COUNTRIES = ("id", "ph", "us", "jp", "sg")

random.seed(42)
start_time = datetime.now()

def get_next_time():
    global start_time
    start_time += timedelta(seconds=random.randint(30, 60))
    return start_time

def generate_machine_data(device_id):
    current_timestamp_ms = int(time.time() * 1000)

    json_data = {
        "timestamp": current_timestamp_ms,
        "country": random.choice(COUNTRIES),
        "service": "kinesis-connector",
        "table": "orange_juicer_events",
        "event": "insert",
        "record": {
            "id": str(uuid.uuid4()),
            "deviceId": device_id,
            "timestamp": get_next_time().isoformat(),
            "machineStatus": random.choice(["Idle", "Juicing", "Cleaning", "Error"]),
            "orangesUsed": random.randint(1, 5),
            "juiceVolume_ml": round(random.uniform(200, 400), 2),  # ml of juice produced
            "cupSize": random.choice(["Small", "Medium", "Large"]),
            "temperature_C": round(random.uniform(4, 10), 1),  # storage temp
            "sugarLevel": random.choice(["No Sugar", "Less Sugar", "Normal", "Extra Sweet"]),
            "paymentMethod": random.choice(["Cashless", "Card", "MobilePay"]),
            "price": random.choice([1.5, 2.0, 2.5, 3.0]),  # in local currency unit
            "brand": "XJuice",
            "model": "SmartJuicerX1000",
            "year": 2024
        }
    }

    return json_data
    