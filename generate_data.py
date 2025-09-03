import time
import json
from jobs.simulation import generate_vehicle_data
from kafka_utils.kafka_client import send_account_data_to_kafka


def simulate_journey(device_id):
    print("Starting vehicle journey simulation...")
    while True:
        vehicle_data = generate_vehicle_data(device_id) # returns dict
        print(f"vehicle_data:: {vehicle_data}")
        print(f"latitude:: {vehicle_data['record']['location']['latitude']}")
        print(f"longitude:: {vehicle_data['record']['location']['longitude']}")

        # Assuming end coordinates for Birmingham
        if (vehicle_data['record']['location']['latitude'] >= 52.4862
                and vehicle_data['record']['location']['longitude'] <= -1.8904):
            print('Vehicle has reached Birmingham. Simulation ending...')
            break

        send_account_data_to_kafka(vehicle_data)
        time.sleep(10)

if __name__ == "__main__":
    try:
        simulate_journey('Vehicle-CodeWithYu-123')
    except KeyboardInterrupt:
        print('Simulation ended by the user')
    except Exception as e:
        print(f'Unexpected Error occurred: {e}')