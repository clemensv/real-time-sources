"""Container tests for the ČHMÚ Hydro bridge with Kafka."""

import json
import pytest
import time
from unittest.mock import patch, MagicMock
from testcontainers.kafka import KafkaContainer
from confluent_kafka import Producer, Consumer
from confluent_kafka.admin import AdminClient, NewTopic

from chmi_hydro.chmi_hydro import CHMIHydroAPI, feed_stations
from chmi_hydro.chmi_hydro_producer.producer_client import CZGovCHMIHydroEventProducer

SAMPLE_META_RECORDS = [
    ["0-203-1-001000", "001000", "Špindlerův Mlýn", "Labe",
     50.7231692, 15.5980379, "H", "vodní stav", "CM", 88,
     165, 200, 220, 297, "průtok", "M3_S", 0.419,
     19.3, 39.4, 54.5, 137, 0],
    ["0-203-1-042000", "042000", "Němčice", "Labe",
     50.0946613, 15.8067603, "H", "vodní stav", "CM", 54,
     350, 400, 450, 659, "průtok", "M3_S", 10.1,
     200, 249, 307, 725, 1],
]

SAMPLE_STATION_DATA = {
    "0-203-1-001000": {
        "objList": [{
            "objID": "0-203-1-001000",
            "tsList": [
                {"tsConID": "H", "unit": "CM", "tsData": [
                    {"dt": "2026-03-25T00:00:00Z", "value": 96},
                ]},
                {"tsConID": "Q", "unit": "M3_S", "tsData": [
                    {"dt": "2026-03-25T00:00:00Z", "value": 1.08},
                ]}
            ]
        }]
    },
    "0-203-1-042000": {
        "objList": [{
            "objID": "0-203-1-042000",
            "tsList": [
                {"tsConID": "H", "unit": "CM", "tsData": [
                    {"dt": "2026-03-25T12:00:00Z", "value": 150},
                ]},
            ]
        }]
    }
}

SAMPLE_METADATA_RESPONSE = {
    "zaznamID": "test", "datovyZdrojID": "hydrologie",
    "datovyTokID": "Open.Data.Metadata",
    "datumVytvoreni": "2026-03-25T14:00:03Z", "verzeDat": "1.0",
    "data": {"type": "DataCollection", "data": {
        "header": "objID,DBC,STATION_NAME,STREAM_NAME,GEOGR1,GEOGR2,SPA_TYP,SPAH_DS,SPAH_UNIT,DRYH,SPA1H,SPA2H,SPA3H,SPA4H,SPAQ_DS,SPAQ_UNIT,DRYQ,SPA1Q,SPA2Q,SPA3Q,SPA4Q,ISFORECAST",
        "values": SAMPLE_META_RECORDS
    }}
}


@pytest.fixture(scope="module")
def kafka_container():
    """Start a Kafka container for testing."""
    with KafkaContainer() as kafka:
        admin = AdminClient({'bootstrap.servers': kafka.get_bootstrap_server()})
        topic = NewTopic('chmi-hydro', num_partitions=1, replication_factor=1)
        admin.create_topics([topic])
        time.sleep(2)
        yield kafka


class TestCHMIHydroContainer:
    """Tests that run against a real Kafka container."""

    def test_feed_with_mocked_api(self, kafka_container):
        """Test feeding mocked data to a real Kafka broker."""
        bootstrap_server = kafka_container.get_bootstrap_server()
        kafka_config = {'bootstrap.servers': bootstrap_server, 'client.id': 'test-chmi-hydro'}
        producer = Producer(kafka_config)
        event_producer = CZGovCHMIHydroEventProducer(producer, 'chmi-hydro')
        api = CHMIHydroAPI()

        with patch.object(api, 'get_metadata', return_value=SAMPLE_META_RECORDS), \
             patch.object(api, 'get_all_station_data', return_value=SAMPLE_STATION_DATA):
            count = feed_stations(api, event_producer)
        assert count == 4  # 2 stations + 2 observations

        consumer = Consumer({
            'bootstrap.servers': bootstrap_server,
            'group.id': 'test-group',
            'auto.offset.reset': 'earliest',
        })
        consumer.subscribe(['chmi-hydro'])
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
            assert value['source'] == 'https://opendata.chmi.cz'

    def test_feed_with_live_api(self, kafka_container):
        """Test feeding live API data to a real Kafka broker."""
        bootstrap_server = kafka_container.get_bootstrap_server()
        kafka_config = {'bootstrap.servers': bootstrap_server, 'client.id': 'test-chmi-hydro-live'}
        producer = Producer(kafka_config)
        topic = 'chmi-hydro-live'
        admin = AdminClient({'bootstrap.servers': bootstrap_server})
        admin.create_topics([NewTopic(topic, num_partitions=1, replication_factor=1)])
        time.sleep(1)
        event_producer = CZGovCHMIHydroEventProducer(producer, topic)
        api = CHMIHydroAPI()

        count = feed_stations(api, event_producer)
        assert count > 100  # ČHMÚ has hundreds of stations

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
        assert value['source'] == 'https://opendata.chmi.cz'

    def test_cloudevents_format(self, kafka_container):
        """Test that messages are proper CloudEvents."""
        bootstrap_server = kafka_container.get_bootstrap_server()
        kafka_config = {'bootstrap.servers': bootstrap_server, 'client.id': 'test-chmi-ce'}
        producer = Producer(kafka_config)
        topic = 'chmi-hydro-ce'
        admin = AdminClient({'bootstrap.servers': bootstrap_server})
        admin.create_topics([NewTopic(topic, num_partitions=1, replication_factor=1)])
        time.sleep(1)
        event_producer = CZGovCHMIHydroEventProducer(producer, topic)
        api = CHMIHydroAPI()

        with patch.object(api, 'get_metadata', return_value=[SAMPLE_META_RECORDS[0]]), \
             patch.object(api, 'get_all_station_data', return_value={"0-203-1-001000": SAMPLE_STATION_DATA["0-203-1-001000"]}):
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
