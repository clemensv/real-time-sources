# pylint: disable=missing-function-docstring, wrong-import-position, import-error, no-name-in-module, import-outside-toplevel, no-member, redefined-outer-name, unused-argument, unused-variable, invalid-name, redefined-outer-name, missing-class-docstring

import asyncio
import logging
import os
import sys
import datetime
from typing import Optional

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../usgs_iv_producer_data/src')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../usgs_iv_producer_data/tests')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../usgs_iv_producer_kafka_producer/src')))

import tempfile
import pytest
from confluent_kafka import Producer, Consumer, KafkaException, Message
from confluent_kafka.admin import AdminClient, NewTopic
from cloudevents.abstract import CloudEvent
from cloudevents.kafka import from_binary, from_structured, KafkaMessage
from testcontainers.kafka import KafkaContainer
from usgs_iv_producer_kafka_producer.producer import USGSSitesEventProducer
from test_usgs_iv_producer_data_usgs_sites_site import Test_Site
from usgs_iv_producer_kafka_producer.producer import USGSInstantaneousValuesEventProducer
from test_usgs_iv_producer_data_usgs_instantaneousvalues_precipitation import Test_Precipitation
from test_usgs_iv_producer_data_usgs_instantaneousvalues_streamflow import Test_Streamflow
from test_usgs_iv_producer_data_usgs_instantaneousvalues_gageheight import Test_GageHeight
from test_usgs_iv_producer_data_usgs_instantaneousvalues_watertemperature import Test_WaterTemperature
from test_usgs_iv_producer_data_usgs_instantaneousvalues_dissolvedoxygen import Test_DissolvedOxygen
from test_usgs_iv_producer_data_usgs_instantaneousvalues_ph import Test_PH
from test_usgs_iv_producer_data_usgs_instantaneousvalues_specificconductance import Test_SpecificConductance
from test_usgs_iv_producer_data_usgs_instantaneousvalues_turbidity import Test_Turbidity

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
async def test_usgs_sites_usgssitessite(kafka_emulator):
    """Test the USGSSitesSite event from the USGS.Sites message group"""

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
            if cloudevent['type'] == "USGS.Sites.Site":
                return True

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = USGSSitesEventProducer(kafka_producer, topic, 'binary')
    event_data = Test_Site.create_instance()
    await producer_instance.send_usgs_sites_site(_source_uri = 'test', data = event_data)

    assert await asyncio.wait_for(on_event(), timeout=10)
    consumer.close()

@pytest.mark.asyncio
async def test_usgs_instantaneousvalues_usgsinstantaneousvaluesprecipitation(kafka_emulator):
    """Test the USGSInstantaneousValuesPrecipitation event from the USGS.InstantaneousValues message group"""

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
            if cloudevent['type'] == "USGS.InstantaneousValues.Precipitation":
                return True

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = USGSInstantaneousValuesEventProducer(kafka_producer, topic, 'binary')
    event_data = Test_Precipitation.create_instance()
    await producer_instance.send_usgs_instantaneous_values_precipitation(_source_uri = 'test', _agency_cd = 'test', _site_no = 'test', _parameter_cd = 'test', _timeseries_cd = 'test', _datetime = 'test', data = event_data)

    assert await asyncio.wait_for(on_event(), timeout=10)
    consumer.close()

@pytest.mark.asyncio
async def test_usgs_instantaneousvalues_usgsinstantaneousvaluesstreamflow(kafka_emulator):
    """Test the USGSInstantaneousValuesStreamflow event from the USGS.InstantaneousValues message group"""

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
            if cloudevent['type'] == "USGS.InstantaneousValues.Streamflow":
                return True

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = USGSInstantaneousValuesEventProducer(kafka_producer, topic, 'binary')
    event_data = Test_Streamflow.create_instance()
    await producer_instance.send_usgs_instantaneous_values_streamflow(_source_uri = 'test', _agency_cd = 'test', _site_no = 'test', _parameter_cd = 'test', _timeseries_cd = 'test', _datetime = 'test', data = event_data)

    assert await asyncio.wait_for(on_event(), timeout=10)
    consumer.close()

@pytest.mark.asyncio
async def test_usgs_instantaneousvalues_usgsinstantaneousvaluesgageheight(kafka_emulator):
    """Test the USGSInstantaneousValuesGageHeight event from the USGS.InstantaneousValues message group"""

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
            if cloudevent['type'] == "USGS.InstantaneousValues.GageHeight":
                return True

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = USGSInstantaneousValuesEventProducer(kafka_producer, topic, 'binary')
    event_data = Test_GageHeight.create_instance()
    await producer_instance.send_usgs_instantaneous_values_gage_height(_source_uri = 'test', _agency_cd = 'test', _site_no = 'test', _parameter_cd = 'test', _timeseries_cd = 'test', _datetime = 'test', data = event_data)

    assert await asyncio.wait_for(on_event(), timeout=10)
    consumer.close()

