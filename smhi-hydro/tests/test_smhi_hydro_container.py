"""Container tests for the SMHI Hydro bridge with Kafka."""

import json
import pytest
import time
from unittest.mock import patch, MagicMock
from testcontainers.kafka import KafkaContainer
from confluent_kafka import Producer, Consumer
from confluent_kafka.admin import AdminClient, NewTopic

from smhi_hydro.smhi_hydro import SMHIHydroAPI, feed_stations
from smhi_hydro_producer_kafka_producer.producer import SEGovSMHIHydroEventProducer

SAMPLE_STATION_DATA_1 = {
    "key": "1583",
    "name": "VÄSTERSEL",
    "owner": "SMHI",
    "measuringStations": "CORE",
    "region": 36,
    "catchmentName": "MOÄLVEN",
    "catchmentNumber": 36000,
    "catchmentSize": 1465.2,
    "from": 420898500000,
    "to": 1774455300000,
    "latitude": 63.4332,
    "longitude": 18.3034,
    "value": [
        {"date": 1774451700000, "value": 16.0, "quality": "O"},
        {"date": 1774454400000, "value": 16.0, "quality": "O"},
    ]
}

SAMPLE_STATION_DATA_2 = {
    "key": "2305",
    "name": "HULUBÄCKEN",
    "owner": "SMHI",
    "measuringStations": "CORE",
    "region": 101,
    "catchmentName": "NISSAN",
    "catchmentNumber": 101000,
    "catchmentSize": 3.8,
    "from": 354705300000,
    "to": 1774454400000,
    "latitude": 57.7219,
    "longitude": 13.7301,
    "value": [
        {"date": 1774451700000, "value": 0.069, "quality": "O"},
        {"date": 1774453500000, "value": 0.072, "quality": "O"},
    ]
}

SAMPLE_BULK_RESPONSE = {
    "updated": 1774454400000,
    "parameter": {"key": "2", "name": "Vattenföring (15 min)", "unit": "m³/s"},
    "period": {"key": "latest-hour", "from": 1774450801000, "to": 1774454400000},
    "link": [],
    "station": [SAMPLE_STATION_DATA_1, SAMPLE_STATION_DATA_2]
}


@pytest.fixture(scope="module")
def kafka_container():
    """Start a Kafka container for testing."""
    with KafkaContainer() as kafka:
        admin = AdminClient({'bootstrap.servers': kafka.get_bootstrap_server()})
        topic = NewTopic('smhi-hydro', num_partitions=1, replication_factor=1)
        admin.create_topics([topic])
        time.sleep(2)
        yield kafka


class TestSMHIHydroContainer:
    """Tests that run against a real Kafka container."""

    def test_feed_with_mocked_api(self, kafka_container):
        """Test feeding mocked data to a real Kafka broker."""
        bootstrap_server = kafka_container.get_bootstrap_server()
        kafka_config = {'bootstrap.servers': bootstrap_server, 'client.id': 'test-smhi-hydro'}
        producer = Producer(kafka_config)
        event_producer = SEGovSMHIHydroEventProducer(producer, 'smhi-hydro')
        api = SMHIHydroAPI()

        with patch.object(api, 'get_bulk_discharge_data', return_value=SAMPLE_BULK_RESPONSE):
            count = feed_stations(api, event_producer)
        assert count == 4  # 2 stations + 2 observations

        consumer = Consumer({
            'bootstrap.servers': bootstrap_server,
            'group.id': 'test-group',
            'auto.offset.reset': 'earliest',
        })
        consumer.subscribe(['smhi-hydro'])
        messages = []
        deadline = time.time() + 10
        while time.time() < deadline and len(messages) < 4:
            msg = consumer.poll(1.0)
            if msg and not msg.error():
                messages.append(msg)
        consumer.close()

        assert len(messages) == 4
        for msg in messages:
            value = json.loads(msg.value())
            assert 'type' in value
            assert value['source'] == 'https://opendata-download-hydroobs.smhi.se'

    def test_feed_with_live_api(self, kafka_container):
        """Test feeding live API data to a real Kafka broker."""
        bootstrap_server = kafka_container.get_bootstrap_server()
        kafka_config = {'bootstrap.servers': bootstrap_server, 'client.id': 'test-smhi-hydro-live'}
        producer = Producer(kafka_config)
        topic = 'smhi-hydro-live'
        admin = AdminClient({'bootstrap.servers': bootstrap_server})
        admin.create_topics([NewTopic(topic, num_partitions=1, replication_factor=1)])
        time.sleep(1)
        event_producer = SEGovSMHIHydroEventProducer(producer, topic)
        api = SMHIHydroAPI()

        count = feed_stations(api, event_producer)
        assert count > 100  # SMHI has hundreds of stations

        consumer = Consumer({
            'bootstrap.servers': bootstrap_server,
            'group.id': 'test-group-live',
            'auto.offset.reset': 'earliest',
        })
        consumer.subscribe([topic])
        messages = []
        deadline = time.time() + 30
        while time.time() < deadline and len(messages) < 10:
            msg = consumer.poll(1.0)
            if msg and not msg.error():
                messages.append(msg)
        consumer.close()

        assert len(messages) >= 10
        value = json.loads(messages[0].value())
        assert value['source'] == 'https://opendata-download-hydroobs.smhi.se'

    def test_cloudevents_format(self, kafka_container):
        """Test that messages are proper CloudEvents."""
        bootstrap_server = kafka_container.get_bootstrap_server()
        kafka_config = {'bootstrap.servers': bootstrap_server, 'client.id': 'test-smhi-ce'}
        producer = Producer(kafka_config)
        topic = 'smhi-hydro-ce'
        admin = AdminClient({'bootstrap.servers': bootstrap_server})
        admin.create_topics([NewTopic(topic, num_partitions=1, replication_factor=1)])
        time.sleep(1)
        event_producer = SEGovSMHIHydroEventProducer(producer, topic)
        api = SMHIHydroAPI()

        single_station_response = {**SAMPLE_BULK_RESPONSE, "station": [SAMPLE_STATION_DATA_1]}
        with patch.object(api, 'get_bulk_discharge_data', return_value=single_station_response):
            feed_stations(api, event_producer)

        consumer = Consumer({
            'bootstrap.servers': bootstrap_server,
            'group.id': 'test-group-ce',
            'auto.offset.reset': 'earliest',
        })
        consumer.subscribe([topic])
        messages = []
        deadline = time.time() + 10
        while time.time() < deadline and len(messages) < 2:
            msg = consumer.poll(1.0)
            if msg and not msg.error():
                messages.append(msg)
        consumer.close()

        assert len(messages) == 2
        for msg in messages:
            value = json.loads(msg.value())
            assert 'specversion' in value
            assert value['specversion'] == '1.0'
            assert 'type' in value
            assert 'source' in value
            assert 'data' in value
