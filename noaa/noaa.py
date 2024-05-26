import requests
import time
import os
import json
from datetime import datetime, timedelta
from confluent_kafka import Producer
from cloudevents.http import CloudEvent, to_structured
import argparse

NOAA_API_URLS = {
    "water_level": "https://api.tidesandcurrents.noaa.gov/api/prod/datagetter?product=water_level&units=metric&time_zone=gmt&application=web_services&format=json",
    "predictions": "https://api.tidesandcurrents.noaa.gov/api/prod/datagetter?product=predictions&units=metric&time_zone=gmt&application=web_services&format=json",
    "air_temperature": "https://api.tidesandcurrents.noaa.gov/api/prod/datagetter?product=air_temperature&units=metric&time_zone=gmt&application=web_services&format=json",
    "wind": "https://api.tidesandcurrents.noaa.gov/api/prod/datagetter?product=wind&units=metric&time_zone=gmt&application=web_services&format=json",
    "air_pressure": "https://api.tidesandcurrents.noaa.gov/api/prod/datagetter?product=air_pressure&units=metric&time_zone=gmt&application=web_services&format=json",
    "water_temperature": "https://api.tidesandcurrents.noaa.gov/api/prod/datagetter?product=water_temperature&units=metric&time_zone=gmt&application=web_services&format=json",
    "air_gap": "https://api.tidesandcurrents.noaa.gov/api/prod/datagetter?product=air_gap&units=metric&time_zone=gmt&application=web_services&format=json",
    "conductivity": "https://api.tidesandcurrents.noaa.gov/api/prod/datagetter?product=conductivity&units=metric&time_zone=gmt&application=web_services&format=json",
    "visibility": "https://api.tidesandcurrents.noaa.gov/api/prod/datagetter?product=visibility&units=metric&time_zone=gmt&application=web_services&format=json",
    "humidity": "https://api.tidesandcurrents.noaa.gov/api/prod/datagetter?product=humidity&units=metric&time_zone=gmt&application=web_services&format=json",
    "salinity": "https://api.tidesandcurrents.noaa.gov/api/prod/datagetter?product=salinity&units=metric&time_zone=gmt&application=web_services&format=json",
    "currents": "https://api.tidesandcurrents.noaa.gov/api/prod/datagetter?product=currents&units=metric&time_zone=gmt&application=web_services&format=json",
    "currents_predictions": "https://api.tidesandcurrents.noaa.gov/api/prod/datagetter?product=currents_predictions&units=metric&time_zone=gmt&application=web_services&format=json",
    "high_low": "https://api.tidesandcurrents.noaa.gov/api/prod/datagetter?product=high_low&units=metric&time_zone=gmt&application=web_services&format=json",
    "monthly_mean": "https://api.tidesandcurrents.noaa.gov/api/prod/datagetter?product=monthly_mean&units=metric&time_zone=gmt&application=web_services&format=json",
    "daily_mean": "https://api.tidesandcurrents.noaa.gov/api/prod/datagetter?product=daily_mean&units=metric&time_zone=gmt&application=web_services&format=json"
}

KAFKA_TOPIC = "noaa_data"
KAFKA_BOOTSTRAP_SERVERS = "localhost:9092"

producer = Producer({'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS})

def fetch_all_stations():
    url = "https://api.tidesandcurrents.noaa.gov/mdapi/prod/webapi/stations.json"
    try:
        response = requests.get(url)
        response.raise_for_status()
        stations_data = response.json()
        stations = [station['id'] for station in stations_data.get('stations', [])]
        currents_stations = [station['id'] for station in stations_data.get('stations', []) if station['type'] == 'C']
        return stations, currents_stations
    except requests.RequestException as e:
        print(f"Error fetching stations: {e}")
        return [], []

def poll_noaa_api(product_url, station_id, last_polled_time, data_key):
    try:
        response = requests.get(f"{product_url}&station={station_id}")
        response.raise_for_status()
        data = response.json().get(data_key, [])
        new_data = [record for record in data if datetime.strptime(record['t'], "%Y-%m-%d %H:%M") > last_polled_time]
        return new_data
    except requests.RequestException as e:
        print(f"Error fetching data for station {station_id}: {e}")
        return []

def create_cloud_event(data, source, event_type):
    attributes = {
        "type": event_type,
        "source": source,
        "time": datetime.utcnow().isoformat(),
        "id": str(data.get("t", "")),
        "datacontenttype": "application/json"
    }
    event = CloudEvent(attributes, data)
    headers, body = to_structured(event)
    return headers, body

def send_to_kafka(headers, body):
    try:
        producer.produce(KAFKA_TOPIC, key=headers["ce-id"], value=body, headers=headers.items())
        producer.flush()
    except Exception as e:
        print(f"Error sending data to Kafka: {e}")

def load_last_polled_times(filepath):
    if os.path.exists(filepath):
        with open(filepath, 'r') as file:
            return json.load(file)
    return {}

def save_last_polled_times(filepath, last_polled_times):
    with open(filepath, 'w') as file:
        json.dump(last_polled_times, file)

def poll_and_send(last_polled_file):
    stations, currents_stations = fetch_all_stations()
    last_polled_times = load_last_polled_times(last_polled_file)
    
    for product in NOAA_API_URLS:
        if product not in last_polled_times:
            last_polled_times[product] = {}
    
    while True:
        current_time = datetime.utcnow()
        for product, url in NOAA_API_URLS.items():
            data_key = "data" if "predictions" not in product else "predictions"
            station_list = currents_stations if "currents" in product else stations
            
            for station_id in station_list:
                last_polled_time = last_polled_times[product].get(station_id, datetime.utcnow() - timedelta(minutes=5))
                new_data_records = poll_noaa_api(url, station_id, last_polled_time, data_key)
                
                for record in new_data_records:
                    headers, body = create_cloud_event(record, url, f"com.noaa.{product}")
                    send_to_kafka(headers, body)
                
                if new_data_records:
                    last_polled_times[product][station_id] = current_time

        save_last_polled_times(last_polled_file, last_polled_times)
        time.sleep(300)  # Poll every 5 minutes

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="NOAA Data Poller")
    parser.add_argument('--last_polled_file', type=str, default=os.path.expanduser('~/.noaa_last_polled.json'),
                        help="File to store the last polled times for each station and product")
    args = parser.parse_args()

    poll_and_send(args.last_polled_file)