# pylint: disable=missing-function-docstring, wrong-import-position, import-error, no-name-in-module, import-outside-toplevel, no-member, redefined-outer-name, unused-argument, unused-variable, invalid-name, redefined-outer-name, missing-class-docstring

import asyncio
import logging
import os
import sys
import datetime
from typing import Optional

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../pegelonline_producer_data/src')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../pegelonline_producer_data/tests')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../pegelonline_producer_kafka_producer/src')))

import tempfile
import pytest
from confluent_kafka import Producer, Consumer, KafkaException, Message
from confluent_kafka.admin import AdminClient, NewTopic
from cloudevents.abstract import CloudEvent
from cloudevents.kafka import from_binary, from_structured, KafkaMessage
from testcontainers.kafka import KafkaContainer
from pegelonline_producer_kafka_producer.producer import DeWsvPegelonlineEventProducer
from test_pegelonline_producer_data_de_wsv_pegelonline_station import Test_Station
from test_pegelonline_producer_data_de_wsv_pegelonline_currentmeasurement import Test_CurrentMeasurement

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

@pytest.mark.asyncio
async def test_de_wsv_pegelonline_dewsvpegelonlinestation(kafka_emulator):
    """Test the DeWsvPegelonlineStation event from the De.Wsv.Pegelonline message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_group',
        'auto.offset.reset': 'earliest'
    })
    consumer.subscribe([topic])

    async def on_event():
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            cloudevent = parse_cloudevent(msg)
            if cloudevent['type'] == "de.wsv.pegelonline.Station":
                return True

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = DeWsvPegelonlineEventProducer(kafka_producer, topic, 'binary')
    event_data = Test_Station.create_instance()
    await producer_instance.send_de_wsv_pegelonline_station(_feedurl = 'test', _station_id = 'test', data = event_data)

    assert await asyncio.wait_for(on_event(), timeout=10)
    consumer.close()

@pytest.mark.asyncio
async def test_de_wsv_pegelonline_dewsvpegelonlinecurrentmeasurement(kafka_emulator):
    """Test the DeWsvPegelonlineCurrentMeasurement event from the De.Wsv.Pegelonline message group"""

    bootstrap_servers = kafka_emulator["bootstrap_servers"]
    topic = kafka_emulator["topic"]

    producer = Producer({'bootstrap.servers': bootstrap_servers})
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_group',
        'auto.offset.reset': 'earliest'
    })
    consumer.subscribe([topic])

    async def on_event():
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            cloudevent = parse_cloudevent(msg)
            if cloudevent['type'] == "de.wsv.pegelonline.CurrentMeasurement":
                return True

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = DeWsvPegelonlineEventProducer(kafka_producer, topic, 'binary')
    event_data = Test_CurrentMeasurement.create_instance()
    await producer_instance.send_de_wsv_pegelonline_current_measurement(_feedurl = 'test', _station_id = 'test', data = event_data)

    assert await asyncio.wait_for(on_event(), timeout=10)
    consumer.close()