@pytest.mark.asyncio
async def test_usgs_instantaneousvalues_usgsinstantaneousvalueswatertemperature(kafka_emulator):
    """Test the USGSInstantaneousValuesWaterTemperature event from the USGS.InstantaneousValues message group"""

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
            if cloudevent['type'] == "USGS.InstantaneousValues.WaterTemperature":
                return True

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = USGSInstantaneousValuesEventProducer(kafka_producer, topic, 'binary')
    event_data = Test_WaterTemperature.create_instance()
    await producer_instance.send_usgs_instantaneous_values_water_temperature(_source_uri = 'test', _agency_cd = 'test', _site_no = 'test', _parameter_cd = 'test', _timeseries_cd = 'test', _datetime = 'test', data = event_data)

    assert await asyncio.wait_for(on_event(), timeout=10)
    consumer.close()

@pytest.mark.asyncio
async def test_usgs_instantaneousvalues_usgsinstantaneousvaluesdissolvedoxygen(kafka_emulator):
    """Test the USGSInstantaneousValuesDissolvedOxygen event from the USGS.InstantaneousValues message group"""

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
            if cloudevent['type'] == "USGS.InstantaneousValues.DissolvedOxygen":
                return True

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = USGSInstantaneousValuesEventProducer(kafka_producer, topic, 'binary')
    event_data = Test_DissolvedOxygen.create_instance()
    await producer_instance.send_usgs_instantaneous_values_dissolved_oxygen(_source_uri = 'test', _agency_cd = 'test', _site_no = 'test', _parameter_cd = 'test', _timeseries_cd = 'test', _datetime = 'test', data = event_data)

    assert await asyncio.wait_for(on_event(), timeout=10)
    consumer.close()

@pytest.mark.asyncio
async def test_usgs_instantaneousvalues_usgsinstantaneousvaluesph(kafka_emulator):
    """Test the USGSInstantaneousValuesPH event from the USGS.InstantaneousValues message group"""

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
            if cloudevent['type'] == "USGS.InstantaneousValues.pH":
                return True

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = USGSInstantaneousValuesEventProducer(kafka_producer, topic, 'binary')
    event_data = Test_PH.create_instance()
    await producer_instance.send_usgs_instantaneous_values_p_h(_source_uri = 'test', _agency_cd = 'test', _site_no = 'test', _parameter_cd = 'test', _timeseries_cd = 'test', _datetime = 'test', data = event_data)

    assert await asyncio.wait_for(on_event(), timeout=10)
    consumer.close()

@pytest.mark.asyncio
async def test_usgs_instantaneousvalues_usgsinstantaneousvaluesspecificconductance(kafka_emulator):
    """Test the USGSInstantaneousValuesSpecificConductance event from the USGS.InstantaneousValues message group"""

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
            if cloudevent['type'] == "USGS.InstantaneousValues.SpecificConductance":
                return True

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = USGSInstantaneousValuesEventProducer(kafka_producer, topic, 'binary')
    event_data = Test_SpecificConductance.create_instance()
    await producer_instance.send_usgs_instantaneous_values_specific_conductance(_source_uri = 'test', _agency_cd = 'test', _site_no = 'test', _parameter_cd = 'test', _timeseries_cd = 'test', _datetime = 'test', data = event_data)

    assert await asyncio.wait_for(on_event(), timeout=10)
    consumer.close()

@pytest.mark.asyncio
async def test_usgs_instantaneousvalues_usgsinstantaneousvaluesturbidity(kafka_emulator):
    """Test the USGSInstantaneousValuesTurbidity event from the USGS.InstantaneousValues message group"""

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
            if cloudevent['type'] == "USGS.InstantaneousValues.Turbidity":
                return True

    kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})
    producer_instance = USGSInstantaneousValuesEventProducer(kafka_producer, topic, 'binary')
    event_data = Test_Turbidity.create_instance()
    await producer_instance.send_usgs_instantaneous_values_turbidity(_source_uri = 'test', _agency_cd = 'test', _site_no = 'test', _parameter_cd = 'test', _timeseries_cd = 'test', _datetime = 'test', data = event_data)

    assert await asyncio.wait_for(on_event(), timeout=10)
    consumer.close()