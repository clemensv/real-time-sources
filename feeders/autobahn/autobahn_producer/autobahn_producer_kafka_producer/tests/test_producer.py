# pylint: disable=missing-function-docstring, wrong-import-position, import-error, no-name-in-module, import-outside-toplevel, no-member, redefined-outer-name, unused-argument, unused-variable, invalid-name, redefined-outer-name, missing-class-docstring

import asyncio
import logging
import os
import sys
import datetime
from typing import Optional

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../autobahn_producer_data/src')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../autobahn_producer_data/tests')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../autobahn_producer_kafka_producer/src')))

import tempfile
import pytest
from confluent_kafka import Producer, Consumer, KafkaException, Message
from confluent_kafka.admin import AdminClient, NewTopic
from cloudevents.abstract import CloudEvent
from cloudevents.kafka import from_binary, from_structured, KafkaMessage
from testcontainers.kafka import KafkaContainer
from autobahn_producer_kafka_producer.producer import DEAutobahnEventProducer
from autobahn_producer_data import RoadEvent
from test_roadevent import Test_RoadEvent
from autobahn_producer_data import WarningEvent
from test_warningevent import Test_WarningEvent
from autobahn_producer_data import ParkingLorry
from test_parkinglorry import Test_ParkingLorry
from autobahn_producer_data import ChargingStation
from test_chargingstation import Test_ChargingStation
from autobahn_producer_data import Webcam
from test_webcam import Test_Webcam
from autobahn_producer_kafka_producer.producer import DEAutobahnMqttEventProducer
from autobahn_producer_kafka_producer.producer import DEAutobahnAmqpEventProducer

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


