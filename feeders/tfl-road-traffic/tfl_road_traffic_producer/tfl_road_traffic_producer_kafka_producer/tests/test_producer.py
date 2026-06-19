# pylint: disable=missing-function-docstring, wrong-import-position, import-error, no-name-in-module, import-outside-toplevel, no-member, redefined-outer-name, unused-argument, unused-variable, invalid-name, redefined-outer-name, missing-class-docstring

import asyncio
import logging
import os
import sys
import datetime
from typing import Optional

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../tfl_road_traffic_producer_data/src')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../tfl_road_traffic_producer_data/tests')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../tfl_road_traffic_producer_kafka_producer/src')))

import tempfile
import pytest
from confluent_kafka import Producer, Consumer, KafkaException, Message
from confluent_kafka.admin import AdminClient, NewTopic
from cloudevents.abstract import CloudEvent
from cloudevents.kafka import from_binary, from_structured, KafkaMessage
from testcontainers.kafka import KafkaContainer
from tfl_road_traffic_producer_kafka_producer.producer import UkGovTflRoadCorridorsEventProducer
from tfl_road_traffic_producer_data import RoadCorridor
from test_roadcorridor import Test_RoadCorridor
from tfl_road_traffic_producer_data import RoadStatus
from test_roadstatus import Test_RoadStatus
from tfl_road_traffic_producer_kafka_producer.producer import UkGovTflRoadDisruptionsEventProducer
from tfl_road_traffic_producer_data import RoadDisruption
from test_roaddisruption import Test_RoadDisruption
from tfl_road_traffic_producer_kafka_producer.producer import UkGovTflRoadMqttEventProducer
from tfl_road_traffic_producer_kafka_producer.producer import UkGovTflRoadAmqpEventProducer

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


