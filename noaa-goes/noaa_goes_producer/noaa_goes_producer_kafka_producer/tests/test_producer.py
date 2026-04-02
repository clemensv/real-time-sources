# pylint: disable=missing-function-docstring, wrong-import-position, import-error, no-name-in-module, import-outside-toplevel, no-member, redefined-outer-name, unused-argument, unused-variable, invalid-name, redefined-outer-name, missing-class-docstring

import asyncio
import logging
import os
import sys
import datetime
from typing import Optional

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../noaa_goes_producer_data/src')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../noaa_goes_producer_data/tests')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../noaa_goes_producer_kafka_producer/src')))

import tempfile
import pytest
from confluent_kafka import Producer, Consumer, KafkaException, Message
from confluent_kafka.admin import AdminClient, NewTopic
from cloudevents.abstract import CloudEvent
from cloudevents.kafka import from_binary, from_structured, KafkaMessage
from testcontainers.kafka import KafkaContainer
from noaa_goes_producer_kafka_producer.producer import MicrosoftOpenDataUSNOAASWPCEventProducer
from noaa_goes_producer_data import SpaceWeatherAlert
from test_noaa_goes_producer_data_spaceweatheralert import Test_SpaceWeatherAlert
from noaa_goes_producer_data import PlanetaryKIndex
from test_noaa_goes_producer_data_planetarykindex import Test_PlanetaryKIndex
from noaa_goes_producer_data import SolarWindSummary
from test_noaa_goes_producer_data_solarwindsummary import Test_SolarWindSummary

@pytest.fixture(scope="module")
def kafka_emulator():
    with KafkaContainer() as kafka:
        admin_client = AdminClient({'bootstrap.servers': kafka.get_bootstrap_server()})
        topic_list = [
            NewTopic("test_topic", num_partitions=1, replication_factor=1)
        ]
        admin_client.create_topics(topic_list)

        yield {
            "bootstrap_servers": kafka.get_bootstrap_server(),
            "topic": "test_topic",
        }

def parse_cloudevent(msg: Message) -> CloudEvent:
    headers_dict: Dict[str, bytes] = {header[0]: header[1] for header in msg.headers()}
    message = KafkaMessage(headers=headers_dict, key=msg.key(), value=msg.value())
    if message.headers and 'content-type' in message.headers:
        content_type = message.headers['content-type'].decode()
        if content_type.startswith('application/cloudevents'):
            ce = from_structured(message)
            if 'datacontenttype' not in ce:
                ce['datacontenttype'] = 'application/json'
        else:
            ce = from_binary(message)
            ce['datacontenttype'] = message.headers['content-type'].decode()
    else:
        ce = from_binary(message)
        ce['datacontenttype'] = 'application/json'
    return ce

def test_microsoft_opendata_us_noaa_swpc_microsoftopendatausnoaaswpcspaceweatheralert(kafka_emulator):
    """Test the MicrosoftOpenDataUSNOAASWPCSpaceWeatherAlert event from the Microsoft.OpenData.US.NOAA.SWPC message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_microsoft_opendata_us_noaa_swpc_microsoftopendatausnoaaswpcspaceweatheralert',  # Unique group per test
        'auto.offset.reset': 'earliest'
    })
    consumer.subscribe([topic])
    
    # Wait for partition assignment before producing messages
    import time
    assignment_timeout = time.time() + 10
    while not consumer.assignment() and time.time() < assignment_timeout:
        consumer.poll(0.1)
    
    # Verify partition assignment succeeded
    if not consumer.assignment():
        pytest.fail(f"Consumer failed to get partition assignment within 10 seconds. Topic: {topic}")
    
    # Give consumer time to stabilize and seek to beginning
    time.sleep(1)

    def on_event():
        import time
        timeout = time.time() + 20  # 20 second timeout for CI robustness
        while True:
            if time.time() > timeout:
                return False
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                continue
            cloudevent = parse_cloudevent(msg)
            if cloudevent['type'] == "Microsoft.OpenData.US.NOAA.SWPC.SpaceWeatherAlert":
                return True

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = MicrosoftOpenDataUSNOAASWPCEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_SpaceWeatherAlert.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_microsoft_open_data_us_noaa_swpc_space_weather_alert(data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received
    for i in range(5):
        assert on_event(), f"Failed to receive message {i+1} of 5"
    consumer.close()

def test_microsoft_opendata_us_noaa_swpc_microsoftopendatausnoaaswpcplanetarykindex(kafka_emulator):
    """Test the MicrosoftOpenDataUSNOAASWPCPlanetaryKIndex event from the Microsoft.OpenData.US.NOAA.SWPC message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_microsoft_opendata_us_noaa_swpc_microsoftopendatausnoaaswpcplanetarykindex',  # Unique group per test
        'auto.offset.reset': 'earliest'
    })
    consumer.subscribe([topic])
    
    # Wait for partition assignment before producing messages
    import time
    assignment_timeout = time.time() + 10
    while not consumer.assignment() and time.time() < assignment_timeout:
        consumer.poll(0.1)
    
    # Verify partition assignment succeeded
    if not consumer.assignment():
        pytest.fail(f"Consumer failed to get partition assignment within 10 seconds. Topic: {topic}")
    
    # Give consumer time to stabilize and seek to beginning
    time.sleep(1)

    def on_event():
        import time
        timeout = time.time() + 20  # 20 second timeout for CI robustness
        while True:
            if time.time() > timeout:
                return False
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                continue
            cloudevent = parse_cloudevent(msg)
            if cloudevent['type'] == "Microsoft.OpenData.US.NOAA.SWPC.PlanetaryKIndex":
                return True

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = MicrosoftOpenDataUSNOAASWPCEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_PlanetaryKIndex.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_microsoft_open_data_us_noaa_swpc_planetary_kindex(data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received
    for i in range(5):
        assert on_event(), f"Failed to receive message {i+1} of 5"
    consumer.close()

def test_microsoft_opendata_us_noaa_swpc_microsoftopendatausnoaaswpcsolarwindsummary(kafka_emulator):
    """Test the MicrosoftOpenDataUSNOAASWPCSolarWindSummary event from the Microsoft.OpenData.US.NOAA.SWPC message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_microsoft_opendata_us_noaa_swpc_microsoftopendatausnoaaswpcsolarwindsummary',  # Unique group per test
        'auto.offset.reset': 'earliest'
    })
    consumer.subscribe([topic])
    
    # Wait for partition assignment before producing messages
    import time
    assignment_timeout = time.time() + 10
    while not consumer.assignment() and time.time() < assignment_timeout:
        consumer.poll(0.1)
    
    # Verify partition assignment succeeded
    if not consumer.assignment():
        pytest.fail(f"Consumer failed to get partition assignment within 10 seconds. Topic: {topic}")
    
    # Give consumer time to stabilize and seek to beginning
    time.sleep(1)

    def on_event():
        import time
        timeout = time.time() + 20  # 20 second timeout for CI robustness
        while True:
            if time.time() > timeout:
                return False
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                continue
            cloudevent = parse_cloudevent(msg)
            if cloudevent['type'] == "Microsoft.OpenData.US.NOAA.SWPC.SolarWindSummary":
                return True

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = MicrosoftOpenDataUSNOAASWPCEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_SolarWindSummary.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_microsoft_open_data_us_noaa_swpc_solar_wind_summary(data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received
    for i in range(5):
        assert on_event(), f"Failed to receive message {i+1} of 5"
    consumer.close()