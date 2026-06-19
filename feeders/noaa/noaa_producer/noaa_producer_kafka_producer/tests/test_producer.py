# pylint: disable=missing-function-docstring, wrong-import-position, import-error, no-name-in-module, import-outside-toplevel, no-member, redefined-outer-name, unused-argument, unused-variable, invalid-name, redefined-outer-name, missing-class-docstring

import asyncio
import logging
import os
import sys
import datetime
from typing import Optional

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../noaa_producer_data/src')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../noaa_producer_data/tests')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../noaa_producer_kafka_producer/src')))

import tempfile
import pytest
from confluent_kafka import Producer, Consumer, KafkaException, Message
from confluent_kafka.admin import AdminClient, NewTopic
from cloudevents.abstract import CloudEvent
from cloudevents.kafka import from_binary, from_structured, KafkaMessage
from testcontainers.kafka import KafkaContainer
from noaa_producer_kafka_producer.producer import MicrosoftOpenDataUSNOAAEventProducer
from noaa_producer_data import WaterLevel
from test_waterlevel import Test_WaterLevel
from noaa_producer_data import Predictions
from test_predictions import Test_Predictions
from noaa_producer_data import AirPressure
from test_airpressure import Test_AirPressure
from noaa_producer_data import AirTemperature
from test_airtemperature import Test_AirTemperature
from noaa_producer_data import WaterTemperature
from test_watertemperature import Test_WaterTemperature
from noaa_producer_data import Wind
from test_wind import Test_Wind
from noaa_producer_data import Humidity
from test_humidity import Test_Humidity
from noaa_producer_data import Conductivity
from test_conductivity import Test_Conductivity
from noaa_producer_data import Salinity
from test_salinity import Test_Salinity
from noaa_producer_data import Station
from test_station import Test_Station
from noaa_producer_data import Visibility
from test_visibility import Test_Visibility
from noaa_producer_data import Currents
from test_currents import Test_Currents
from noaa_producer_data import CurrentPredictions
from test_currentpredictions import Test_CurrentPredictions
from noaa_producer_kafka_producer.producer import MicrosoftOpenDataUSNOAAMqttEventProducer
from noaa_producer_kafka_producer.producer import MicrosoftOpenDataUSNOAAAmqpEventProducer

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


