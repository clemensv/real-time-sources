import unittest
import requests_mock
import os
import json
from datetime import datetime, timedelta
from unittest.mock import patch
from confluent_kafka import Consumer, KafkaException
from testcontainers.kafka import KafkaContainer
from my_noaa_script import fetch_all_stations, poll_noaa_api, create_cloud_event, send_to_kafka, poll_and_send, load_last_polled_times, save_last_polled_times

class TestNOAAPoller(unittest.TestCase):

    @requests_mock.Mocker()
    def test_fetch_all_stations(self, m):
        with open('stations.json', 'r') as f:
            stations_json = json.load(f)
        
        m.get("https://api.tidesandcurrents.noaa.gov/mdapi/prod/webapi/stations.json", json=stations_json)
        stations, currents_stations = fetch_all_stations()
        
        self.assertGreater(len(stations), 0)
        self.assertGreater(len(currents_stations), 0)

    @requests_mock.Mocker()
    def test_poll_noaa_api(self, m):
        product_url = "https://api.tidesandcurrents.noaa.gov/api/prod/datagetter"
        station_id = "9414290"
        last_polled_time = datetime.utcnow() - timedelta(minutes=10)
        mock_response = {
            "data": [
                {"t": (datetime.utcnow() - timedelta(minutes=5)).strftime("%Y-%m-%d %H:%M"), "v": "0.5"}
            ]
        }

        m.get(f"{product_url}&station={station_id}", json=mock_response)
        data = poll_noaa_api(product_url, station_id, last_polled_time, "data")
        
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["v"], "0.5")

    def test_create_cloud_event(self):
        data = {"t": "2023-05-26 12:00", "v": "0.5"}
        source = "https://api.tidesandcurrents.noaa.gov/api/prod/datagetter"
        event_type = "com.noaa.water_level"
        
        headers, body = create_cloud_event(data, source, event_type)
        self.assertIn("ce-type", headers)
        self.assertIn("ce-source", headers)
        self.assertIn("ce-time", headers)
        self.assertIn("ce-id", headers)
        self.assertIn("content-type", headers)
        
        self.assertIn("t", json.loads(body))
        self.assertIn("v", json.loads(body))

    def test_load_last_polled_times(self):
        filepath = os.path.expanduser('~/.noaa_last_polled.json')
        data = {
            "water_level": {"9414290": "2023-05-26T12:00:00"}
        }
        with open(filepath, 'w') as f:
            json.dump(data, f)
        
        loaded_data = load_last_polled_times(filepath)
        self.assertEqual(loaded_data, data)
        os.remove(filepath)

    def test_save_last_polled_times(self):
        filepath = os.path.expanduser('~/.noaa_last_polled.json')
        data = {
            "water_level": {"9414290": "2023-05-26T12:00:00"}
        }
        save_last_polled_times(filepath, data)
        
        with open(filepath, 'r') as f:
            loaded_data = json.load(f)
        
        self.assertEqual(loaded_data, data)
        os.remove(filepath)

    @patch('my_noaa_script.producer')
    def test_send_to_kafka(self, mock_producer):
        data = {"t": "2023-05-26 12:00", "v": "0.5"}
        source = "https://api.tidesandcurrents.noaa.gov/api/prod/datagetter"
        event_type = "com.noaa.water_level"
        
        headers, body = create_cloud_event(data, source, event_type)
        send_to_kafka(headers, body)
        
        mock_producer.produce.assert_called_once()

    @unittest.skip("Integration test with Kafka")
    def test_poll_and_send(self):
        with KafkaContainer() as kafka:
            kafka_ip = kafka.get_container_host_ip()
            kafka_port = kafka.get_exposed_port(kafka.KAFKA_PORT)
            kafka_bootstrap_servers = f"{kafka_ip}:{kafka_port}"

            producer = Producer({'bootstrap.servers': kafka_bootstrap_servers})

            last_polled_file = os.path.expanduser('~/.noaa_last_polled.json')
            poll_and_send(last_polled_file)

            consumer = Consumer({
                'bootstrap.servers': kafka_bootstrap_servers,
                'group.id': 'test',
                'auto.offset.reset': 'earliest'
            })
            consumer.subscribe([KAFKA_TOPIC])

            msg = consumer.poll(10)
            self.assertIsNotNone(msg)
            self.assertIsNotNone(msg.value())

            consumer.close()
            os.remove(last_polled_file)

if __name__ == "__main__":
    unittest.main()