def test_uk_gov_tfl_road_corridors_ukgovtflroadroadcorridor(kafka_emulator):
    """Test the UkGovTflRoadRoadCorridor event from the Uk.Gov.Tfl.Road.Corridors message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_uk_gov_tfl_road_corridors_ukgovtflroadroadcorridor',  # Unique group per test
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
            if cloudevent['type'] == "uk.gov.tfl.road.RoadCorridor":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = UkGovTflRoadCorridorsEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_RoadCorridor.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_uk_gov_tfl_road_road_corridor(_road_id = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
        expected_key = "roads/{road_id}".format(road_id=f'test_{i}')
        assert received_key == expected_key, f"Expected Kafka key '{expected_key}' but got '{received_key}'"
    consumer.close()


def test_uk_gov_tfl_road_corridors_ukgovtflroadroadstatus(kafka_emulator):
    """Test the UkGovTflRoadRoadStatus event from the Uk.Gov.Tfl.Road.Corridors message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_uk_gov_tfl_road_corridors_ukgovtflroadroadstatus',  # Unique group per test
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
            if cloudevent['type'] == "uk.gov.tfl.road.RoadStatus":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = UkGovTflRoadCorridorsEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_RoadStatus.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_uk_gov_tfl_road_road_status(_road_id = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
        expected_key = "roads/{road_id}".format(road_id=f'test_{i}')
        assert received_key == expected_key, f"Expected Kafka key '{expected_key}' but got '{received_key}'"
    consumer.close()


def test_uk_gov_tfl_road_disruptions_ukgovtflroadroaddisruption(kafka_emulator):
    """Test the UkGovTflRoadRoadDisruption event from the Uk.Gov.Tfl.Road.Disruptions message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_uk_gov_tfl_road_disruptions_ukgovtflroadroaddisruption',  # Unique group per test
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
            if cloudevent['type'] == "uk.gov.tfl.road.RoadDisruption":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = UkGovTflRoadDisruptionsEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_RoadDisruption.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_uk_gov_tfl_road_road_disruption(_road_id = f'test_{i}', _severity = f'test_{i}', _disruption_id = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
        expected_key = "disruptions/{road_id}/{severity}/{disruption_id}".format(road_id=f'test_{i}', severity=f'test_{i}', disruption_id=f'test_{i}')
        assert received_key == expected_key, f"Expected Kafka key '{expected_key}' but got '{received_key}'"
    consumer.close()


def test_uk_gov_tfl_road_mqtt_ukgovtflroadmqttroadcorridor(kafka_emulator):
    """Test the UkGovTflRoadMqttRoadCorridor event from the Uk.Gov.Tfl.Road.Mqtt message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_uk_gov_tfl_road_mqtt_ukgovtflroadmqttroadcorridor',  # Unique group per test
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
            if cloudevent['type'] == "uk.gov.tfl.road.RoadCorridor":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = UkGovTflRoadMqttEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_RoadCorridor.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_uk_gov_tfl_road_mqtt_road_corridor(_road_id = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
    consumer.close()


def test_uk_gov_tfl_road_mqtt_ukgovtflroadmqttroadstatus(kafka_emulator):
    """Test the UkGovTflRoadMqttRoadStatus event from the Uk.Gov.Tfl.Road.Mqtt message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_uk_gov_tfl_road_mqtt_ukgovtflroadmqttroadstatus',  # Unique group per test
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
            if cloudevent['type'] == "uk.gov.tfl.road.RoadStatus":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = UkGovTflRoadMqttEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_RoadStatus.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_uk_gov_tfl_road_mqtt_road_status(_road_id = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
    consumer.close()


def test_uk_gov_tfl_road_mqtt_ukgovtflroadmqttroaddisruptionserious(kafka_emulator):
    """Test the UkGovTflRoadMqttRoadDisruptionSerious event from the Uk.Gov.Tfl.Road.Mqtt message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_uk_gov_tfl_road_mqtt_ukgovtflroadmqttroaddisruptionserious',  # Unique group per test
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
            if cloudevent['type'] == "uk.gov.tfl.road.RoadDisruption":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = UkGovTflRoadMqttEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_RoadDisruption.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_uk_gov_tfl_road_mqtt_road_disruption_serious(_road_id = f'test_{i}', _severity = f'test_{i}', _disruption_id = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
    consumer.close()


def test_uk_gov_tfl_road_mqtt_ukgovtflroadmqttroaddisruptionsevere(kafka_emulator):
    """Test the UkGovTflRoadMqttRoadDisruptionSevere event from the Uk.Gov.Tfl.Road.Mqtt message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_uk_gov_tfl_road_mqtt_ukgovtflroadmqttroaddisruptionsevere',  # Unique group per test
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
            if cloudevent['type'] == "uk.gov.tfl.road.RoadDisruption":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = UkGovTflRoadMqttEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_RoadDisruption.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_uk_gov_tfl_road_mqtt_road_disruption_severe(_road_id = f'test_{i}', _severity = f'test_{i}', _disruption_id = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
    consumer.close()


def test_uk_gov_tfl_road_mqtt_ukgovtflroadmqttroaddisruptionmoderate(kafka_emulator):
    """Test the UkGovTflRoadMqttRoadDisruptionModerate event from the Uk.Gov.Tfl.Road.Mqtt message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_uk_gov_tfl_road_mqtt_ukgovtflroadmqttroaddisruptionmoderate',  # Unique group per test
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
            if cloudevent['type'] == "uk.gov.tfl.road.RoadDisruption":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = UkGovTflRoadMqttEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_RoadDisruption.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_uk_gov_tfl_road_mqtt_road_disruption_moderate(_road_id = f'test_{i}', _severity = f'test_{i}', _disruption_id = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
    consumer.close()


def test_uk_gov_tfl_road_mqtt_ukgovtflroadmqttroaddisruptionminor(kafka_emulator):
    """Test the UkGovTflRoadMqttRoadDisruptionMinor event from the Uk.Gov.Tfl.Road.Mqtt message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_uk_gov_tfl_road_mqtt_ukgovtflroadmqttroaddisruptionminor',  # Unique group per test
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
            if cloudevent['type'] == "uk.gov.tfl.road.RoadDisruption":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = UkGovTflRoadMqttEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_RoadDisruption.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_uk_gov_tfl_road_mqtt_road_disruption_minor(_road_id = f'test_{i}', _severity = f'test_{i}', _disruption_id = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
    consumer.close()


def test_uk_gov_tfl_road_mqtt_ukgovtflroadmqttroaddisruptioninformation(kafka_emulator):
    """Test the UkGovTflRoadMqttRoadDisruptionInformation event from the Uk.Gov.Tfl.Road.Mqtt message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_uk_gov_tfl_road_mqtt_ukgovtflroadmqttroaddisruptioninformation',  # Unique group per test
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
            if cloudevent['type'] == "uk.gov.tfl.road.RoadDisruption":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = UkGovTflRoadMqttEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_RoadDisruption.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_uk_gov_tfl_road_mqtt_road_disruption_information(_road_id = f'test_{i}', _severity = f'test_{i}', _disruption_id = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
    consumer.close()


def test_uk_gov_tfl_road_mqtt_ukgovtflroadmqttroaddisruptionclosure(kafka_emulator):
    """Test the UkGovTflRoadMqttRoadDisruptionClosure event from the Uk.Gov.Tfl.Road.Mqtt message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_uk_gov_tfl_road_mqtt_ukgovtflroadmqttroaddisruptionclosure',  # Unique group per test
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
            if cloudevent['type'] == "uk.gov.tfl.road.RoadDisruption":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = UkGovTflRoadMqttEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_RoadDisruption.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_uk_gov_tfl_road_mqtt_road_disruption_closure(_road_id = f'test_{i}', _severity = f'test_{i}', _disruption_id = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
    consumer.close()


def test_uk_gov_tfl_road_amqp_ukgovtflroadamqproadcorridor(kafka_emulator):
    """Test the UkGovTflRoadAmqpRoadCorridor event from the Uk.Gov.Tfl.Road.Amqp message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_uk_gov_tfl_road_amqp_ukgovtflroadamqproadcorridor',  # Unique group per test
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
            if cloudevent['type'] == "uk.gov.tfl.road.RoadCorridor":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = UkGovTflRoadAmqpEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_RoadCorridor.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_uk_gov_tfl_road_amqp_road_corridor(_road_id = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
    consumer.close()


def test_uk_gov_tfl_road_amqp_ukgovtflroadamqproadstatus(kafka_emulator):
    """Test the UkGovTflRoadAmqpRoadStatus event from the Uk.Gov.Tfl.Road.Amqp message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_uk_gov_tfl_road_amqp_ukgovtflroadamqproadstatus',  # Unique group per test
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
            if cloudevent['type'] == "uk.gov.tfl.road.RoadStatus":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = UkGovTflRoadAmqpEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_RoadStatus.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_uk_gov_tfl_road_amqp_road_status(_road_id = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
    consumer.close()


def test_uk_gov_tfl_road_amqp_ukgovtflroadamqproaddisruptionserious(kafka_emulator):
    """Test the UkGovTflRoadAmqpRoadDisruptionSerious event from the Uk.Gov.Tfl.Road.Amqp message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_uk_gov_tfl_road_amqp_ukgovtflroadamqproaddisruptionserious',  # Unique group per test
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
            if cloudevent['type'] == "uk.gov.tfl.road.RoadDisruption":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = UkGovTflRoadAmqpEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_RoadDisruption.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_uk_gov_tfl_road_amqp_road_disruption_serious(_road_id = f'test_{i}', _severity = f'test_{i}', _disruption_id = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
    consumer.close()


def test_uk_gov_tfl_road_amqp_ukgovtflroadamqproaddisruptionsevere(kafka_emulator):
    """Test the UkGovTflRoadAmqpRoadDisruptionSevere event from the Uk.Gov.Tfl.Road.Amqp message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_uk_gov_tfl_road_amqp_ukgovtflroadamqproaddisruptionsevere',  # Unique group per test
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
            if cloudevent['type'] == "uk.gov.tfl.road.RoadDisruption":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = UkGovTflRoadAmqpEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_RoadDisruption.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_uk_gov_tfl_road_amqp_road_disruption_severe(_road_id = f'test_{i}', _severity = f'test_{i}', _disruption_id = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
    consumer.close()


def test_uk_gov_tfl_road_amqp_ukgovtflroadamqproaddisruptionmoderate(kafka_emulator):
    """Test the UkGovTflRoadAmqpRoadDisruptionModerate event from the Uk.Gov.Tfl.Road.Amqp message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_uk_gov_tfl_road_amqp_ukgovtflroadamqproaddisruptionmoderate',  # Unique group per test
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
            if cloudevent['type'] == "uk.gov.tfl.road.RoadDisruption":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = UkGovTflRoadAmqpEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_RoadDisruption.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_uk_gov_tfl_road_amqp_road_disruption_moderate(_road_id = f'test_{i}', _severity = f'test_{i}', _disruption_id = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
    consumer.close()


def test_uk_gov_tfl_road_amqp_ukgovtflroadamqproaddisruptionminor(kafka_emulator):
    """Test the UkGovTflRoadAmqpRoadDisruptionMinor event from the Uk.Gov.Tfl.Road.Amqp message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_uk_gov_tfl_road_amqp_ukgovtflroadamqproaddisruptionminor',  # Unique group per test
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
            if cloudevent['type'] == "uk.gov.tfl.road.RoadDisruption":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = UkGovTflRoadAmqpEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_RoadDisruption.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_uk_gov_tfl_road_amqp_road_disruption_minor(_road_id = f'test_{i}', _severity = f'test_{i}', _disruption_id = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
    consumer.close()


def test_uk_gov_tfl_road_amqp_ukgovtflroadamqproaddisruptioninformation(kafka_emulator):
    """Test the UkGovTflRoadAmqpRoadDisruptionInformation event from the Uk.Gov.Tfl.Road.Amqp message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_uk_gov_tfl_road_amqp_ukgovtflroadamqproaddisruptioninformation',  # Unique group per test
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
            if cloudevent['type'] == "uk.gov.tfl.road.RoadDisruption":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = UkGovTflRoadAmqpEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_RoadDisruption.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_uk_gov_tfl_road_amqp_road_disruption_information(_road_id = f'test_{i}', _severity = f'test_{i}', _disruption_id = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
    consumer.close()


def test_uk_gov_tfl_road_amqp_ukgovtflroadamqproaddisruptionclosure(kafka_emulator):
    """Test the UkGovTflRoadAmqpRoadDisruptionClosure event from the Uk.Gov.Tfl.Road.Amqp message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_uk_gov_tfl_road_amqp_ukgovtflroadamqproaddisruptionclosure',  # Unique group per test
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
            if cloudevent['type'] == "uk.gov.tfl.road.RoadDisruption":
                return msg.key().decode('utf-8') if msg.key() else None

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = UkGovTflRoadAmqpEventProducer(kafka_producer, topic, 'binary')
    # Create valid test data using the test helper
    event_data = Test_RoadDisruption.create_instance()
    
    # Send 5 messages to test message settlement and ordering
    for i in range(5):
        producer_instance.send_uk_gov_tfl_road_amqp_road_disruption_closure(_road_id = f'test_{i}', _severity = f'test_{i}', _disruption_id = f'test_{i}', _time = datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data = event_data)
    
    # Flush producer to ensure messages are sent before consumer polling
    kafka_producer.flush(timeout=5.0)

    # Verify all 5 messages received and assert Kafka key
    for i in range(5):
        received_key = on_event()
        assert received_key is not None, f"Failed to receive message {i+1} of 5"
    consumer.close()


def test_uk_gov_tfl_road_corridors_cross_event_type_kafka_key(kafka_emulator):
    """Test that different event types in Uk.Gov.Tfl.Road.Corridors produce the same Kafka key for the same placeholder values"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_uk_gov_tfl_road_corridors_cross_key',
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
    producer_instance = UkGovTflRoadCorridorsEventProducer(kafka_producer, topic, 'binary')

    shared_key_value = "shared_entity_42"
    data1 = Test_RoadCorridor.create_instance()
    data2 = Test_RoadStatus.create_instance()

    producer_instance.send_uk_gov_tfl_road_road_corridor(_road_id = shared_key_value, data = data1)
    producer_instance.send_uk_gov_tfl_road_road_status(_road_id = shared_key_value, data = data2)
    kafka_producer.flush(timeout=5.0)

    # Collect keys from both messages
    collected_keys = []
    timeout = time.time() + 20
    while len(collected_keys) < 2 and time.time() < timeout:
        msg = consumer.poll(1.0)
        if msg is None or msg.error():
            continue
        cloudevent = parse_cloudevent(msg)
        if cloudevent['type'] in ["uk.gov.tfl.road.RoadCorridor", "uk.gov.tfl.road.RoadStatus"]:
            key = msg.key().decode('utf-8') if msg.key() else None
            collected_keys.append(key)

    assert len(collected_keys) == 2, f"Expected 2 messages but received {len(collected_keys)}"
    assert collected_keys[0] == collected_keys[1], \
        f"Expected same Kafka key for different event types but got '{collected_keys[0]}' and '{collected_keys[1]}'"
    expected_key = "roads/{road_id}".format(road_id=shared_key_value)
    assert collected_keys[0] == expected_key, \
        f"Expected Kafka key '{expected_key}' but got '{collected_keys[0]}'"
    consumer.close()