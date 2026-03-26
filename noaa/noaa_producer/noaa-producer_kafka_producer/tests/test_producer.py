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
from test_noaa_producer_data_microsoft_opendata_us_noaa_waterlevel import Test_WaterLevel
from noaa_producer_data import Predictions
from test_noaa_producer_data_microsoft_opendata_us_noaa_predictions import Test_Predictions
from noaa_producer_data import AirPressure
from test_noaa_producer_data_microsoft_opendata_us_noaa_airpressure import Test_AirPressure
from noaa_producer_data import AirTemperature
from test_noaa_producer_data_microsoft_opendata_us_noaa_airtemperature import Test_AirTemperature
from noaa_producer_data import WaterTemperature
from test_noaa_producer_data_microsoft_opendata_us_noaa_watertemperature import Test_WaterTemperature
from noaa_producer_data import Wind
from test_noaa_producer_data_microsoft_opendata_us_noaa_wind import Test_Wind
from noaa_producer_data import Humidity
from test_noaa_producer_data_microsoft_opendata_us_noaa_humidity import Test_Humidity
from noaa_producer_data import Conductivity
from test_noaa_producer_data_microsoft_opendata_us_noaa_conductivity import Test_Conductivity
from noaa_producer_data import Salinity
from test_noaa_producer_data_microsoft_opendata_us_noaa_salinity import Test_Salinity
from noaa_producer_data import Station
from test_noaa_producer_data_microsoft_opendata_us_noaa_station import Test_Station
from noaa_producer_data import Visibility
from test_noaa_producer_data_microsoft_opendata_us_noaa_visibility import Test_Visibility
from noaa_producer_data import Currents
from test_noaa_producer_data_microsoft_opendata_us_noaa_currents import Test_Currents
from noaa_producer_data import CurrentPredictions
from test_noaa_producer_data_microsoft_opendata_us_noaa_currentpredictions import Test_CurrentPredictions

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
                return False
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                continue
            cloudevent = parse_cloudevent(msg)
            if cloudevent['type'] == "Microsoft.OpenData.US.NOAA.WaterLevel":
                return True

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = MicrosoftOpenDataUSNOAAEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_WaterLevel.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_microsoft_open_data_us_noaa_water_level(data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received
    for i in range(5):
        assert on_event(), f"Failed to receive message {i+1} of 5"
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
                return False
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                continue
            cloudevent = parse_cloudevent(msg)
            if cloudevent['type'] == "Microsoft.OpenData.US.NOAA.Predictions":
                return True

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = MicrosoftOpenDataUSNOAAEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_Predictions.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_microsoft_open_data_us_noaa_predictions(data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received
    for i in range(5):
        assert on_event(), f"Failed to receive message {i+1} of 5"
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
                return False
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                continue
            cloudevent = parse_cloudevent(msg)
            if cloudevent['type'] == "Microsoft.OpenData.US.NOAA.AirPressure":
                return True

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = MicrosoftOpenDataUSNOAAEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_AirPressure.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_microsoft_open_data_us_noaa_air_pressure(data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received
    for i in range(5):
        assert on_event(), f"Failed to receive message {i+1} of 5"
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
                return False
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                continue
            cloudevent = parse_cloudevent(msg)
            if cloudevent['type'] == "Microsoft.OpenData.US.NOAA.AirTemperature":
                return True

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = MicrosoftOpenDataUSNOAAEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_AirTemperature.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_microsoft_open_data_us_noaa_air_temperature(data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received
    for i in range(5):
        assert on_event(), f"Failed to receive message {i+1} of 5"
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
                return False
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                continue
            cloudevent = parse_cloudevent(msg)
            if cloudevent['type'] == "Microsoft.OpenData.US.NOAA.WaterTemperature":
                return True

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = MicrosoftOpenDataUSNOAAEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_WaterTemperature.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_microsoft_open_data_us_noaa_water_temperature(data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received
    for i in range(5):
        assert on_event(), f"Failed to receive message {i+1} of 5"
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
                return False
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                continue
            cloudevent = parse_cloudevent(msg)
            if cloudevent['type'] == "Microsoft.OpenData.US.NOAA.Wind":
                return True

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = MicrosoftOpenDataUSNOAAEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_Wind.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_microsoft_open_data_us_noaa_wind(data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received
    for i in range(5):
        assert on_event(), f"Failed to receive message {i+1} of 5"
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
                return False
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                continue
            cloudevent = parse_cloudevent(msg)
            if cloudevent['type'] == "Microsoft.OpenData.US.NOAA.Humidity":
                return True

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = MicrosoftOpenDataUSNOAAEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_Humidity.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_microsoft_open_data_us_noaa_humidity(data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received
    for i in range(5):
        assert on_event(), f"Failed to receive message {i+1} of 5"
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
                return False
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                continue
            cloudevent = parse_cloudevent(msg)
            if cloudevent['type'] == "Microsoft.OpenData.US.NOAA.Conductivity":
                return True

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = MicrosoftOpenDataUSNOAAEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_Conductivity.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_microsoft_open_data_us_noaa_conductivity(data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received
    for i in range(5):
        assert on_event(), f"Failed to receive message {i+1} of 5"
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
                return False
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                continue
            cloudevent = parse_cloudevent(msg)
            if cloudevent['type'] == "Microsoft.OpenData.US.NOAA.Salinity":
                return True

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = MicrosoftOpenDataUSNOAAEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_Salinity.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_microsoft_open_data_us_noaa_salinity(data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received
    for i in range(5):
        assert on_event(), f"Failed to receive message {i+1} of 5"
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
                return False
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                continue
            cloudevent = parse_cloudevent(msg)
            if cloudevent['type'] == "Microsoft.OpenData.US.NOAA.Station":
                return True

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = MicrosoftOpenDataUSNOAAEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_Station.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_microsoft_open_data_us_noaa_station(data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received
    for i in range(5):
        assert on_event(), f"Failed to receive message {i+1} of 5"
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
                return False
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                continue
            cloudevent = parse_cloudevent(msg)
            if cloudevent['type'] == "Microsoft.OpenData.US.NOAA.Visibility":
                return True

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = MicrosoftOpenDataUSNOAAEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_Visibility.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_microsoft_open_data_us_noaa_visibility(_datacontenttype = f'test_{i}',_subject = f'test_{i}',_time = datetime.datetime.now().isoformat(),_dataschema = f'test_{i}',data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received
    for i in range(5):
        assert on_event(), f"Failed to receive message {i+1} of 5"
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
                return False
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                continue
            cloudevent = parse_cloudevent(msg)
            if cloudevent['type'] == "Microsoft.OpenData.US.NOAA.Currents":
                return True

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = MicrosoftOpenDataUSNOAAEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_Currents.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_microsoft_open_data_us_noaa_currents(data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received
    for i in range(5):
        assert on_event(), f"Failed to receive message {i+1} of 5"
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
                return False
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                continue
            cloudevent = parse_cloudevent(msg)
            if cloudevent['type'] == "Microsoft.OpenData.US.NOAA.CurrentPredictions":
                return True

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = MicrosoftOpenDataUSNOAAEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_CurrentPredictions.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_microsoft_open_data_us_noaa_current_predictions(data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received
    for i in range(5):
        assert on_event(), f"Failed to receive message {i+1} of 5"
    consumer.close()