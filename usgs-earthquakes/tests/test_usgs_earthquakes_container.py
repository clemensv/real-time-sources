"""
Container integration test for USGS Earthquake data poller.
Runs against a real Kafka container using testcontainers.
Requires Docker to be running.
"""

# pylint: disable=missing-function-docstring, redefined-outer-name

import json
import time
from typing import Dict

import pytest
from confluent_kafka import Producer, Consumer, Message
from confluent_kafka.admin import AdminClient, NewTopic
from cloudevents.abstract import CloudEvent
from cloudevents.kafka import from_binary, from_structured, KafkaMessage
from testcontainers.kafka import KafkaContainer

from usgs_earthquakes.usgs_earthquakes_producer.usgs.earthquakes.event import Event
from usgs_earthquakes.usgs_earthquakes_producer.producer_client import USGSEarthquakesEventProducer
from usgs_earthquakes.usgs_earthquakes import USGSEarthquakePoller


@pytest.fixture(scope="module")
def kafka_emulator():
    with KafkaContainer() as kafka:
        admin_client = AdminClient({'bootstrap.servers': kafka.get_bootstrap_server()})
        topic_list = [
            NewTopic("test_structured", num_partitions=1, replication_factor=1),
            NewTopic("test_binary", num_partitions=1, replication_factor=1),
            NewTopic("test_live", num_partitions=1, replication_factor=1),
        ]
        admin_client.create_topics(topic_list)

        yield {
            "bootstrap_servers": kafka.get_bootstrap_server(),
            "topic_structured": "test_structured",
            "topic_binary": "test_binary",
            "topic_live": "test_live",
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


def make_consumer(bootstrap_servers: str, topic: str, group_id: str) -> Consumer:
    """Create a consumer, subscribe to topic, and wait for partition assignment."""
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': group_id,
        'auto.offset.reset': 'earliest'
    })
    consumer.subscribe([topic])

    assignment_timeout = time.time() + 10
    while not consumer.assignment() and time.time() < assignment_timeout:
        consumer.poll(0.1)

    if not consumer.assignment():
        pytest.fail(f"Consumer failed to get partition assignment within 10 seconds. Topic: {topic}")

    time.sleep(1)
    return consumer


def poll_for_event(consumer: Consumer, expected_type: str, timeout_secs: int = 20) -> CloudEvent:
    """Poll for a CloudEvent of the expected type. Returns the event or fails."""
    deadline = time.time() + timeout_secs
    while time.time() < deadline:
        msg = consumer.poll(1.0)
        if msg is None or msg.error():
            continue
        cloudevent = parse_cloudevent(msg)
        if cloudevent['type'] == expected_type:
            return cloudevent
    pytest.fail(f"Did not receive event of type '{expected_type}' within {timeout_secs}s")


def test_send_earthquake_event_structured(kafka_emulator):
    """Test sending an earthquake event in structured CloudEvents mode to a Kafka container."""
    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic_structured"]

    consumer = make_consumer(bootstrap_servers, topic, 'test_structured')

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer = USGSEarthquakesEventProducer(kafka_producer, topic, 'structured')

    event = Event(
        id="us7000test",
        magnitude=5.2,
        mag_type="mww",
        place="50km NW of Test City, Country",
        event_time="2024-01-15T10:30:00+00:00",
        updated="2024-01-15T10:35:00+00:00",
        url="https://earthquake.usgs.gov/earthquakes/eventpage/us7000test",
        detail_url="https://earthquake.usgs.gov/fdsnws/event/1/query?eventid=us7000test&format=geojson",
        felt=100,
        cdi=4.5,
        mmi=5.0,
        alert="green",
        status="reviewed",
        tsunami=0,
        sig=450,
        net="us",
        code="7000test",
        sources=",us,ci,",
        nst=30,
        dmin=1.2,
        rms=0.65,
        gap=60.0,
        event_type="earthquake",
        latitude=35.2,
        longitude=-120.5,
        depth=15.0
    )

    producer.send_usgs_earthquakes_event(
        _source_uri="https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/",
        _net="us",
        _code="7000test",
        _event_time="2024-01-15T10:30:00+00:00",
        data=event
    )
    kafka_producer.flush(timeout=5.0)

    ce = poll_for_event(consumer, "USGS.Earthquakes.Event")
    assert ce['type'] == "USGS.Earthquakes.Event"
    assert ce['subject'] == "us/7000test"
    assert 'source' in ce.get_attributes()

    # Verify the data payload
    data = ce.data
    assert data['id'] == "us7000test"
    assert data['magnitude'] == 5.2
    assert data['place'] == "50km NW of Test City, Country"
    assert data['latitude'] == 35.2
    assert data['longitude'] == -120.5
    assert data['depth'] == 15.0

    consumer.close()