def test_microsoft_opendata_us_noaa_microsoftopendatausnoaawaterlevel(kafka_emulator):
    """Test the MicrosoftOpenDataUSNOAAWaterLevel event from the Microsoft.OpenData.US.NOAA message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_microsoft_opendata_us_noaa_microsoftopendatausnoaawaterlevel',  # Unique group per test
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
                return None
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                continue
            cloudevent = parse_cloudevent(msg)
            if cloudevent['type'] == "Microsoft.OpenData.US.NOAA.WaterLevel":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = MicrosoftOpenDataUSNOAAEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_WaterLevel.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_microsoft_open_data_us_noaa_water_level(_station_id = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
        expected_key = "{station_id}".format(station_id=f'test_{i}')
        assert received_key == expected_key, f"Expected Kafka key '{expected_key}' but got '{received_key}'"
    consumer.close()


def test_microsoft_opendata_us_noaa_microsoftopendatausnoaapredictions(kafka_emulator):
    """Test the MicrosoftOpenDataUSNOAAPredictions event from the Microsoft.OpenData.US.NOAA message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_microsoft_opendata_us_noaa_microsoftopendatausnoaapredictions',  # Unique group per test
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
                return None
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                continue
            cloudevent = parse_cloudevent(msg)
            if cloudevent['type'] == "Microsoft.OpenData.US.NOAA.Predictions":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = MicrosoftOpenDataUSNOAAEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_Predictions.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_microsoft_open_data_us_noaa_predictions(_station_id = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
        expected_key = "{station_id}".format(station_id=f'test_{i}')
        assert received_key == expected_key, f"Expected Kafka key '{expected_key}' but got '{received_key}'"
    consumer.close()


def test_microsoft_opendata_us_noaa_microsoftopendatausnoaaairpressure(kafka_emulator):
    """Test the MicrosoftOpenDataUSNOAAAirPressure event from the Microsoft.OpenData.US.NOAA message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_microsoft_opendata_us_noaa_microsoftopendatausnoaaairpressure',  # Unique group per test
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
                return None
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                continue
            cloudevent = parse_cloudevent(msg)
            if cloudevent['type'] == "Microsoft.OpenData.US.NOAA.AirPressure":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = MicrosoftOpenDataUSNOAAEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_AirPressure.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_microsoft_open_data_us_noaa_air_pressure(_station_id = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
        expected_key = "{station_id}".format(station_id=f'test_{i}')
        assert received_key == expected_key, f"Expected Kafka key '{expected_key}' but got '{received_key}'"
    consumer.close()


def test_microsoft_opendata_us_noaa_microsoftopendatausnoaaairtemperature(kafka_emulator):
    """Test the MicrosoftOpenDataUSNOAAAirTemperature event from the Microsoft.OpenData.US.NOAA message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_microsoft_opendata_us_noaa_microsoftopendatausnoaaairtemperature',  # Unique group per test
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
                return None
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                continue
            cloudevent = parse_cloudevent(msg)
            if cloudevent['type'] == "Microsoft.OpenData.US.NOAA.AirTemperature":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = MicrosoftOpenDataUSNOAAEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_AirTemperature.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_microsoft_open_data_us_noaa_air_temperature(_station_id = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
        expected_key = "{station_id}".format(station_id=f'test_{i}')
        assert received_key == expected_key, f"Expected Kafka key '{expected_key}' but got '{received_key}'"
    consumer.close()


def test_microsoft_opendata_us_noaa_microsoftopendatausnoaawatertemperature(kafka_emulator):
    """Test the MicrosoftOpenDataUSNOAAWaterTemperature event from the Microsoft.OpenData.US.NOAA message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_microsoft_opendata_us_noaa_microsoftopendatausnoaawatertemperature',  # Unique group per test
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
                return None
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                continue
            cloudevent = parse_cloudevent(msg)
            if cloudevent['type'] == "Microsoft.OpenData.US.NOAA.WaterTemperature":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = MicrosoftOpenDataUSNOAAEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_WaterTemperature.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_microsoft_open_data_us_noaa_water_temperature(_station_id = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
        expected_key = "{station_id}".format(station_id=f'test_{i}')
        assert received_key == expected_key, f"Expected Kafka key '{expected_key}' but got '{received_key}'"
    consumer.close()


def test_microsoft_opendata_us_noaa_microsoftopendatausnoaawind(kafka_emulator):
    """Test the MicrosoftOpenDataUSNOAAWind event from the Microsoft.OpenData.US.NOAA message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_microsoft_opendata_us_noaa_microsoftopendatausnoaawind',  # Unique group per test
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
                return None
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                continue
            cloudevent = parse_cloudevent(msg)
            if cloudevent['type'] == "Microsoft.OpenData.US.NOAA.Wind":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = MicrosoftOpenDataUSNOAAEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_Wind.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_microsoft_open_data_us_noaa_wind(_station_id = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
        expected_key = "{station_id}".format(station_id=f'test_{i}')
        assert received_key == expected_key, f"Expected Kafka key '{expected_key}' but got '{received_key}'"
    consumer.close()


def test_microsoft_opendata_us_noaa_microsoftopendatausnoaahumidity(kafka_emulator):
    """Test the MicrosoftOpenDataUSNOAAHumidity event from the Microsoft.OpenData.US.NOAA message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_microsoft_opendata_us_noaa_microsoftopendatausnoaahumidity',  # Unique group per test
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
                return None
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                continue
            cloudevent = parse_cloudevent(msg)
            if cloudevent['type'] == "Microsoft.OpenData.US.NOAA.Humidity":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = MicrosoftOpenDataUSNOAAEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_Humidity.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_microsoft_open_data_us_noaa_humidity(_station_id = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
        expected_key = "{station_id}".format(station_id=f'test_{i}')
        assert received_key == expected_key, f"Expected Kafka key '{expected_key}' but got '{received_key}'"
    consumer.close()


def test_microsoft_opendata_us_noaa_microsoftopendatausnoaaconductivity(kafka_emulator):
    """Test the MicrosoftOpenDataUSNOAAConductivity event from the Microsoft.OpenData.US.NOAA message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_microsoft_opendata_us_noaa_microsoftopendatausnoaaconductivity',  # Unique group per test
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
                return None
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                continue
            cloudevent = parse_cloudevent(msg)
            if cloudevent['type'] == "Microsoft.OpenData.US.NOAA.Conductivity":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = MicrosoftOpenDataUSNOAAEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_Conductivity.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_microsoft_open_data_us_noaa_conductivity(_station_id = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
        expected_key = "{station_id}".format(station_id=f'test_{i}')
        assert received_key == expected_key, f"Expected Kafka key '{expected_key}' but got '{received_key}'"
    consumer.close()


def test_microsoft_opendata_us_noaa_microsoftopendatausnoaasalinity(kafka_emulator):
    """Test the MicrosoftOpenDataUSNOAASalinity event from the Microsoft.OpenData.US.NOAA message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_microsoft_opendata_us_noaa_microsoftopendatausnoaasalinity',  # Unique group per test
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
                return None
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                continue
            cloudevent = parse_cloudevent(msg)
            if cloudevent['type'] == "Microsoft.OpenData.US.NOAA.Salinity":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = MicrosoftOpenDataUSNOAAEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_Salinity.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_microsoft_open_data_us_noaa_salinity(_station_id = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
        expected_key = "{station_id}".format(station_id=f'test_{i}')
        assert received_key == expected_key, f"Expected Kafka key '{expected_key}' but got '{received_key}'"
    consumer.close()


def test_microsoft_opendata_us_noaa_microsoftopendatausnoaastation(kafka_emulator):
    """Test the MicrosoftOpenDataUSNOAAStation event from the Microsoft.OpenData.US.NOAA message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_microsoft_opendata_us_noaa_microsoftopendatausnoaastation',  # Unique group per test
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
                return None
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                continue
            cloudevent = parse_cloudevent(msg)
            if cloudevent['type'] == "Microsoft.OpenData.US.NOAA.Station":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = MicrosoftOpenDataUSNOAAEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_Station.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_microsoft_open_data_us_noaa_station(_station_id = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
        expected_key = "{station_id}".format(station_id=f'test_{i}')
        assert received_key == expected_key, f"Expected Kafka key '{expected_key}' but got '{received_key}'"
    consumer.close()


def test_microsoft_opendata_us_noaa_microsoftopendatausnoaavisibility(kafka_emulator):
    """Test the MicrosoftOpenDataUSNOAAVisibility event from the Microsoft.OpenData.US.NOAA message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_microsoft_opendata_us_noaa_microsoftopendatausnoaavisibility',  # Unique group per test
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
                return None
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                continue
            cloudevent = parse_cloudevent(msg)
            if cloudevent['type'] == "Microsoft.OpenData.US.NOAA.Visibility":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = MicrosoftOpenDataUSNOAAEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_Visibility.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_microsoft_open_data_us_noaa_visibility(_datacontenttype = f'test_{i}',_dataschema = f'test_{i}',_station_id = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
        expected_key = "{station_id}".format(station_id=f'test_{i}')
        assert received_key == expected_key, f"Expected Kafka key '{expected_key}' but got '{received_key}'"
    consumer.close()


def test_microsoft_opendata_us_noaa_microsoftopendatausnoaacurrents(kafka_emulator):
    """Test the MicrosoftOpenDataUSNOAACurrents event from the Microsoft.OpenData.US.NOAA message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_microsoft_opendata_us_noaa_microsoftopendatausnoaacurrents',  # Unique group per test
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
                return None
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                continue
            cloudevent = parse_cloudevent(msg)
            if cloudevent['type'] == "Microsoft.OpenData.US.NOAA.Currents":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = MicrosoftOpenDataUSNOAAEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_Currents.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_microsoft_open_data_us_noaa_currents(_station_id = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
        expected_key = "{station_id}".format(station_id=f'test_{i}')
        assert received_key == expected_key, f"Expected Kafka key '{expected_key}' but got '{received_key}'"
    consumer.close()


def test_microsoft_opendata_us_noaa_microsoftopendatausnoaacurrentpredictions(kafka_emulator):
    """Test the MicrosoftOpenDataUSNOAACurrentPredictions event from the Microsoft.OpenData.US.NOAA message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_microsoft_opendata_us_noaa_microsoftopendatausnoaacurrentpredictions',  # Unique group per test
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
                return None
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                continue
            cloudevent = parse_cloudevent(msg)
            if cloudevent['type'] == "Microsoft.OpenData.US.NOAA.CurrentPredictions":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = MicrosoftOpenDataUSNOAAEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_CurrentPredictions.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_microsoft_open_data_us_noaa_current_predictions(_station_id = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
        expected_key = "{station_id}".format(station_id=f'test_{i}')
        assert received_key == expected_key, f"Expected Kafka key '{expected_key}' but got '{received_key}'"
    consumer.close()


def test_microsoft_opendata_us_noaa_mqtt_microsoftopendatausnoaamqttwaterlevel(kafka_emulator):
    """Test the MicrosoftOpenDataUSNOAAMqttWaterLevel event from the Microsoft.OpenData.US.NOAA.Mqtt message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_microsoft_opendata_us_noaa_mqtt_microsoftopendatausnoaamqttwaterlevel',  # Unique group per test
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
                return None
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                continue
            cloudevent = parse_cloudevent(msg)
            if cloudevent['type'] == "Microsoft.OpenData.US.NOAA.WaterLevel":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = MicrosoftOpenDataUSNOAAMqttEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_WaterLevel.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_microsoft_open_data_us_noaa_mqtt_water_level(_station_id = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
    consumer.close()


def test_microsoft_opendata_us_noaa_mqtt_microsoftopendatausnoaamqttpredictions(kafka_emulator):
    """Test the MicrosoftOpenDataUSNOAAMqttPredictions event from the Microsoft.OpenData.US.NOAA.Mqtt message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_microsoft_opendata_us_noaa_mqtt_microsoftopendatausnoaamqttpredictions',  # Unique group per test
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
                return None
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                continue
            cloudevent = parse_cloudevent(msg)
            if cloudevent['type'] == "Microsoft.OpenData.US.NOAA.Predictions":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = MicrosoftOpenDataUSNOAAMqttEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_Predictions.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_microsoft_open_data_us_noaa_mqtt_predictions(_station_id = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
    consumer.close()


def test_microsoft_opendata_us_noaa_mqtt_microsoftopendatausnoaamqttairpressure(kafka_emulator):
    """Test the MicrosoftOpenDataUSNOAAMqttAirPressure event from the Microsoft.OpenData.US.NOAA.Mqtt message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_microsoft_opendata_us_noaa_mqtt_microsoftopendatausnoaamqttairpressure',  # Unique group per test
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
                return None
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                continue
            cloudevent = parse_cloudevent(msg)
            if cloudevent['type'] == "Microsoft.OpenData.US.NOAA.AirPressure":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = MicrosoftOpenDataUSNOAAMqttEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_AirPressure.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_microsoft_open_data_us_noaa_mqtt_air_pressure(_station_id = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
    consumer.close()


def test_microsoft_opendata_us_noaa_mqtt_microsoftopendatausnoaamqttairtemperature(kafka_emulator):
    """Test the MicrosoftOpenDataUSNOAAMqttAirTemperature event from the Microsoft.OpenData.US.NOAA.Mqtt message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_microsoft_opendata_us_noaa_mqtt_microsoftopendatausnoaamqttairtemperature',  # Unique group per test
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
                return None
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                continue
            cloudevent = parse_cloudevent(msg)
            if cloudevent['type'] == "Microsoft.OpenData.US.NOAA.AirTemperature":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = MicrosoftOpenDataUSNOAAMqttEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_AirTemperature.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_microsoft_open_data_us_noaa_mqtt_air_temperature(_station_id = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
    consumer.close()


def test_microsoft_opendata_us_noaa_mqtt_microsoftopendatausnoaamqttwatertemperature(kafka_emulator):
    """Test the MicrosoftOpenDataUSNOAAMqttWaterTemperature event from the Microsoft.OpenData.US.NOAA.Mqtt message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_microsoft_opendata_us_noaa_mqtt_microsoftopendatausnoaamqttwatertemperature',  # Unique group per test
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
                return None
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                continue
            cloudevent = parse_cloudevent(msg)
            if cloudevent['type'] == "Microsoft.OpenData.US.NOAA.WaterTemperature":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = MicrosoftOpenDataUSNOAAMqttEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_WaterTemperature.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_microsoft_open_data_us_noaa_mqtt_water_temperature(_station_id = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
    consumer.close()


def test_microsoft_opendata_us_noaa_mqtt_microsoftopendatausnoaamqttwind(kafka_emulator):
    """Test the MicrosoftOpenDataUSNOAAMqttWind event from the Microsoft.OpenData.US.NOAA.Mqtt message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_microsoft_opendata_us_noaa_mqtt_microsoftopendatausnoaamqttwind',  # Unique group per test
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
                return None
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                continue
            cloudevent = parse_cloudevent(msg)
            if cloudevent['type'] == "Microsoft.OpenData.US.NOAA.Wind":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = MicrosoftOpenDataUSNOAAMqttEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_Wind.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_microsoft_open_data_us_noaa_mqtt_wind(_station_id = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
    consumer.close()


def test_microsoft_opendata_us_noaa_mqtt_microsoftopendatausnoaamqtthumidity(kafka_emulator):
    """Test the MicrosoftOpenDataUSNOAAMqttHumidity event from the Microsoft.OpenData.US.NOAA.Mqtt message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_microsoft_opendata_us_noaa_mqtt_microsoftopendatausnoaamqtthumidity',  # Unique group per test
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
                return None
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                continue
            cloudevent = parse_cloudevent(msg)
            if cloudevent['type'] == "Microsoft.OpenData.US.NOAA.Humidity":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = MicrosoftOpenDataUSNOAAMqttEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_Humidity.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_microsoft_open_data_us_noaa_mqtt_humidity(_station_id = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
    consumer.close()


def test_microsoft_opendata_us_noaa_mqtt_microsoftopendatausnoaamqttconductivity(kafka_emulator):
    """Test the MicrosoftOpenDataUSNOAAMqttConductivity event from the Microsoft.OpenData.US.NOAA.Mqtt message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_microsoft_opendata_us_noaa_mqtt_microsoftopendatausnoaamqttconductivity',  # Unique group per test
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
                return None
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                continue
            cloudevent = parse_cloudevent(msg)
            if cloudevent['type'] == "Microsoft.OpenData.US.NOAA.Conductivity":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = MicrosoftOpenDataUSNOAAMqttEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_Conductivity.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_microsoft_open_data_us_noaa_mqtt_conductivity(_station_id = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
    consumer.close()


def test_microsoft_opendata_us_noaa_mqtt_microsoftopendatausnoaamqttsalinity(kafka_emulator):
    """Test the MicrosoftOpenDataUSNOAAMqttSalinity event from the Microsoft.OpenData.US.NOAA.Mqtt message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_microsoft_opendata_us_noaa_mqtt_microsoftopendatausnoaamqttsalinity',  # Unique group per test
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
                return None
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                continue
            cloudevent = parse_cloudevent(msg)
            if cloudevent['type'] == "Microsoft.OpenData.US.NOAA.Salinity":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = MicrosoftOpenDataUSNOAAMqttEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_Salinity.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_microsoft_open_data_us_noaa_mqtt_salinity(_station_id = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
    consumer.close()


def test_microsoft_opendata_us_noaa_mqtt_microsoftopendatausnoaamqttstation(kafka_emulator):
    """Test the MicrosoftOpenDataUSNOAAMqttStation event from the Microsoft.OpenData.US.NOAA.Mqtt message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_microsoft_opendata_us_noaa_mqtt_microsoftopendatausnoaamqttstation',  # Unique group per test
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
                return None
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                continue
            cloudevent = parse_cloudevent(msg)
            if cloudevent['type'] == "Microsoft.OpenData.US.NOAA.Station":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = MicrosoftOpenDataUSNOAAMqttEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_Station.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_microsoft_open_data_us_noaa_mqtt_station(_station_id = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
    consumer.close()


def test_microsoft_opendata_us_noaa_mqtt_microsoftopendatausnoaamqttvisibility(kafka_emulator):
    """Test the MicrosoftOpenDataUSNOAAMqttVisibility event from the Microsoft.OpenData.US.NOAA.Mqtt message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_microsoft_opendata_us_noaa_mqtt_microsoftopendatausnoaamqttvisibility',  # Unique group per test
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
                return None
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                continue
            cloudevent = parse_cloudevent(msg)
            if cloudevent['type'] == "Microsoft.OpenData.US.NOAA.Visibility":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = MicrosoftOpenDataUSNOAAMqttEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_Visibility.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_microsoft_open_data_us_noaa_mqtt_visibility(_datacontenttype = f'test_{i}',_dataschema = f'test_{i}',_station_id = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
    consumer.close()


def test_microsoft_opendata_us_noaa_mqtt_microsoftopendatausnoaamqttcurrents(kafka_emulator):
    """Test the MicrosoftOpenDataUSNOAAMqttCurrents event from the Microsoft.OpenData.US.NOAA.Mqtt message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_microsoft_opendata_us_noaa_mqtt_microsoftopendatausnoaamqttcurrents',  # Unique group per test
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
                return None
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                continue
            cloudevent = parse_cloudevent(msg)
            if cloudevent['type'] == "Microsoft.OpenData.US.NOAA.Currents":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = MicrosoftOpenDataUSNOAAMqttEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_Currents.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_microsoft_open_data_us_noaa_mqtt_currents(_station_id = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
    consumer.close()


def test_microsoft_opendata_us_noaa_mqtt_microsoftopendatausnoaamqttcurrentpredictions(kafka_emulator):
    """Test the MicrosoftOpenDataUSNOAAMqttCurrentPredictions event from the Microsoft.OpenData.US.NOAA.Mqtt message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_microsoft_opendata_us_noaa_mqtt_microsoftopendatausnoaamqttcurrentpredictions',  # Unique group per test
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
                return None
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                continue
            cloudevent = parse_cloudevent(msg)
            if cloudevent['type'] == "Microsoft.OpenData.US.NOAA.CurrentPredictions":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = MicrosoftOpenDataUSNOAAMqttEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_CurrentPredictions.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_microsoft_open_data_us_noaa_mqtt_current_predictions(_station_id = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
    consumer.close()


def test_microsoft_opendata_us_noaa_amqp_microsoftopendatausnoaaamqpwaterlevel(kafka_emulator):
    """Test the MicrosoftOpenDataUSNOAAAmqpWaterLevel event from the Microsoft.OpenData.US.NOAA.Amqp message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_microsoft_opendata_us_noaa_amqp_microsoftopendatausnoaaamqpwaterlevel',  # Unique group per test
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
                return None
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                continue
            cloudevent = parse_cloudevent(msg)
            if cloudevent['type'] == "Microsoft.OpenData.US.NOAA.WaterLevel":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = MicrosoftOpenDataUSNOAAAmqpEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_WaterLevel.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_microsoft_open_data_us_noaa_amqp_water_level(_station_id = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
    consumer.close()


def test_microsoft_opendata_us_noaa_amqp_microsoftopendatausnoaaamqppredictions(kafka_emulator):
    """Test the MicrosoftOpenDataUSNOAAAmqpPredictions event from the Microsoft.OpenData.US.NOAA.Amqp message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_microsoft_opendata_us_noaa_amqp_microsoftopendatausnoaaamqppredictions',  # Unique group per test
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
                return None
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                continue
            cloudevent = parse_cloudevent(msg)
            if cloudevent['type'] == "Microsoft.OpenData.US.NOAA.Predictions":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = MicrosoftOpenDataUSNOAAAmqpEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_Predictions.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_microsoft_open_data_us_noaa_amqp_predictions(_station_id = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
    consumer.close()


def test_microsoft_opendata_us_noaa_amqp_microsoftopendatausnoaaamqpairpressure(kafka_emulator):
    """Test the MicrosoftOpenDataUSNOAAAmqpAirPressure event from the Microsoft.OpenData.US.NOAA.Amqp message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_microsoft_opendata_us_noaa_amqp_microsoftopendatausnoaaamqpairpressure',  # Unique group per test
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
                return None
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                continue
            cloudevent = parse_cloudevent(msg)
            if cloudevent['type'] == "Microsoft.OpenData.US.NOAA.AirPressure":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = MicrosoftOpenDataUSNOAAAmqpEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_AirPressure.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_microsoft_open_data_us_noaa_amqp_air_pressure(_station_id = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
    consumer.close()


def test_microsoft_opendata_us_noaa_amqp_microsoftopendatausnoaaamqpairtemperature(kafka_emulator):
    """Test the MicrosoftOpenDataUSNOAAAmqpAirTemperature event from the Microsoft.OpenData.US.NOAA.Amqp message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_microsoft_opendata_us_noaa_amqp_microsoftopendatausnoaaamqpairtemperature',  # Unique group per test
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
                return None
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                continue
            cloudevent = parse_cloudevent(msg)
            if cloudevent['type'] == "Microsoft.OpenData.US.NOAA.AirTemperature":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = MicrosoftOpenDataUSNOAAAmqpEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_AirTemperature.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_microsoft_open_data_us_noaa_amqp_air_temperature(_station_id = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
    consumer.close()


def test_microsoft_opendata_us_noaa_amqp_microsoftopendatausnoaaamqpwatertemperature(kafka_emulator):
    """Test the MicrosoftOpenDataUSNOAAAmqpWaterTemperature event from the Microsoft.OpenData.US.NOAA.Amqp message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_microsoft_opendata_us_noaa_amqp_microsoftopendatausnoaaamqpwatertemperature',  # Unique group per test
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
                return None
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                continue
            cloudevent = parse_cloudevent(msg)
            if cloudevent['type'] == "Microsoft.OpenData.US.NOAA.WaterTemperature":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = MicrosoftOpenDataUSNOAAAmqpEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_WaterTemperature.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_microsoft_open_data_us_noaa_amqp_water_temperature(_station_id = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
    consumer.close()


def test_microsoft_opendata_us_noaa_amqp_microsoftopendatausnoaaamqpwind(kafka_emulator):
    """Test the MicrosoftOpenDataUSNOAAAmqpWind event from the Microsoft.OpenData.US.NOAA.Amqp message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_microsoft_opendata_us_noaa_amqp_microsoftopendatausnoaaamqpwind',  # Unique group per test
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
                return None
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                continue
            cloudevent = parse_cloudevent(msg)
            if cloudevent['type'] == "Microsoft.OpenData.US.NOAA.Wind":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = MicrosoftOpenDataUSNOAAAmqpEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_Wind.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_microsoft_open_data_us_noaa_amqp_wind(_station_id = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
    consumer.close()


def test_microsoft_opendata_us_noaa_amqp_microsoftopendatausnoaaamqphumidity(kafka_emulator):
    """Test the MicrosoftOpenDataUSNOAAAmqpHumidity event from the Microsoft.OpenData.US.NOAA.Amqp message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_microsoft_opendata_us_noaa_amqp_microsoftopendatausnoaaamqphumidity',  # Unique group per test
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
                return None
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                continue
            cloudevent = parse_cloudevent(msg)
            if cloudevent['type'] == "Microsoft.OpenData.US.NOAA.Humidity":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = MicrosoftOpenDataUSNOAAAmqpEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_Humidity.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_microsoft_open_data_us_noaa_amqp_humidity(_station_id = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
    consumer.close()


def test_microsoft_opendata_us_noaa_amqp_microsoftopendatausnoaaamqpconductivity(kafka_emulator):
    """Test the MicrosoftOpenDataUSNOAAAmqpConductivity event from the Microsoft.OpenData.US.NOAA.Amqp message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_microsoft_opendata_us_noaa_amqp_microsoftopendatausnoaaamqpconductivity',  # Unique group per test
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
                return None
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                continue
            cloudevent = parse_cloudevent(msg)
            if cloudevent['type'] == "Microsoft.OpenData.US.NOAA.Conductivity":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = MicrosoftOpenDataUSNOAAAmqpEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_Conductivity.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_microsoft_open_data_us_noaa_amqp_conductivity(_station_id = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
    consumer.close()


def test_microsoft_opendata_us_noaa_amqp_microsoftopendatausnoaaamqpsalinity(kafka_emulator):
    """Test the MicrosoftOpenDataUSNOAAAmqpSalinity event from the Microsoft.OpenData.US.NOAA.Amqp message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_microsoft_opendata_us_noaa_amqp_microsoftopendatausnoaaamqpsalinity',  # Unique group per test
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
                return None
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                continue
            cloudevent = parse_cloudevent(msg)
            if cloudevent['type'] == "Microsoft.OpenData.US.NOAA.Salinity":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = MicrosoftOpenDataUSNOAAAmqpEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_Salinity.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_microsoft_open_data_us_noaa_amqp_salinity(_station_id = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
    consumer.close()


def test_microsoft_opendata_us_noaa_amqp_microsoftopendatausnoaaamqpstation(kafka_emulator):
    """Test the MicrosoftOpenDataUSNOAAAmqpStation event from the Microsoft.OpenData.US.NOAA.Amqp message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_microsoft_opendata_us_noaa_amqp_microsoftopendatausnoaaamqpstation',  # Unique group per test
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
                return None
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                continue
            cloudevent = parse_cloudevent(msg)
            if cloudevent['type'] == "Microsoft.OpenData.US.NOAA.Station":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = MicrosoftOpenDataUSNOAAAmqpEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_Station.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_microsoft_open_data_us_noaa_amqp_station(_station_id = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
    consumer.close()


def test_microsoft_opendata_us_noaa_amqp_microsoftopendatausnoaaamqpvisibility(kafka_emulator):
    """Test the MicrosoftOpenDataUSNOAAAmqpVisibility event from the Microsoft.OpenData.US.NOAA.Amqp message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_microsoft_opendata_us_noaa_amqp_microsoftopendatausnoaaamqpvisibility',  # Unique group per test
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
                return None
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                continue
            cloudevent = parse_cloudevent(msg)
            if cloudevent['type'] == "Microsoft.OpenData.US.NOAA.Visibility":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = MicrosoftOpenDataUSNOAAAmqpEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_Visibility.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_microsoft_open_data_us_noaa_amqp_visibility(_datacontenttype = f'test_{i}',_dataschema = f'test_{i}',_station_id = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
    consumer.close()


def test_microsoft_opendata_us_noaa_amqp_microsoftopendatausnoaaamqpcurrents(kafka_emulator):
    """Test the MicrosoftOpenDataUSNOAAAmqpCurrents event from the Microsoft.OpenData.US.NOAA.Amqp message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_microsoft_opendata_us_noaa_amqp_microsoftopendatausnoaaamqpcurrents',  # Unique group per test
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
                return None
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                continue
            cloudevent = parse_cloudevent(msg)
            if cloudevent['type'] == "Microsoft.OpenData.US.NOAA.Currents":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = MicrosoftOpenDataUSNOAAAmqpEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_Currents.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_microsoft_open_data_us_noaa_amqp_currents(_station_id = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
    consumer.close()


def test_microsoft_opendata_us_noaa_amqp_microsoftopendatausnoaaamqpcurrentpredictions(kafka_emulator):
    """Test the MicrosoftOpenDataUSNOAAAmqpCurrentPredictions event from the Microsoft.OpenData.US.NOAA.Amqp message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_microsoft_opendata_us_noaa_amqp_microsoftopendatausnoaaamqpcurrentpredictions',  # Unique group per test
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
                return None
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                continue
            cloudevent = parse_cloudevent(msg)
            if cloudevent['type'] == "Microsoft.OpenData.US.NOAA.CurrentPredictions":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = MicrosoftOpenDataUSNOAAAmqpEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_CurrentPredictions.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_microsoft_open_data_us_noaa_amqp_current_predictions(_station_id = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
    consumer.close()


def test_microsoft_opendata_us_noaa_cross_event_type_kafka_key(kafka_emulator):
    """Test that different event types in Microsoft.OpenData.US.NOAA produce the same Kafka key for the same placeholder values"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_microsoft_opendata_us_noaa_cross_key',
        'auto.offset.reset': 'latest'
    })
    consumer.subscribe([topic])

    import time
    assignment_timeout = time.time() + 10
    while not consumer.assignment() and time.time() < assignment_timeout:
        consumer.poll(0.1)
    if not consumer.assignment():
        pytest.fail(f"Consumer failed to get partition assignment within 10 seconds. Topic: {topic}")
    # Drain any pre-existing messages before producing our test messages
    drain_timeout = time.time() + 3
    while time.time() < drain_timeout:
        msg = consumer.poll(0.5)
    time.sleep(1)

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = MicrosoftOpenDataUSNOAAEventProducer(kafka_producer, topic, 'binary')

    shared_key_value = "shared_entity_42"
    data1 = Test_WaterLevel.create_instance()
    data2 = Test_Predictions.create_instance()

    producer_instance.send_microsoft_open_data_us_noaa_water_level(_station_id = shared_key_value, data = data1)
    producer_instance.send_microsoft_open_data_us_noaa_predictions(_station_id = shared_key_value, data = data2)
    kafka_producer.flush(timeout=5.0)

    # Collect keys from both messages
    collected_keys = []
    timeout = time.time() + 20
    while len(collected_keys) < 2 and time.time() < timeout:
        msg = consumer.poll(1.0)
        if msg is None or msg.error():
            continue
        cloudevent = parse_cloudevent(msg)
        if cloudevent['type'] in ["Microsoft.OpenData.US.NOAA.WaterLevel", "Microsoft.OpenData.US.NOAA.Predictions"]:
            key = msg.key().decode('utf-8') if msg.key() else None
            collected_keys.append(key)

    assert len(collected_keys) == 2, f"Expected 2 messages but received {len(collected_keys)}"
    assert collected_keys[0] == collected_keys[1], \
        f"Expected same Kafka key for different event types but got '{collected_keys[0]}' and '{collected_keys[1]}'"
    expected_key = "{station_id}".format(station_id=shared_key_value)
    assert collected_keys[0] == expected_key, \
        f"Expected Kafka key '{expected_key}' but got '{collected_keys[0]}'"
    consumer.close()