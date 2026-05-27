"""Container tests for the IMGW Hydro bridge with Kafka."""

import json
import pytest
import time
from unittest.mock import patch, MagicMock
from testcontainers.kafka import KafkaContainer
from confluent_kafka import Producer, Consumer
from confluent_kafka.admin import AdminClient, NewTopic

from imgw_hydro.imgw_hydro import IMGWHydroAPI, feed_stations
from imgw_hydro_producer_kafka_producer.producer import PLGovIMGWHydroEventProducer

SAMPLE_RECORDS = [
    {
        "id_stacji": "150180090",
        "stacja": "Nędza",
        "rzeka": "Sumina",
        "wojewodztwo": "śląskie",
        "lon": "18.5431",
        "lat": "50.3825",
        "stan_wody": "45",
        "stan_wody_data_pomiaru": "2026-03-25 12:00:00",
        "temperatura_wody": "4.8",
        "temperatura_wody_data_pomiaru": "2026-03-25 06:00:00",
        "przeplyw": "0.65",
        "przeplyw_data": "2026-02-18 09:50:00",
        "zjawisko_lodowe": "0",
        "zjawisko_lodowe_data_pomiaru": "2026-02-26 13:40:00",
        "zjawisko_zarastania": "0",
        "zjawisko_zarastania_data_pomiaru": "2026-02-26 13:40:00",
    },
    {
        "id_stacji": "150190010",
        "stacja": "Krzyżanowice",
        "rzeka": "Odra",
        "wojewodztwo": None,
        "lon": None,
        "lat": None,
        "stan_wody": "200",
        "stan_wody_data_pomiaru": "2026-03-25 12:00:00",
        "temperatura_wody": None,
        "temperatura_wody_data_pomiaru": None,
        "przeplyw": None,
        "przeplyw_data": None,
        "zjawisko_lodowe": None,
        "zjawisko_lodowe_data_pomiaru": None,
        "zjawisko_zarastania": None,
        "zjawisko_zarastania_data_pomiaru": None,
    },
]


@pytest.fixture(scope="module")
def kafka_container():
    """Start a Kafka container for testing."""
    with KafkaContainer() as kafka:
        admin = AdminClient({'bootstrap.servers': kafka.get_bootstrap_server()})
        topic = NewTopic('imgw-hydro', num_partitions=1, replication_factor=1)
        admin.create_topics([topic])
        time.sleep(2)
        yield kafka


class TestIMGWHydroContainer:
    """Tests that run against a real Kafka container."""

    def test_feed_with_mocked_api(self, kafka_container):
        """Test feeding mocked data to a real Kafka broker."""
        bootstrap_server = kafka_container.get_bootstrap_server()
        kafka_config = {'bootstrap.servers': bootstrap_server, 'client.id': 'test-imgw-hydro'}
        producer = Producer(kafka_config)
        event_producer = PLGovIMGWHydroEventProducer(producer, 'imgw-hydro')
        api = IMGWHydroAPI()

        with patch.object(api, 'get_all_data', return_value=SAMPLE_RECORDS):
            count = feed_stations(api, event_producer)
        assert count == 4  # 2 stations + 2 observations

        consumer = Consumer({
            'bootstrap.servers': bootstrap_server,
            'group.id': 'test-group',
            'auto.offset.reset': 'earliest',
        })
        consumer.subscribe(['imgw-hydro'])
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
            assert value['source'] == 'https://danepubliczne.imgw.pl'

    def test_feed_with_live_api(self, kafka_container):
        """Test feeding live API data to a real Kafka broker."""
        bootstrap_server = kafka_container.get_bootstrap_server()
        kafka_config = {'bootstrap.servers': bootstrap_server, 'client.id': 'test-imgw-hydro-live'}
        producer = Producer(kafka_config)
        topic = 'imgw-hydro-live'
        admin = AdminClient({'bootstrap.servers': bootstrap_server})
        admin.create_topics([NewTopic(topic, num_partitions=1, replication_factor=1)])
        time.sleep(1)
        event_producer = PLGovIMGWHydroEventProducer(producer, topic)
        api = IMGWHydroAPI()

        count = feed_stations(api, event_producer)
        assert count > 100  # IMGW has hundreds of stations

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
        assert value['source'] == 'https://danepubliczne.imgw.pl'

    def test_cloudevents_format(self, kafka_container):
        """Test that messages are proper CloudEvents."""
        bootstrap_server = kafka_container.get_bootstrap_server()
        kafka_config = {'bootstrap.servers': bootstrap_server, 'client.id': 'test-imgw-ce'}
        producer = Producer(kafka_config)
        topic = 'imgw-hydro-ce'
        admin = AdminClient({'bootstrap.servers': bootstrap_server})
        admin.create_topics([NewTopic(topic, num_partitions=1, replication_factor=1)])
        time.sleep(1)
        event_producer = PLGovIMGWHydroEventProducer(producer, topic)
        api = IMGWHydroAPI()

        with patch.object(api, 'get_all_data', return_value=[SAMPLE_RECORDS[0]]):
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