def test_de_autobahn_deautobahnroadworkappeared(kafka_emulator):
    """Test the DEAutobahnRoadworkAppeared event from the DE.Autobahn message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_de_autobahn_deautobahnroadworkappeared',  # Unique group per test
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
            if cloudevent['type'] == "DE.Autobahn.RoadworkAppeared":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = DEAutobahnEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_RoadEvent.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_de_autobahn_roadwork_appeared(_identifier = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
        expected_key = "{identifier}".format(identifier=f'test_{i}')
        assert received_key == expected_key, f"Expected Kafka key '{expected_key}' but got '{received_key}'"
    consumer.close()


def test_de_autobahn_deautobahnroadworkupdated(kafka_emulator):
    """Test the DEAutobahnRoadworkUpdated event from the DE.Autobahn message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_de_autobahn_deautobahnroadworkupdated',  # Unique group per test
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
            if cloudevent['type'] == "DE.Autobahn.RoadworkUpdated":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = DEAutobahnEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_RoadEvent.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_de_autobahn_roadwork_updated(_identifier = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
        expected_key = "{identifier}".format(identifier=f'test_{i}')
        assert received_key == expected_key, f"Expected Kafka key '{expected_key}' but got '{received_key}'"
    consumer.close()


def test_de_autobahn_deautobahnroadworkresolved(kafka_emulator):
    """Test the DEAutobahnRoadworkResolved event from the DE.Autobahn message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_de_autobahn_deautobahnroadworkresolved',  # Unique group per test
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
            if cloudevent['type'] == "DE.Autobahn.RoadworkResolved":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = DEAutobahnEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_RoadEvent.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_de_autobahn_roadwork_resolved(_identifier = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
        expected_key = "{identifier}".format(identifier=f'test_{i}')
        assert received_key == expected_key, f"Expected Kafka key '{expected_key}' but got '{received_key}'"
    consumer.close()


def test_de_autobahn_deautobahnshorttermroadworkappeared(kafka_emulator):
    """Test the DEAutobahnShortTermRoadworkAppeared event from the DE.Autobahn message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_de_autobahn_deautobahnshorttermroadworkappeared',  # Unique group per test
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
            if cloudevent['type'] == "DE.Autobahn.ShortTermRoadworkAppeared":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = DEAutobahnEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_RoadEvent.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_de_autobahn_short_term_roadwork_appeared(_identifier = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
        expected_key = "{identifier}".format(identifier=f'test_{i}')
        assert received_key == expected_key, f"Expected Kafka key '{expected_key}' but got '{received_key}'"
    consumer.close()


def test_de_autobahn_deautobahnshorttermroadworkupdated(kafka_emulator):
    """Test the DEAutobahnShortTermRoadworkUpdated event from the DE.Autobahn message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_de_autobahn_deautobahnshorttermroadworkupdated',  # Unique group per test
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
            if cloudevent['type'] == "DE.Autobahn.ShortTermRoadworkUpdated":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = DEAutobahnEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_RoadEvent.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_de_autobahn_short_term_roadwork_updated(_identifier = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
        expected_key = "{identifier}".format(identifier=f'test_{i}')
        assert received_key == expected_key, f"Expected Kafka key '{expected_key}' but got '{received_key}'"
    consumer.close()


def test_de_autobahn_deautobahnshorttermroadworkresolved(kafka_emulator):
    """Test the DEAutobahnShortTermRoadworkResolved event from the DE.Autobahn message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_de_autobahn_deautobahnshorttermroadworkresolved',  # Unique group per test
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
            if cloudevent['type'] == "DE.Autobahn.ShortTermRoadworkResolved":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = DEAutobahnEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_RoadEvent.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_de_autobahn_short_term_roadwork_resolved(_identifier = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
        expected_key = "{identifier}".format(identifier=f'test_{i}')
        assert received_key == expected_key, f"Expected Kafka key '{expected_key}' but got '{received_key}'"
    consumer.close()


def test_de_autobahn_deautobahnwarningappeared(kafka_emulator):
    """Test the DEAutobahnWarningAppeared event from the DE.Autobahn message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_de_autobahn_deautobahnwarningappeared',  # Unique group per test
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
            if cloudevent['type'] == "DE.Autobahn.WarningAppeared":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = DEAutobahnEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_WarningEvent.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_de_autobahn_warning_appeared(_identifier = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
        expected_key = "{identifier}".format(identifier=f'test_{i}')
        assert received_key == expected_key, f"Expected Kafka key '{expected_key}' but got '{received_key}'"
    consumer.close()


def test_de_autobahn_deautobahnwarningupdated(kafka_emulator):
    """Test the DEAutobahnWarningUpdated event from the DE.Autobahn message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_de_autobahn_deautobahnwarningupdated',  # Unique group per test
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
            if cloudevent['type'] == "DE.Autobahn.WarningUpdated":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = DEAutobahnEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_WarningEvent.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_de_autobahn_warning_updated(_identifier = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
        expected_key = "{identifier}".format(identifier=f'test_{i}')
        assert received_key == expected_key, f"Expected Kafka key '{expected_key}' but got '{received_key}'"
    consumer.close()


def test_de_autobahn_deautobahnwarningresolved(kafka_emulator):
    """Test the DEAutobahnWarningResolved event from the DE.Autobahn message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_de_autobahn_deautobahnwarningresolved',  # Unique group per test
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
            if cloudevent['type'] == "DE.Autobahn.WarningResolved":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = DEAutobahnEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_WarningEvent.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_de_autobahn_warning_resolved(_identifier = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
        expected_key = "{identifier}".format(identifier=f'test_{i}')
        assert received_key == expected_key, f"Expected Kafka key '{expected_key}' but got '{received_key}'"
    consumer.close()


def test_de_autobahn_deautobahnclosureappeared(kafka_emulator):
    """Test the DEAutobahnClosureAppeared event from the DE.Autobahn message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_de_autobahn_deautobahnclosureappeared',  # Unique group per test
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
            if cloudevent['type'] == "DE.Autobahn.ClosureAppeared":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = DEAutobahnEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_RoadEvent.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_de_autobahn_closure_appeared(_identifier = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
        expected_key = "{identifier}".format(identifier=f'test_{i}')
        assert received_key == expected_key, f"Expected Kafka key '{expected_key}' but got '{received_key}'"
    consumer.close()


def test_de_autobahn_deautobahnclosureupdated(kafka_emulator):
    """Test the DEAutobahnClosureUpdated event from the DE.Autobahn message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_de_autobahn_deautobahnclosureupdated',  # Unique group per test
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
            if cloudevent['type'] == "DE.Autobahn.ClosureUpdated":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = DEAutobahnEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_RoadEvent.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_de_autobahn_closure_updated(_identifier = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
        expected_key = "{identifier}".format(identifier=f'test_{i}')
        assert received_key == expected_key, f"Expected Kafka key '{expected_key}' but got '{received_key}'"
    consumer.close()


def test_de_autobahn_deautobahnclosureresolved(kafka_emulator):
    """Test the DEAutobahnClosureResolved event from the DE.Autobahn message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_de_autobahn_deautobahnclosureresolved',  # Unique group per test
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
            if cloudevent['type'] == "DE.Autobahn.ClosureResolved":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = DEAutobahnEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_RoadEvent.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_de_autobahn_closure_resolved(_identifier = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
        expected_key = "{identifier}".format(identifier=f'test_{i}')
        assert received_key == expected_key, f"Expected Kafka key '{expected_key}' but got '{received_key}'"
    consumer.close()


def test_de_autobahn_deautobahnentryexitclosureappeared(kafka_emulator):
    """Test the DEAutobahnEntryExitClosureAppeared event from the DE.Autobahn message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_de_autobahn_deautobahnentryexitclosureappeared',  # Unique group per test
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
            if cloudevent['type'] == "DE.Autobahn.EntryExitClosureAppeared":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = DEAutobahnEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_RoadEvent.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_de_autobahn_entry_exit_closure_appeared(_identifier = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
        expected_key = "{identifier}".format(identifier=f'test_{i}')
        assert received_key == expected_key, f"Expected Kafka key '{expected_key}' but got '{received_key}'"
    consumer.close()


def test_de_autobahn_deautobahnentryexitclosureupdated(kafka_emulator):
    """Test the DEAutobahnEntryExitClosureUpdated event from the DE.Autobahn message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_de_autobahn_deautobahnentryexitclosureupdated',  # Unique group per test
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
            if cloudevent['type'] == "DE.Autobahn.EntryExitClosureUpdated":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = DEAutobahnEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_RoadEvent.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_de_autobahn_entry_exit_closure_updated(_identifier = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
        expected_key = "{identifier}".format(identifier=f'test_{i}')
        assert received_key == expected_key, f"Expected Kafka key '{expected_key}' but got '{received_key}'"
    consumer.close()


def test_de_autobahn_deautobahnentryexitclosureresolved(kafka_emulator):
    """Test the DEAutobahnEntryExitClosureResolved event from the DE.Autobahn message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_de_autobahn_deautobahnentryexitclosureresolved',  # Unique group per test
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
            if cloudevent['type'] == "DE.Autobahn.EntryExitClosureResolved":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = DEAutobahnEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_RoadEvent.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_de_autobahn_entry_exit_closure_resolved(_identifier = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
        expected_key = "{identifier}".format(identifier=f'test_{i}')
        assert received_key == expected_key, f"Expected Kafka key '{expected_key}' but got '{received_key}'"
    consumer.close()


def test_de_autobahn_deautobahnweightlimit35restrictionappeared(kafka_emulator):
    """Test the DEAutobahnWeightLimit35RestrictionAppeared event from the DE.Autobahn message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_de_autobahn_deautobahnweightlimit35restrictionappeared',  # Unique group per test
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
            if cloudevent['type'] == "DE.Autobahn.WeightLimit35RestrictionAppeared":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = DEAutobahnEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_RoadEvent.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_de_autobahn_weight_limit35_restriction_appeared(_identifier = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
        expected_key = "{identifier}".format(identifier=f'test_{i}')
        assert received_key == expected_key, f"Expected Kafka key '{expected_key}' but got '{received_key}'"
    consumer.close()


def test_de_autobahn_deautobahnweightlimit35restrictionupdated(kafka_emulator):
    """Test the DEAutobahnWeightLimit35RestrictionUpdated event from the DE.Autobahn message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_de_autobahn_deautobahnweightlimit35restrictionupdated',  # Unique group per test
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
            if cloudevent['type'] == "DE.Autobahn.WeightLimit35RestrictionUpdated":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = DEAutobahnEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_RoadEvent.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_de_autobahn_weight_limit35_restriction_updated(_identifier = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
        expected_key = "{identifier}".format(identifier=f'test_{i}')
        assert received_key == expected_key, f"Expected Kafka key '{expected_key}' but got '{received_key}'"
    consumer.close()


def test_de_autobahn_deautobahnweightlimit35restrictionresolved(kafka_emulator):
    """Test the DEAutobahnWeightLimit35RestrictionResolved event from the DE.Autobahn message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_de_autobahn_deautobahnweightlimit35restrictionresolved',  # Unique group per test
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
            if cloudevent['type'] == "DE.Autobahn.WeightLimit35RestrictionResolved":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = DEAutobahnEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_RoadEvent.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_de_autobahn_weight_limit35_restriction_resolved(_identifier = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
        expected_key = "{identifier}".format(identifier=f'test_{i}')
        assert received_key == expected_key, f"Expected Kafka key '{expected_key}' but got '{received_key}'"
    consumer.close()


def test_de_autobahn_deautobahnparkinglorryappeared(kafka_emulator):
    """Test the DEAutobahnParkingLorryAppeared event from the DE.Autobahn message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_de_autobahn_deautobahnparkinglorryappeared',  # Unique group per test
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
            if cloudevent['type'] == "DE.Autobahn.ParkingLorryAppeared":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = DEAutobahnEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_ParkingLorry.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_de_autobahn_parking_lorry_appeared(_identifier = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
        expected_key = "{identifier}".format(identifier=f'test_{i}')
        assert received_key == expected_key, f"Expected Kafka key '{expected_key}' but got '{received_key}'"
    consumer.close()


def test_de_autobahn_deautobahnparkinglorryupdated(kafka_emulator):
    """Test the DEAutobahnParkingLorryUpdated event from the DE.Autobahn message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_de_autobahn_deautobahnparkinglorryupdated',  # Unique group per test
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
            if cloudevent['type'] == "DE.Autobahn.ParkingLorryUpdated":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = DEAutobahnEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_ParkingLorry.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_de_autobahn_parking_lorry_updated(_identifier = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
        expected_key = "{identifier}".format(identifier=f'test_{i}')
        assert received_key == expected_key, f"Expected Kafka key '{expected_key}' but got '{received_key}'"
    consumer.close()


def test_de_autobahn_deautobahnparkinglorryresolved(kafka_emulator):
    """Test the DEAutobahnParkingLorryResolved event from the DE.Autobahn message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_de_autobahn_deautobahnparkinglorryresolved',  # Unique group per test
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
            if cloudevent['type'] == "DE.Autobahn.ParkingLorryResolved":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = DEAutobahnEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_ParkingLorry.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_de_autobahn_parking_lorry_resolved(_identifier = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
        expected_key = "{identifier}".format(identifier=f'test_{i}')
        assert received_key == expected_key, f"Expected Kafka key '{expected_key}' but got '{received_key}'"
    consumer.close()


def test_de_autobahn_deautobahnelectricchargingstationappeared(kafka_emulator):
    """Test the DEAutobahnElectricChargingStationAppeared event from the DE.Autobahn message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_de_autobahn_deautobahnelectricchargingstationappeared',  # Unique group per test
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
            if cloudevent['type'] == "DE.Autobahn.ElectricChargingStationAppeared":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = DEAutobahnEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_ChargingStation.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_de_autobahn_electric_charging_station_appeared(_identifier = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
        expected_key = "{identifier}".format(identifier=f'test_{i}')
        assert received_key == expected_key, f"Expected Kafka key '{expected_key}' but got '{received_key}'"
    consumer.close()


def test_de_autobahn_deautobahnelectricchargingstationupdated(kafka_emulator):
    """Test the DEAutobahnElectricChargingStationUpdated event from the DE.Autobahn message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_de_autobahn_deautobahnelectricchargingstationupdated',  # Unique group per test
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
            if cloudevent['type'] == "DE.Autobahn.ElectricChargingStationUpdated":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = DEAutobahnEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_ChargingStation.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_de_autobahn_electric_charging_station_updated(_identifier = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
        expected_key = "{identifier}".format(identifier=f'test_{i}')
        assert received_key == expected_key, f"Expected Kafka key '{expected_key}' but got '{received_key}'"
    consumer.close()


def test_de_autobahn_deautobahnelectricchargingstationresolved(kafka_emulator):
    """Test the DEAutobahnElectricChargingStationResolved event from the DE.Autobahn message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_de_autobahn_deautobahnelectricchargingstationresolved',  # Unique group per test
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
            if cloudevent['type'] == "DE.Autobahn.ElectricChargingStationResolved":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = DEAutobahnEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_ChargingStation.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_de_autobahn_electric_charging_station_resolved(_identifier = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
        expected_key = "{identifier}".format(identifier=f'test_{i}')
        assert received_key == expected_key, f"Expected Kafka key '{expected_key}' but got '{received_key}'"
    consumer.close()


def test_de_autobahn_deautobahnstrongelectricchargingstationappeared(kafka_emulator):
    """Test the DEAutobahnStrongElectricChargingStationAppeared event from the DE.Autobahn message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_de_autobahn_deautobahnstrongelectricchargingstationappeared',  # Unique group per test
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
            if cloudevent['type'] == "DE.Autobahn.StrongElectricChargingStationAppeared":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = DEAutobahnEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_ChargingStation.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_de_autobahn_strong_electric_charging_station_appeared(_identifier = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
        expected_key = "{identifier}".format(identifier=f'test_{i}')
        assert received_key == expected_key, f"Expected Kafka key '{expected_key}' but got '{received_key}'"
    consumer.close()


def test_de_autobahn_deautobahnstrongelectricchargingstationupdated(kafka_emulator):
    """Test the DEAutobahnStrongElectricChargingStationUpdated event from the DE.Autobahn message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_de_autobahn_deautobahnstrongelectricchargingstationupdated',  # Unique group per test
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
            if cloudevent['type'] == "DE.Autobahn.StrongElectricChargingStationUpdated":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = DEAutobahnEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_ChargingStation.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_de_autobahn_strong_electric_charging_station_updated(_identifier = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
        expected_key = "{identifier}".format(identifier=f'test_{i}')
        assert received_key == expected_key, f"Expected Kafka key '{expected_key}' but got '{received_key}'"
    consumer.close()


def test_de_autobahn_deautobahnstrongelectricchargingstationresolved(kafka_emulator):
    """Test the DEAutobahnStrongElectricChargingStationResolved event from the DE.Autobahn message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_de_autobahn_deautobahnstrongelectricchargingstationresolved',  # Unique group per test
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
            if cloudevent['type'] == "DE.Autobahn.StrongElectricChargingStationResolved":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = DEAutobahnEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_ChargingStation.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_de_autobahn_strong_electric_charging_station_resolved(_identifier = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
        expected_key = "{identifier}".format(identifier=f'test_{i}')
        assert received_key == expected_key, f"Expected Kafka key '{expected_key}' but got '{received_key}'"
    consumer.close()


def test_de_autobahn_deautobahnwebcamappeared(kafka_emulator):
    """Test the DEAutobahnWebcamAppeared event from the DE.Autobahn message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_de_autobahn_deautobahnwebcamappeared',  # Unique group per test
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
            if cloudevent['type'] == "DE.Autobahn.WebcamAppeared":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = DEAutobahnEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_Webcam.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_de_autobahn_webcam_appeared(_identifier = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
        expected_key = "{identifier}".format(identifier=f'test_{i}')
        assert received_key == expected_key, f"Expected Kafka key '{expected_key}' but got '{received_key}'"
    consumer.close()


def test_de_autobahn_deautobahnwebcamupdated(kafka_emulator):
    """Test the DEAutobahnWebcamUpdated event from the DE.Autobahn message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_de_autobahn_deautobahnwebcamupdated',  # Unique group per test
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
            if cloudevent['type'] == "DE.Autobahn.WebcamUpdated":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = DEAutobahnEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_Webcam.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_de_autobahn_webcam_updated(_identifier = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
        expected_key = "{identifier}".format(identifier=f'test_{i}')
        assert received_key == expected_key, f"Expected Kafka key '{expected_key}' but got '{received_key}'"
    consumer.close()


def test_de_autobahn_deautobahnwebcamresolved(kafka_emulator):
    """Test the DEAutobahnWebcamResolved event from the DE.Autobahn message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_de_autobahn_deautobahnwebcamresolved',  # Unique group per test
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
            if cloudevent['type'] == "DE.Autobahn.WebcamResolved":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = DEAutobahnEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_Webcam.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_de_autobahn_webcam_resolved(_identifier = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
        expected_key = "{identifier}".format(identifier=f'test_{i}')
        assert received_key == expected_key, f"Expected Kafka key '{expected_key}' but got '{received_key}'"
    consumer.close()


def test_de_autobahn_mqtt_deautobahnroadworkappearedmqtt(kafka_emulator):
    """Test the DEAutobahnRoadworkAppearedMqtt event from the DE.Autobahn.Mqtt message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_de_autobahn_mqtt_deautobahnroadworkappearedmqtt',  # Unique group per test
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
            if cloudevent['type'] == "DE.Autobahn.RoadworkAppeared":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = DEAutobahnMqttEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_RoadEvent.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_de_autobahn_roadwork_appeared_mqtt(_identifier = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
    consumer.close()


def test_de_autobahn_mqtt_deautobahnroadworkupdatedmqtt(kafka_emulator):
    """Test the DEAutobahnRoadworkUpdatedMqtt event from the DE.Autobahn.Mqtt message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_de_autobahn_mqtt_deautobahnroadworkupdatedmqtt',  # Unique group per test
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
            if cloudevent['type'] == "DE.Autobahn.RoadworkUpdated":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = DEAutobahnMqttEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_RoadEvent.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_de_autobahn_roadwork_updated_mqtt(_identifier = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
    consumer.close()


def test_de_autobahn_mqtt_deautobahnroadworkresolvedmqtt(kafka_emulator):
    """Test the DEAutobahnRoadworkResolvedMqtt event from the DE.Autobahn.Mqtt message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_de_autobahn_mqtt_deautobahnroadworkresolvedmqtt',  # Unique group per test
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
            if cloudevent['type'] == "DE.Autobahn.RoadworkResolved":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = DEAutobahnMqttEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_RoadEvent.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_de_autobahn_roadwork_resolved_mqtt(_identifier = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
    consumer.close()


def test_de_autobahn_mqtt_deautobahnshorttermroadworkappearedmqtt(kafka_emulator):
    """Test the DEAutobahnShortTermRoadworkAppearedMqtt event from the DE.Autobahn.Mqtt message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_de_autobahn_mqtt_deautobahnshorttermroadworkappearedmqtt',  # Unique group per test
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
            if cloudevent['type'] == "DE.Autobahn.ShortTermRoadworkAppeared":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = DEAutobahnMqttEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_RoadEvent.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_de_autobahn_short_term_roadwork_appeared_mqtt(_identifier = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
    consumer.close()


def test_de_autobahn_mqtt_deautobahnshorttermroadworkupdatedmqtt(kafka_emulator):
    """Test the DEAutobahnShortTermRoadworkUpdatedMqtt event from the DE.Autobahn.Mqtt message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_de_autobahn_mqtt_deautobahnshorttermroadworkupdatedmqtt',  # Unique group per test
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
            if cloudevent['type'] == "DE.Autobahn.ShortTermRoadworkUpdated":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = DEAutobahnMqttEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_RoadEvent.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_de_autobahn_short_term_roadwork_updated_mqtt(_identifier = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
    consumer.close()


def test_de_autobahn_mqtt_deautobahnshorttermroadworkresolvedmqtt(kafka_emulator):
    """Test the DEAutobahnShortTermRoadworkResolvedMqtt event from the DE.Autobahn.Mqtt message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_de_autobahn_mqtt_deautobahnshorttermroadworkresolvedmqtt',  # Unique group per test
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
            if cloudevent['type'] == "DE.Autobahn.ShortTermRoadworkResolved":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = DEAutobahnMqttEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_RoadEvent.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_de_autobahn_short_term_roadwork_resolved_mqtt(_identifier = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
    consumer.close()


def test_de_autobahn_mqtt_deautobahnclosureappearedmqtt(kafka_emulator):
    """Test the DEAutobahnClosureAppearedMqtt event from the DE.Autobahn.Mqtt message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_de_autobahn_mqtt_deautobahnclosureappearedmqtt',  # Unique group per test
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
            if cloudevent['type'] == "DE.Autobahn.ClosureAppeared":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = DEAutobahnMqttEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_RoadEvent.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_de_autobahn_closure_appeared_mqtt(_identifier = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
    consumer.close()


def test_de_autobahn_mqtt_deautobahnclosureupdatedmqtt(kafka_emulator):
    """Test the DEAutobahnClosureUpdatedMqtt event from the DE.Autobahn.Mqtt message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_de_autobahn_mqtt_deautobahnclosureupdatedmqtt',  # Unique group per test
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
            if cloudevent['type'] == "DE.Autobahn.ClosureUpdated":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = DEAutobahnMqttEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_RoadEvent.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_de_autobahn_closure_updated_mqtt(_identifier = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
    consumer.close()


def test_de_autobahn_mqtt_deautobahnclosureresolvedmqtt(kafka_emulator):
    """Test the DEAutobahnClosureResolvedMqtt event from the DE.Autobahn.Mqtt message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_de_autobahn_mqtt_deautobahnclosureresolvedmqtt',  # Unique group per test
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
            if cloudevent['type'] == "DE.Autobahn.ClosureResolved":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = DEAutobahnMqttEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_RoadEvent.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_de_autobahn_closure_resolved_mqtt(_identifier = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
    consumer.close()


def test_de_autobahn_mqtt_deautobahnentryexitclosureappearedmqtt(kafka_emulator):
    """Test the DEAutobahnEntryExitClosureAppearedMqtt event from the DE.Autobahn.Mqtt message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_de_autobahn_mqtt_deautobahnentryexitclosureappearedmqtt',  # Unique group per test
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
            if cloudevent['type'] == "DE.Autobahn.EntryExitClosureAppeared":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = DEAutobahnMqttEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_RoadEvent.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_de_autobahn_entry_exit_closure_appeared_mqtt(_identifier = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
    consumer.close()


def test_de_autobahn_mqtt_deautobahnentryexitclosureupdatedmqtt(kafka_emulator):
    """Test the DEAutobahnEntryExitClosureUpdatedMqtt event from the DE.Autobahn.Mqtt message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_de_autobahn_mqtt_deautobahnentryexitclosureupdatedmqtt',  # Unique group per test
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
            if cloudevent['type'] == "DE.Autobahn.EntryExitClosureUpdated":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = DEAutobahnMqttEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_RoadEvent.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_de_autobahn_entry_exit_closure_updated_mqtt(_identifier = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
    consumer.close()


def test_de_autobahn_mqtt_deautobahnentryexitclosureresolvedmqtt(kafka_emulator):
    """Test the DEAutobahnEntryExitClosureResolvedMqtt event from the DE.Autobahn.Mqtt message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_de_autobahn_mqtt_deautobahnentryexitclosureresolvedmqtt',  # Unique group per test
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
            if cloudevent['type'] == "DE.Autobahn.EntryExitClosureResolved":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = DEAutobahnMqttEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_RoadEvent.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_de_autobahn_entry_exit_closure_resolved_mqtt(_identifier = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
    consumer.close()


def test_de_autobahn_mqtt_deautobahnwarningappearedmqtt(kafka_emulator):
    """Test the DEAutobahnWarningAppearedMqtt event from the DE.Autobahn.Mqtt message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_de_autobahn_mqtt_deautobahnwarningappearedmqtt',  # Unique group per test
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
            if cloudevent['type'] == "DE.Autobahn.WarningAppeared":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = DEAutobahnMqttEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_WarningEvent.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_de_autobahn_warning_appeared_mqtt(_identifier = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
    consumer.close()


def test_de_autobahn_mqtt_deautobahnwarningupdatedmqtt(kafka_emulator):
    """Test the DEAutobahnWarningUpdatedMqtt event from the DE.Autobahn.Mqtt message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_de_autobahn_mqtt_deautobahnwarningupdatedmqtt',  # Unique group per test
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
            if cloudevent['type'] == "DE.Autobahn.WarningUpdated":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = DEAutobahnMqttEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_WarningEvent.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_de_autobahn_warning_updated_mqtt(_identifier = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
    consumer.close()


def test_de_autobahn_mqtt_deautobahnwarningresolvedmqtt(kafka_emulator):
    """Test the DEAutobahnWarningResolvedMqtt event from the DE.Autobahn.Mqtt message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_de_autobahn_mqtt_deautobahnwarningresolvedmqtt',  # Unique group per test
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
            if cloudevent['type'] == "DE.Autobahn.WarningResolved":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = DEAutobahnMqttEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_WarningEvent.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_de_autobahn_warning_resolved_mqtt(_identifier = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
    consumer.close()


def test_de_autobahn_mqtt_deautobahnweightlimit35restrictionappearedmqtt(kafka_emulator):
    """Test the DEAutobahnWeightLimit35RestrictionAppearedMqtt event from the DE.Autobahn.Mqtt message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_de_autobahn_mqtt_deautobahnweightlimit35restrictionappearedmqtt',  # Unique group per test
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
            if cloudevent['type'] == "DE.Autobahn.WeightLimit35RestrictionAppeared":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = DEAutobahnMqttEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_RoadEvent.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_de_autobahn_weight_limit35_restriction_appeared_mqtt(_identifier = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
    consumer.close()


def test_de_autobahn_mqtt_deautobahnweightlimit35restrictionupdatedmqtt(kafka_emulator):
    """Test the DEAutobahnWeightLimit35RestrictionUpdatedMqtt event from the DE.Autobahn.Mqtt message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_de_autobahn_mqtt_deautobahnweightlimit35restrictionupdatedmqtt',  # Unique group per test
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
            if cloudevent['type'] == "DE.Autobahn.WeightLimit35RestrictionUpdated":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = DEAutobahnMqttEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_RoadEvent.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_de_autobahn_weight_limit35_restriction_updated_mqtt(_identifier = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
    consumer.close()


def test_de_autobahn_mqtt_deautobahnweightlimit35restrictionresolvedmqtt(kafka_emulator):
    """Test the DEAutobahnWeightLimit35RestrictionResolvedMqtt event from the DE.Autobahn.Mqtt message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_de_autobahn_mqtt_deautobahnweightlimit35restrictionresolvedmqtt',  # Unique group per test
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
            if cloudevent['type'] == "DE.Autobahn.WeightLimit35RestrictionResolved":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = DEAutobahnMqttEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_RoadEvent.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_de_autobahn_weight_limit35_restriction_resolved_mqtt(_identifier = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
    consumer.close()


def test_de_autobahn_mqtt_deautobahnwebcamappearedmqtt(kafka_emulator):
    """Test the DEAutobahnWebcamAppearedMqtt event from the DE.Autobahn.Mqtt message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_de_autobahn_mqtt_deautobahnwebcamappearedmqtt',  # Unique group per test
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
            if cloudevent['type'] == "DE.Autobahn.WebcamAppeared":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = DEAutobahnMqttEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_Webcam.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_de_autobahn_webcam_appeared_mqtt(_identifier = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
    consumer.close()


def test_de_autobahn_mqtt_deautobahnwebcamupdatedmqtt(kafka_emulator):
    """Test the DEAutobahnWebcamUpdatedMqtt event from the DE.Autobahn.Mqtt message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_de_autobahn_mqtt_deautobahnwebcamupdatedmqtt',  # Unique group per test
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
            if cloudevent['type'] == "DE.Autobahn.WebcamUpdated":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = DEAutobahnMqttEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_Webcam.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_de_autobahn_webcam_updated_mqtt(_identifier = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
    consumer.close()


def test_de_autobahn_mqtt_deautobahnwebcamresolvedmqtt(kafka_emulator):
    """Test the DEAutobahnWebcamResolvedMqtt event from the DE.Autobahn.Mqtt message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_de_autobahn_mqtt_deautobahnwebcamresolvedmqtt',  # Unique group per test
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
            if cloudevent['type'] == "DE.Autobahn.WebcamResolved":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = DEAutobahnMqttEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_Webcam.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_de_autobahn_webcam_resolved_mqtt(_identifier = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
    consumer.close()


def test_de_autobahn_mqtt_deautobahnparkinglorryappearedmqtt(kafka_emulator):
    """Test the DEAutobahnParkingLorryAppearedMqtt event from the DE.Autobahn.Mqtt message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_de_autobahn_mqtt_deautobahnparkinglorryappearedmqtt',  # Unique group per test
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
            if cloudevent['type'] == "DE.Autobahn.ParkingLorryAppeared":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = DEAutobahnMqttEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_ParkingLorry.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_de_autobahn_parking_lorry_appeared_mqtt(_identifier = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
    consumer.close()


def test_de_autobahn_mqtt_deautobahnparkinglorryupdatedmqtt(kafka_emulator):
    """Test the DEAutobahnParkingLorryUpdatedMqtt event from the DE.Autobahn.Mqtt message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_de_autobahn_mqtt_deautobahnparkinglorryupdatedmqtt',  # Unique group per test
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
            if cloudevent['type'] == "DE.Autobahn.ParkingLorryUpdated":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = DEAutobahnMqttEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_ParkingLorry.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_de_autobahn_parking_lorry_updated_mqtt(_identifier = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
    consumer.close()


def test_de_autobahn_mqtt_deautobahnparkinglorryresolvedmqtt(kafka_emulator):
    """Test the DEAutobahnParkingLorryResolvedMqtt event from the DE.Autobahn.Mqtt message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_de_autobahn_mqtt_deautobahnparkinglorryresolvedmqtt',  # Unique group per test
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
            if cloudevent['type'] == "DE.Autobahn.ParkingLorryResolved":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = DEAutobahnMqttEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_ParkingLorry.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_de_autobahn_parking_lorry_resolved_mqtt(_identifier = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
    consumer.close()


def test_de_autobahn_mqtt_deautobahnelectricchargingstationappearedmqtt(kafka_emulator):
    """Test the DEAutobahnElectricChargingStationAppearedMqtt event from the DE.Autobahn.Mqtt message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_de_autobahn_mqtt_deautobahnelectricchargingstationappearedmqtt',  # Unique group per test
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
            if cloudevent['type'] == "DE.Autobahn.ElectricChargingStationAppeared":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = DEAutobahnMqttEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_ChargingStation.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_de_autobahn_electric_charging_station_appeared_mqtt(_identifier = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
    consumer.close()


def test_de_autobahn_mqtt_deautobahnelectricchargingstationupdatedmqtt(kafka_emulator):
    """Test the DEAutobahnElectricChargingStationUpdatedMqtt event from the DE.Autobahn.Mqtt message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_de_autobahn_mqtt_deautobahnelectricchargingstationupdatedmqtt',  # Unique group per test
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
            if cloudevent['type'] == "DE.Autobahn.ElectricChargingStationUpdated":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = DEAutobahnMqttEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_ChargingStation.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_de_autobahn_electric_charging_station_updated_mqtt(_identifier = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
    consumer.close()


def test_de_autobahn_mqtt_deautobahnelectricchargingstationresolvedmqtt(kafka_emulator):
    """Test the DEAutobahnElectricChargingStationResolvedMqtt event from the DE.Autobahn.Mqtt message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_de_autobahn_mqtt_deautobahnelectricchargingstationresolvedmqtt',  # Unique group per test
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
            if cloudevent['type'] == "DE.Autobahn.ElectricChargingStationResolved":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = DEAutobahnMqttEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_ChargingStation.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_de_autobahn_electric_charging_station_resolved_mqtt(_identifier = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
    consumer.close()


def test_de_autobahn_mqtt_deautobahnstrongelectricchargingstationappearedmqtt(kafka_emulator):
    """Test the DEAutobahnStrongElectricChargingStationAppearedMqtt event from the DE.Autobahn.Mqtt message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_de_autobahn_mqtt_deautobahnstrongelectricchargingstationappearedmqtt',  # Unique group per test
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
            if cloudevent['type'] == "DE.Autobahn.StrongElectricChargingStationAppeared":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = DEAutobahnMqttEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_ChargingStation.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_de_autobahn_strong_electric_charging_station_appeared_mqtt(_identifier = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
    consumer.close()


def test_de_autobahn_mqtt_deautobahnstrongelectricchargingstationupdatedmqtt(kafka_emulator):
    """Test the DEAutobahnStrongElectricChargingStationUpdatedMqtt event from the DE.Autobahn.Mqtt message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_de_autobahn_mqtt_deautobahnstrongelectricchargingstationupdatedmqtt',  # Unique group per test
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
            if cloudevent['type'] == "DE.Autobahn.StrongElectricChargingStationUpdated":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = DEAutobahnMqttEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_ChargingStation.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_de_autobahn_strong_electric_charging_station_updated_mqtt(_identifier = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
    consumer.close()


def test_de_autobahn_mqtt_deautobahnstrongelectricchargingstationresolvedmqtt(kafka_emulator):
    """Test the DEAutobahnStrongElectricChargingStationResolvedMqtt event from the DE.Autobahn.Mqtt message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_de_autobahn_mqtt_deautobahnstrongelectricchargingstationresolvedmqtt',  # Unique group per test
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
            if cloudevent['type'] == "DE.Autobahn.StrongElectricChargingStationResolved":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = DEAutobahnMqttEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_ChargingStation.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_de_autobahn_strong_electric_charging_station_resolved_mqtt(_identifier = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
    consumer.close()


def test_de_autobahn_amqp_deautobahnamqproadworkappeared(kafka_emulator):
    """Test the DEAutobahnAmqpRoadworkAppeared event from the DE.Autobahn.Amqp message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_de_autobahn_amqp_deautobahnamqproadworkappeared',  # Unique group per test
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
            if cloudevent['type'] == "DE.Autobahn.RoadworkAppeared":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = DEAutobahnAmqpEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_RoadEvent.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_de_autobahn_amqp_roadwork_appeared(_identifier = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
    consumer.close()


def test_de_autobahn_amqp_deautobahnamqproadworkupdated(kafka_emulator):
    """Test the DEAutobahnAmqpRoadworkUpdated event from the DE.Autobahn.Amqp message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_de_autobahn_amqp_deautobahnamqproadworkupdated',  # Unique group per test
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
            if cloudevent['type'] == "DE.Autobahn.RoadworkUpdated":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = DEAutobahnAmqpEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_RoadEvent.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_de_autobahn_amqp_roadwork_updated(_identifier = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
    consumer.close()


def test_de_autobahn_amqp_deautobahnamqproadworkresolved(kafka_emulator):
    """Test the DEAutobahnAmqpRoadworkResolved event from the DE.Autobahn.Amqp message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_de_autobahn_amqp_deautobahnamqproadworkresolved',  # Unique group per test
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
            if cloudevent['type'] == "DE.Autobahn.RoadworkResolved":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = DEAutobahnAmqpEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_RoadEvent.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_de_autobahn_amqp_roadwork_resolved(_identifier = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
    consumer.close()


def test_de_autobahn_amqp_deautobahnamqpshorttermroadworkappeared(kafka_emulator):
    """Test the DEAutobahnAmqpShortTermRoadworkAppeared event from the DE.Autobahn.Amqp message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_de_autobahn_amqp_deautobahnamqpshorttermroadworkappeared',  # Unique group per test
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
            if cloudevent['type'] == "DE.Autobahn.ShortTermRoadworkAppeared":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = DEAutobahnAmqpEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_RoadEvent.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_de_autobahn_amqp_short_term_roadwork_appeared(_identifier = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
    consumer.close()


def test_de_autobahn_amqp_deautobahnamqpshorttermroadworkupdated(kafka_emulator):
    """Test the DEAutobahnAmqpShortTermRoadworkUpdated event from the DE.Autobahn.Amqp message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_de_autobahn_amqp_deautobahnamqpshorttermroadworkupdated',  # Unique group per test
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
            if cloudevent['type'] == "DE.Autobahn.ShortTermRoadworkUpdated":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = DEAutobahnAmqpEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_RoadEvent.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_de_autobahn_amqp_short_term_roadwork_updated(_identifier = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
    consumer.close()


def test_de_autobahn_amqp_deautobahnamqpshorttermroadworkresolved(kafka_emulator):
    """Test the DEAutobahnAmqpShortTermRoadworkResolved event from the DE.Autobahn.Amqp message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_de_autobahn_amqp_deautobahnamqpshorttermroadworkresolved',  # Unique group per test
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
            if cloudevent['type'] == "DE.Autobahn.ShortTermRoadworkResolved":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = DEAutobahnAmqpEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_RoadEvent.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_de_autobahn_amqp_short_term_roadwork_resolved(_identifier = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
    consumer.close()


def test_de_autobahn_amqp_deautobahnamqpclosureappeared(kafka_emulator):
    """Test the DEAutobahnAmqpClosureAppeared event from the DE.Autobahn.Amqp message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_de_autobahn_amqp_deautobahnamqpclosureappeared',  # Unique group per test
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
            if cloudevent['type'] == "DE.Autobahn.ClosureAppeared":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = DEAutobahnAmqpEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_RoadEvent.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_de_autobahn_amqp_closure_appeared(_identifier = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
    consumer.close()


def test_de_autobahn_amqp_deautobahnamqpclosureupdated(kafka_emulator):
    """Test the DEAutobahnAmqpClosureUpdated event from the DE.Autobahn.Amqp message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_de_autobahn_amqp_deautobahnamqpclosureupdated',  # Unique group per test
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
            if cloudevent['type'] == "DE.Autobahn.ClosureUpdated":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = DEAutobahnAmqpEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_RoadEvent.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_de_autobahn_amqp_closure_updated(_identifier = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
    consumer.close()


def test_de_autobahn_amqp_deautobahnamqpclosureresolved(kafka_emulator):
    """Test the DEAutobahnAmqpClosureResolved event from the DE.Autobahn.Amqp message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_de_autobahn_amqp_deautobahnamqpclosureresolved',  # Unique group per test
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
            if cloudevent['type'] == "DE.Autobahn.ClosureResolved":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = DEAutobahnAmqpEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_RoadEvent.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_de_autobahn_amqp_closure_resolved(_identifier = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
    consumer.close()


def test_de_autobahn_amqp_deautobahnamqpentryexitclosureappeared(kafka_emulator):
    """Test the DEAutobahnAmqpEntryExitClosureAppeared event from the DE.Autobahn.Amqp message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_de_autobahn_amqp_deautobahnamqpentryexitclosureappeared',  # Unique group per test
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
            if cloudevent['type'] == "DE.Autobahn.EntryExitClosureAppeared":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = DEAutobahnAmqpEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_RoadEvent.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_de_autobahn_amqp_entry_exit_closure_appeared(_identifier = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
    consumer.close()


def test_de_autobahn_amqp_deautobahnamqpentryexitclosureupdated(kafka_emulator):
    """Test the DEAutobahnAmqpEntryExitClosureUpdated event from the DE.Autobahn.Amqp message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_de_autobahn_amqp_deautobahnamqpentryexitclosureupdated',  # Unique group per test
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
            if cloudevent['type'] == "DE.Autobahn.EntryExitClosureUpdated":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = DEAutobahnAmqpEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_RoadEvent.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_de_autobahn_amqp_entry_exit_closure_updated(_identifier = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
    consumer.close()


def test_de_autobahn_amqp_deautobahnamqpentryexitclosureresolved(kafka_emulator):
    """Test the DEAutobahnAmqpEntryExitClosureResolved event from the DE.Autobahn.Amqp message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_de_autobahn_amqp_deautobahnamqpentryexitclosureresolved',  # Unique group per test
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
            if cloudevent['type'] == "DE.Autobahn.EntryExitClosureResolved":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = DEAutobahnAmqpEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_RoadEvent.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_de_autobahn_amqp_entry_exit_closure_resolved(_identifier = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
    consumer.close()


def test_de_autobahn_amqp_deautobahnamqpwarningappeared(kafka_emulator):
    """Test the DEAutobahnAmqpWarningAppeared event from the DE.Autobahn.Amqp message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_de_autobahn_amqp_deautobahnamqpwarningappeared',  # Unique group per test
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
            if cloudevent['type'] == "DE.Autobahn.WarningAppeared":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = DEAutobahnAmqpEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_WarningEvent.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_de_autobahn_amqp_warning_appeared(_identifier = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
    consumer.close()


def test_de_autobahn_amqp_deautobahnamqpwarningupdated(kafka_emulator):
    """Test the DEAutobahnAmqpWarningUpdated event from the DE.Autobahn.Amqp message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_de_autobahn_amqp_deautobahnamqpwarningupdated',  # Unique group per test
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
            if cloudevent['type'] == "DE.Autobahn.WarningUpdated":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = DEAutobahnAmqpEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_WarningEvent.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_de_autobahn_amqp_warning_updated(_identifier = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
    consumer.close()


def test_de_autobahn_amqp_deautobahnamqpwarningresolved(kafka_emulator):
    """Test the DEAutobahnAmqpWarningResolved event from the DE.Autobahn.Amqp message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_de_autobahn_amqp_deautobahnamqpwarningresolved',  # Unique group per test
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
            if cloudevent['type'] == "DE.Autobahn.WarningResolved":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = DEAutobahnAmqpEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_WarningEvent.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_de_autobahn_amqp_warning_resolved(_identifier = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
    consumer.close()


def test_de_autobahn_amqp_deautobahnamqpweightlimit35restrictionappeared(kafka_emulator):
    """Test the DEAutobahnAmqpWeightLimit35RestrictionAppeared event from the DE.Autobahn.Amqp message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_de_autobahn_amqp_deautobahnamqpweightlimit35restrictionappeared',  # Unique group per test
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
            if cloudevent['type'] == "DE.Autobahn.WeightLimit35RestrictionAppeared":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = DEAutobahnAmqpEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_RoadEvent.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_de_autobahn_amqp_weight_limit35_restriction_appeared(_identifier = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
    consumer.close()


def test_de_autobahn_amqp_deautobahnamqpweightlimit35restrictionupdated(kafka_emulator):
    """Test the DEAutobahnAmqpWeightLimit35RestrictionUpdated event from the DE.Autobahn.Amqp message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_de_autobahn_amqp_deautobahnamqpweightlimit35restrictionupdated',  # Unique group per test
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
            if cloudevent['type'] == "DE.Autobahn.WeightLimit35RestrictionUpdated":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = DEAutobahnAmqpEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_RoadEvent.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_de_autobahn_amqp_weight_limit35_restriction_updated(_identifier = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
    consumer.close()


def test_de_autobahn_amqp_deautobahnamqpweightlimit35restrictionresolved(kafka_emulator):
    """Test the DEAutobahnAmqpWeightLimit35RestrictionResolved event from the DE.Autobahn.Amqp message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_de_autobahn_amqp_deautobahnamqpweightlimit35restrictionresolved',  # Unique group per test
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
            if cloudevent['type'] == "DE.Autobahn.WeightLimit35RestrictionResolved":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = DEAutobahnAmqpEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_RoadEvent.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_de_autobahn_amqp_weight_limit35_restriction_resolved(_identifier = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
    consumer.close()


def test_de_autobahn_amqp_deautobahnamqpwebcamappeared(kafka_emulator):
    """Test the DEAutobahnAmqpWebcamAppeared event from the DE.Autobahn.Amqp message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_de_autobahn_amqp_deautobahnamqpwebcamappeared',  # Unique group per test
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
            if cloudevent['type'] == "DE.Autobahn.WebcamAppeared":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = DEAutobahnAmqpEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_Webcam.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_de_autobahn_amqp_webcam_appeared(_identifier = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
    consumer.close()


def test_de_autobahn_amqp_deautobahnamqpwebcamupdated(kafka_emulator):
    """Test the DEAutobahnAmqpWebcamUpdated event from the DE.Autobahn.Amqp message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_de_autobahn_amqp_deautobahnamqpwebcamupdated',  # Unique group per test
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
            if cloudevent['type'] == "DE.Autobahn.WebcamUpdated":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = DEAutobahnAmqpEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_Webcam.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_de_autobahn_amqp_webcam_updated(_identifier = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
    consumer.close()


def test_de_autobahn_amqp_deautobahnamqpwebcamresolved(kafka_emulator):
    """Test the DEAutobahnAmqpWebcamResolved event from the DE.Autobahn.Amqp message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_de_autobahn_amqp_deautobahnamqpwebcamresolved',  # Unique group per test
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
            if cloudevent['type'] == "DE.Autobahn.WebcamResolved":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = DEAutobahnAmqpEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_Webcam.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_de_autobahn_amqp_webcam_resolved(_identifier = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
    consumer.close()


def test_de_autobahn_amqp_deautobahnamqpparkinglorryappeared(kafka_emulator):
    """Test the DEAutobahnAmqpParkingLorryAppeared event from the DE.Autobahn.Amqp message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_de_autobahn_amqp_deautobahnamqpparkinglorryappeared',  # Unique group per test
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
            if cloudevent['type'] == "DE.Autobahn.ParkingLorryAppeared":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = DEAutobahnAmqpEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_ParkingLorry.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_de_autobahn_amqp_parking_lorry_appeared(_identifier = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
    consumer.close()


def test_de_autobahn_amqp_deautobahnamqpparkinglorryupdated(kafka_emulator):
    """Test the DEAutobahnAmqpParkingLorryUpdated event from the DE.Autobahn.Amqp message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_de_autobahn_amqp_deautobahnamqpparkinglorryupdated',  # Unique group per test
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
            if cloudevent['type'] == "DE.Autobahn.ParkingLorryUpdated":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = DEAutobahnAmqpEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_ParkingLorry.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_de_autobahn_amqp_parking_lorry_updated(_identifier = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
    consumer.close()


def test_de_autobahn_amqp_deautobahnamqpparkinglorryresolved(kafka_emulator):
    """Test the DEAutobahnAmqpParkingLorryResolved event from the DE.Autobahn.Amqp message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_de_autobahn_amqp_deautobahnamqpparkinglorryresolved',  # Unique group per test
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
            if cloudevent['type'] == "DE.Autobahn.ParkingLorryResolved":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = DEAutobahnAmqpEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_ParkingLorry.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_de_autobahn_amqp_parking_lorry_resolved(_identifier = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
    consumer.close()


def test_de_autobahn_amqp_deautobahnamqpelectricchargingstationappeared(kafka_emulator):
    """Test the DEAutobahnAmqpElectricChargingStationAppeared event from the DE.Autobahn.Amqp message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_de_autobahn_amqp_deautobahnamqpelectricchargingstationappeared',  # Unique group per test
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
            if cloudevent['type'] == "DE.Autobahn.ElectricChargingStationAppeared":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = DEAutobahnAmqpEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_ChargingStation.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_de_autobahn_amqp_electric_charging_station_appeared(_identifier = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
    consumer.close()


def test_de_autobahn_amqp_deautobahnamqpelectricchargingstationupdated(kafka_emulator):
    """Test the DEAutobahnAmqpElectricChargingStationUpdated event from the DE.Autobahn.Amqp message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_de_autobahn_amqp_deautobahnamqpelectricchargingstationupdated',  # Unique group per test
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
            if cloudevent['type'] == "DE.Autobahn.ElectricChargingStationUpdated":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = DEAutobahnAmqpEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_ChargingStation.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_de_autobahn_amqp_electric_charging_station_updated(_identifier = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
    consumer.close()


def test_de_autobahn_amqp_deautobahnamqpelectricchargingstationresolved(kafka_emulator):
    """Test the DEAutobahnAmqpElectricChargingStationResolved event from the DE.Autobahn.Amqp message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_de_autobahn_amqp_deautobahnamqpelectricchargingstationresolved',  # Unique group per test
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
            if cloudevent['type'] == "DE.Autobahn.ElectricChargingStationResolved":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = DEAutobahnAmqpEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_ChargingStation.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_de_autobahn_amqp_electric_charging_station_resolved(_identifier = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
    consumer.close()


def test_de_autobahn_amqp_deautobahnamqpstrongelectricchargingstationappeared(kafka_emulator):
    """Test the DEAutobahnAmqpStrongElectricChargingStationAppeared event from the DE.Autobahn.Amqp message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_de_autobahn_amqp_deautobahnamqpstrongelectricchargingstationappeared',  # Unique group per test
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
            if cloudevent['type'] == "DE.Autobahn.StrongElectricChargingStationAppeared":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = DEAutobahnAmqpEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_ChargingStation.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_de_autobahn_amqp_strong_electric_charging_station_appeared(_identifier = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
    consumer.close()


def test_de_autobahn_amqp_deautobahnamqpstrongelectricchargingstationupdated(kafka_emulator):
    """Test the DEAutobahnAmqpStrongElectricChargingStationUpdated event from the DE.Autobahn.Amqp message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_de_autobahn_amqp_deautobahnamqpstrongelectricchargingstationupdated',  # Unique group per test
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
            if cloudevent['type'] == "DE.Autobahn.StrongElectricChargingStationUpdated":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = DEAutobahnAmqpEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_ChargingStation.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_de_autobahn_amqp_strong_electric_charging_station_updated(_identifier = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
    consumer.close()


def test_de_autobahn_amqp_deautobahnamqpstrongelectricchargingstationresolved(kafka_emulator):
    """Test the DEAutobahnAmqpStrongElectricChargingStationResolved event from the DE.Autobahn.Amqp message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_de_autobahn_amqp_deautobahnamqpstrongelectricchargingstationresolved',  # Unique group per test
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
            if cloudevent['type'] == "DE.Autobahn.StrongElectricChargingStationResolved":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = DEAutobahnAmqpEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_ChargingStation.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_de_autobahn_amqp_strong_electric_charging_station_resolved(_identifier = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
    consumer.close()


def test_de_autobahn_cross_event_type_kafka_key(kafka_emulator):
    """Test that different event types in DE.Autobahn produce the same Kafka key for the same placeholder values"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_de_autobahn_cross_key',
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
    producer_instance = DEAutobahnEventProducer(kafka_producer, topic, 'binary')

    shared_key_value = "shared_entity_42"
    data1 = Test_RoadEvent.create_instance()
    data2 = Test_RoadEvent.create_instance()

    producer_instance.send_de_autobahn_roadwork_appeared(_identifier = shared_key_value, data = data1)
    producer_instance.send_de_autobahn_roadwork_updated(_identifier = shared_key_value, data = data2)
    kafka_producer.flush(timeout=5.0)

    # Collect keys from both messages
    collected_keys = []
    timeout = time.time() + 20
    while len(collected_keys) < 2 and time.time() < timeout:
        msg = consumer.poll(1.0)
        if msg is None or msg.error():
            continue
        cloudevent = parse_cloudevent(msg)
        if cloudevent['type'] in ["DE.Autobahn.RoadworkAppeared", "DE.Autobahn.RoadworkUpdated"]:
            key = msg.key().decode('utf-8') if msg.key() else None
            collected_keys.append(key)

    assert len(collected_keys) == 2, f"Expected 2 messages but received {len(collected_keys)}"
    assert collected_keys[0] == collected_keys[1], \
        f"Expected same Kafka key for different event types but got '{collected_keys[0]}' and '{collected_keys[1]}'"
    expected_key = "{identifier}".format(identifier=shared_key_value)
    assert collected_keys[0] == expected_key, \
        f"Expected Kafka key '{expected_key}' but got '{collected_keys[0]}'"
    consumer.close()