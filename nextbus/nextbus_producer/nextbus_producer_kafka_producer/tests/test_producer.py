# pylint: disable=missing-function-docstring, wrong-import-position, import-error, no-name-in-module, import-outside-toplevel, no-member, redefined-outer-name, unused-argument, unused-variable, invalid-name, redefined-outer-name, missing-class-docstring

import asyncio
import logging
import os
import sys
import datetime
from typing import Optional

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../nextbus_producer_data/src')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../nextbus_producer_data/tests')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../nextbus_producer_kafka_producer/src')))

import tempfile
import pytest
from confluent_kafka import Producer, Consumer, KafkaException, Message
from confluent_kafka.admin import AdminClient, NewTopic
from cloudevents.abstract import CloudEvent
from cloudevents.kafka import from_binary, from_structured, KafkaMessage
from testcontainers.kafka import KafkaContainer
from nextbus_producer_kafka_producer.producer import NextbusEventProducer
from nextbus_producer_data import VehiclePosition
from test_nextbus_producer_data_vehicleposition import Test_VehiclePosition
from nextbus_producer_data import RouteConfig
from test_nextbus_producer_data_routeconfig import Test_RouteConfig
from nextbus_producer_data import Schedule
from test_nextbus_producer_data_schedule import Test_Schedule
from nextbus_producer_data import Message
from test_nextbus_producer_data_message import Test_Message

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


def test_nextbus_nextbusvehicleposition(kafka_emulator):
    """Test the NextbusVehiclePosition event from the Nextbus message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_nextbus_nextbusvehicleposition',  # Unique group per test
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
            if cloudevent['type'] == "nextbus.VehiclePosition":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = NextbusEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_VehiclePosition.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_nextbus_vehicle_position(_agency_id = f'test_{i}', _route_tag = f'test_{i}', _vehicle_id = f'test_{i}', _timestamp = f'test_{i}', data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
        expected_key = "{agency_id}/{route_tag}".format(agency_id=f'test_{i}', route_tag=f'test_{i}')
        assert received_key == expected_key, f"Expected Kafka key '{expected_key}' but got '{received_key}'"
    consumer.close()


def test_nextbus_nextbusrouteconfig(kafka_emulator):
    """Test the NextbusRouteConfig event from the Nextbus message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_nextbus_nextbusrouteconfig',  # Unique group per test
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
            if cloudevent['type'] == "nextbus.RouteConfig":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = NextbusEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_RouteConfig.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_nextbus_route_config(_agency_id = f'test_{i}', _route_tag = f'test_{i}', _stop_or_vehicle_id = f'test_{i}', _timestamp = f'test_{i}', data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
        expected_key = "{agency_id}/{route_tag}".format(agency_id=f'test_{i}', route_tag=f'test_{i}')
        assert received_key == expected_key, f"Expected Kafka key '{expected_key}' but got '{received_key}'"
    consumer.close()


def test_nextbus_nextbusschedule(kafka_emulator):
    """Test the NextbusSchedule event from the Nextbus message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_nextbus_nextbusschedule',  # Unique group per test
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
            if cloudevent['type'] == "nextbus.Schedule":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = NextbusEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_Schedule.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_nextbus_schedule(_agency_id = f'test_{i}', _route_tag = f'test_{i}', _stop_or_vehicle_id = f'test_{i}', _timestamp = f'test_{i}', data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
        expected_key = "{agency_id}/{route_tag}".format(agency_id=f'test_{i}', route_tag=f'test_{i}')
        assert received_key == expected_key, f"Expected Kafka key '{expected_key}' but got '{received_key}'"
    consumer.close()


def test_nextbus_nextbusmessage(kafka_emulator):
    """Test the NextbusMessage event from the Nextbus message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_nextbus_nextbusmessage',  # Unique group per test
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
            if cloudevent['type'] == "nextbus.Message":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = NextbusEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_Message.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_nextbus_message(_agency_id = f'test_{i}', _route_tag = f'test_{i}', _stop_or_vehicle_id = f'test_{i}', _timestamp = f'test_{i}', data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
        expected_key = "{agency_id}/{route_tag}".format(agency_id=f'test_{i}', route_tag=f'test_{i}')
        assert received_key == expected_key, f"Expected Kafka key '{expected_key}' but got '{received_key}'"
    consumer.close()


def test_nextbus_cross_event_type_kafka_key(kafka_emulator):
    """Test that different event types in Nextbus produce the same Kafka key for the same placeholder values"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_nextbus_cross_key',
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
    producer_instance = NextbusEventProducer(kafka_producer, topic, 'binary')

    shared_key_value = "shared_entity_42"
    data1 = Test_VehiclePosition.create_instance()
    data2 = Test_RouteConfig.create_instance()

    producer_instance.send_nextbus_vehicle_position(_agency_id = shared_key_value, _route_tag = shared_key_value, _vehicle_id = shared_key_value, _timestamp = shared_key_value, data = data1)
    producer_instance.send_nextbus_route_config(_agency_id = shared_key_value, _route_tag = shared_key_value, _stop_or_vehicle_id = shared_key_value, _timestamp = shared_key_value, data = data2)
    kafka_producer.flush(timeout=5.0)

    # Collect keys from both messages
    collected_keys = []
    timeout = time.time() + 20
    while len(collected_keys) < 2 and time.time() < timeout:
        msg = consumer.poll(1.0)
        if msg is None or msg.error():
            continue
        cloudevent = parse_cloudevent(msg)
        if cloudevent['type'] in ["nextbus.VehiclePosition", "nextbus.RouteConfig"]:
            key = msg.key().decode('utf-8') if msg.key() else None
            collected_keys.append(key)

    assert len(collected_keys) == 2, f"Expected 2 messages but received {len(collected_keys)}"
    assert collected_keys[0] == collected_keys[1], \
        f"Expected same Kafka key for different event types but got '{collected_keys[0]}' and '{collected_keys[1]}'"
    expected_key = "{agency_id}/{route_tag}".format(agency_id=shared_key_value, route_tag=shared_key_value)
    assert collected_keys[0] == expected_key, \
        f"Expected Kafka key '{expected_key}' but got '{collected_keys[0]}'"
    consumer.close()