"""
Container integration test for the NASA FIRMS active-fire poller.
Runs against a real Kafka container using testcontainers.
Requires Docker to be running.
"""

# pylint: disable=missing-function-docstring, redefined-outer-name

import time
from typing import Dict
from unittest.mock import AsyncMock, Mock

import pytest
from confluent_kafka import Producer, Consumer, Message
from confluent_kafka.admin import AdminClient, NewTopic
from cloudevents.abstract import CloudEvent
from cloudevents.kafka import from_binary, from_structured, KafkaMessage
from testcontainers.kafka import KafkaContainer

from nasa_firms_producer_data import (
    FireDetection,
    DataAvailability,
    InstrumentEnum,
    ConfidenceLevelenum,
    DaynightEnum,
)
from nasa_firms_producer_kafka_producer.producer import NASAFIRMSEventProducer
from nasa_firms.nasa_firms import FirmsPoller, SOURCE_URI


VIIRS_CSV = (
    "latitude,longitude,bright_ti4,scan,track,acq_date,acq_time,satellite,"
    "instrument,confidence,version,bright_ti5,frp,daynight\n"
    "-12.345,34.567,330.1,0.45,0.39,2024-01-15,112,N,VIIRS,n,2.0NRT,295.0,12.7,D\n"
    "10.000,20.000,350.0,0.5,0.4,2024-01-15,113,N,VIIRS,h,2.0NRT,300.0,55.0,D\n"
)
AVAILABILITY_CSV = "data_id,min_date,max_date\nVIIRS_SNPP_NRT,2024-01-01,2024-01-15\n"


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
    deadline = time.time() + timeout_secs
    while time.time() < deadline:
        msg = consumer.poll(1.0)
        if msg is None or msg.error():
            continue
        cloudevent = parse_cloudevent(msg)
        if cloudevent['type'] == expected_type:
            return cloudevent
    pytest.fail(f"Did not receive event of type '{expected_type}' within {timeout_secs}s")


def _detection() -> FireDetection:
    return FireDetection(
        source="VIIRS_SNPP_NRT",
        record_id="a1b2c3d4e5f60718",
        latitude=-12.345,
        longitude=34.567,
        brightness=None,
        bright_t31=None,
        bright_ti4=330.1,
        bright_ti5=295.0,
        scan=0.45,
        track=0.39,
        acq_date="2024-01-15",
        acq_time="0112",
        acq_datetime="2024-01-15T01:12:00Z",
        satellite="N",
        instrument=InstrumentEnum.VIIRS,
        confidence="n",
        confidence_level=ConfidenceLevelenum.nominal,
        version="2.0NRT",
        frp=12.7,
        daynight=DaynightEnum.D,
        tile="lat-20_lon30",
    )


def test_send_fire_detection_structured(kafka_emulator):
    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic_structured"]
    consumer = make_consumer(bootstrap_servers, topic, 'test_structured')

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer = NASAFIRMSEventProducer(kafka_producer, topic, 'structured')

    det = _detection()
    producer.send_nasa_firms_fire_detection(
        _source_uri=SOURCE_URI,
        _source=det.source,
        _record_id=det.record_id,
        _time=det.acq_datetime,
        data=det,
    )
    kafka_producer.flush(timeout=5.0)

    ce = poll_for_event(consumer, "NASA.FIRMS.FireDetection")
    assert ce['type'] == "NASA.FIRMS.FireDetection"
    assert ce['subject'] == "VIIRS_SNPP_NRT/a1b2c3d4e5f60718"
    assert ce['time'] == "2024-01-15T01:12:00Z"
    data = ce.data
    assert data['source'] == "VIIRS_SNPP_NRT"
    assert data['latitude'] == -12.345
    assert data['longitude'] == 34.567
    assert data['frp'] == 12.7
    consumer.close()


def test_send_fire_detection_binary(kafka_emulator):
    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic_binary"]
    consumer = make_consumer(bootstrap_servers, topic, 'test_binary')

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer = NASAFIRMSEventProducer(kafka_producer, topic, 'binary')

    det = _detection()
    producer.send_nasa_firms_fire_detection(
        _source_uri=SOURCE_URI,
        _source=det.source,
        _record_id=det.record_id,
        _time=det.acq_datetime,
        data=det,
    )
    kafka_producer.flush(timeout=5.0)

    ce = poll_for_event(consumer, "NASA.FIRMS.FireDetection")
    assert ce['type'] == "NASA.FIRMS.FireDetection"
    assert ce['subject'] == "VIIRS_SNPP_NRT/a1b2c3d4e5f60718"
    consumer.close()


def test_send_data_availability_reference(kafka_emulator):
    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic_binary"]
    consumer = make_consumer(bootstrap_servers, topic, 'test_reference')

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer = NASAFIRMSEventProducer(kafka_producer, topic, 'structured')

    rec = DataAvailability(
        source="MODIS_NRT",
        record_id="coverage",
        data_id="MODIS_NRT",
        min_date="2024-01-01",
        max_date="2024-01-15",
        instrument=InstrumentEnum.MODIS,
        satellite="Terra/Aqua",
        resolution_m=1000.0,
        retrieved_at="2024-01-15T00:00:00+00:00",
    )
    producer.send_nasa_firms_data_availability(
        _source_uri=SOURCE_URI,
        _source=rec.source,
        _record_id=rec.record_id,
        _time=rec.retrieved_at,
        data=rec,
    )
    kafka_producer.flush(timeout=5.0)

    ce = poll_for_event(consumer, "NASA.FIRMS.DataAvailability")
    assert ce['type'] == "NASA.FIRMS.DataAvailability"
    assert ce['subject'] == "MODIS_NRT/coverage"
    assert ce.data['data_id'] == "MODIS_NRT"
    consumer.close()


@pytest.mark.asyncio
async def test_poll_and_send_to_kafka(kafka_emulator):
    """Full pipeline: mocked FIRMS CSV -> poller -> Kafka container."""
    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic_live"]
    consumer = make_consumer(bootstrap_servers, topic, 'test_live_pipeline')

    poller = FirmsPoller(
        map_key='k',
        kafka_config={'bootstrap.servers': bootstrap_servers},
        kafka_topic=topic,
        sources=['VIIRS_SNPP_NRT'],
        last_polled_file=None,
    )
    poller._fetch_text = AsyncMock(side_effect=[AVAILABILITY_CSV, VIIRS_CSV])
    await poller.poll_and_send(once=True)
    poller.event_producer.producer.flush(timeout=5.0)

    ce = poll_for_event(consumer, "NASA.FIRMS.FireDetection")
    assert ce['type'] == "NASA.FIRMS.FireDetection"
    assert ce['subject'].startswith("VIIRS_SNPP_NRT/")
    assert ce.data['latitude'] is not None
    assert ce.data['longitude'] is not None
    consumer.close()
