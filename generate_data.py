import time
import json
from jobs.simulation import generate_machine_data
from kafka_utils.kafka_client import send_account_data_to_kafka


def simulate_journey(device_id):
    print("Starting orange juice vending machine simulation...")
    while True:
        vending_machine_data = generate_machine_data(device_id) # returns dict
        print(f"vending_machine_data:: {vending_machine_data}")

        send_account_data_to_kafka(vending_machine_data)
        time.sleep(1)  # simulate a delay between events

if __name__ == "__main__":
    try:
        simulate_journey('orange-juice-123')
    except KeyboardInterrupt:
        print('Simulation ended by the user')
    except Exception as e:
        print(f'Unexpected Error occurred: {e}')