def test_send_earthquake_event_binary(kafka_emulator):
    """Test sending an earthquake event in binary CloudEvents mode to a Kafka container."""
    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic_binary"]

    consumer = make_consumer(bootstrap_servers, topic, 'test_binary')

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer = USGSEarthquakesEventProducer(kafka_producer, topic, 'binary')

    event = Event(
        id="ci12345678",
        magnitude=2.1,
        mag_type="ml",
        place="5km E of Small Town, CA",
        event_time="2024-01-15T11:00:00+00:00",
        updated="2024-01-15T11:05:00+00:00",
        url=None,
        detail_url=None,
        felt=None,
        cdi=None,
        mmi=None,
        alert=None,
        status="automatic",
        tsunami=0,
        sig=68,
        net="ci",
        code="12345678",
        sources=",ci,",
        nst=12,
        dmin=0.03,
        rms=0.12,
        gap=90.0,
        event_type="earthquake",
        latitude=33.8,
        longitude=-117.2,
        depth=8.5
    )

    producer.send_usgs_earthquakes_event(
        _source_uri="https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/",
        _net="ci",
        _code="12345678",
        _event_time="2024-01-15T11:00:00+00:00",
        data=event
    )
    kafka_producer.flush(timeout=5.0)

    ce = poll_for_event(consumer, "USGS.Earthquakes.Event")
    assert ce['type'] == "USGS.Earthquakes.Event"
    assert ce['subject'] == "ci/12345678"

    consumer.close()


@pytest.mark.asyncio
async def test_poll_and_send_live_to_kafka(kafka_emulator):
    """
    End-to-end test: fetch real earthquake events from the USGS API
    and send them to a Kafka container. Verifies the full pipeline.
    """
    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic_live"]

    consumer = make_consumer(bootstrap_servers, topic, 'test_live_pipeline')

    kafka_config = {
        'bootstrap.servers': bootstrap_servers,
    }

    poller = USGSEarthquakePoller(
        kafka_config=kafka_config,
        kafka_topic=topic,
        last_polled_file=None,
        feed='all_hour'
    )

    # Fetch real data from USGS and send to Kafka
    features = await poller.fetch_feed()
    count = 0
    for feature in features:
        event = poller.parse_event(feature)
        if event is None:
            continue
        poller.event_producer.send_usgs_earthquakes_event(
            _source_uri=poller.BASE_URL,
            _net=event.net,
            _code=event.code,
            _event_time=event.event_time,
            data=event,
            flush_producer=False
        )
        count += 1
        if count >= 3:
            break

    poller.event_producer.producer.flush(timeout=5.0)

    if count == 0:
        pytest.skip("No earthquake events available in the past hour")

    # Verify at least one event arrived
    ce = poll_for_event(consumer, "USGS.Earthquakes.Event")
    assert ce['type'] == "USGS.Earthquakes.Event"
    assert ce['subject']  # net/code should be present
    assert ce.data['id']  # Real event ID
    assert ce.data['latitude'] is not None
    assert ce.data['longitude'] is not None

    consumer.close()
