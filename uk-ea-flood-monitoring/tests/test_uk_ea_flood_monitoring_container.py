"""
Container integration tests for UK EA Flood Monitoring poller.
Tests with a real Kafka container using testcontainers.

Run with: pytest tests/test_uk_ea_flood_monitoring_container.py -v
"""

import pytest
import json
import time
from unittest.mock import patch, Mock


SAMPLE_STATIONS_RESPONSE = {
    "items": [
        {
            "@id": "http://environment.data.gov.uk/flood-monitoring/id/stations/1029TH",
            "stationReference": "1029TH",
            "label": "Bourton Dickler",
            "riverName": "River Dikler",
            "catchmentName": "Cotswolds",
            "town": "Little Rissington",
            "lat": 51.874767,
            "long": -1.740083,
            "notation": "1029TH",
            "status": "http://environment.data.gov.uk/flood-monitoring/def/core/statusActive",
            "dateOpened": "1994-01-01",
            "measures": [
                {
                    "@id": "http://environment.data.gov.uk/flood-monitoring/id/measures/1029TH-level-stage-i-15_min-mASD",
                    "parameter": "level",
                    "parameterName": "Water Level",
                    "period": 900,
                    "qualifier": "Stage",
                    "unitName": "mASD"
                }
            ]
        },
        {
            "@id": "http://environment.data.gov.uk/flood-monitoring/id/stations/E2043",
            "stationReference": "E2043",
            "label": "Wallingford",
            "riverName": "River Thames",
            "catchmentName": "Thames",
            "town": "Wallingford",
            "lat": 51.601,
            "long": -1.125,
            "notation": "E2043",
            "status": "http://environment.data.gov.uk/flood-monitoring/def/core/statusActive",
            "dateOpened": "1990-01-01",
            "measures": [
                {
                    "@id": "http://environment.data.gov.uk/flood-monitoring/id/measures/E2043-level-stage-i-15_min-mASD",
                    "parameter": "level",
                    "parameterName": "Water Level",
                    "period": 900,
                    "qualifier": "Stage",
                    "unitName": "mASD"
                }
            ]
        }
    ]
}

SAMPLE_READINGS_RESPONSE = {
    "items": [
        {
            "@id": "http://environment.data.gov.uk/flood-monitoring/data/readings/1029TH-level-stage-i-15_min-mASD/2024-06-15T12-00-00Z",
            "dateTime": "2024-06-15T12:00:00Z",
            "measure": "http://environment.data.gov.uk/flood-monitoring/id/measures/1029TH-level-stage-i-15_min-mASD",
            "value": 0.245
        },
        {
            "@id": "http://environment.data.gov.uk/flood-monitoring/data/readings/E2043-level-stage-i-15_min-mASD/2024-06-15T12-00-00Z",
            "dateTime": "2024-06-15T12:00:00Z",
            "measure": "http://environment.data.gov.uk/flood-monitoring/id/measures/E2043-level-stage-i-15_min-mASD",
            "value": 1.350
        }
    ]
}


@pytest.mark.integration
class TestEAFloodMonitoringContainerIntegration:
    """Integration tests using a real Kafka container."""

    @pytest.fixture(scope="class")
    def kafka_container(self):
        """Start a KafkaContainer for the test session."""
        from testcontainers.kafka import KafkaContainer
        container = KafkaContainer()
        container.start()
        yield container
        container.stop()

    @pytest.fixture
    def kafka_config(self, kafka_container):
        """Build Kafka config from the running container."""
        bootstrap_servers = kafka_container.get_bootstrap_server()
        return {
            'bootstrap.servers': bootstrap_servers,
            'security.protocol': 'PLAINTEXT',
        }

    @pytest.fixture
    def kafka_topic(self):
        return 'test-ea-flood-monitoring'

    def _create_topic(self, kafka_container, topic_name):
        """Create a Kafka topic using the container's admin client."""
        from confluent_kafka.admin import AdminClient, NewTopic
        bootstrap_servers = kafka_container.get_bootstrap_server()
        admin = AdminClient({'bootstrap.servers': bootstrap_servers})
        new_topic = NewTopic(topic_name, num_partitions=1, replication_factor=1)
        futures = admin.create_topics([new_topic])
        for topic, future in futures.items():
            try:
                future.result()
            except Exception:
                pass

    @patch('uk_ea_flood_monitoring.uk_ea_flood_monitoring.EAFloodMonitoringAPI.list_stations')
    @patch('uk_ea_flood_monitoring.uk_ea_flood_monitoring.EAFloodMonitoringAPI.get_latest_readings')
    def test_readings_delivered_to_kafka(self, mock_readings, mock_stations,
                                         kafka_container, kafka_config, kafka_topic):
        """Test that readings are fetched and delivered to Kafka."""
        topic = 'test-ea-readings'
        self._create_topic(kafka_container, topic)

        mock_stations.return_value = SAMPLE_STATIONS_RESPONSE["items"]
        mock_readings.return_value = SAMPLE_READINGS_RESPONSE["items"]

        from uk_ea_flood_monitoring.uk_ea_flood_monitoring import EAFloodMonitoringAPI
        from uk_ea_flood_monitoring.uk_ea_flood_monitoring_producer.producer_client import UKGovEnvironmentEAFloodMonitoringEventProducer
        from uk_ea_flood_monitoring.uk_ea_flood_monitoring_producer.uk.gov.environment.ea.floodmonitoring.station import Station
        from uk_ea_flood_monitoring.uk_ea_flood_monitoring_producer.uk.gov.environment.ea.floodmonitoring.reading import Reading
        from confluent_kafka import Producer

        producer = Producer(kafka_config)
        ea_producer = UKGovEnvironmentEAFloodMonitoringEventProducer(producer, topic)

        api = EAFloodMonitoringAPI()
        stations = api.list_stations()
        measure_map = api.build_measure_map(stations)

        # Send station reference data
        for station in stations:
            station_ref = station.get("stationReference", "")
            station_data = Station(
                station_reference=station_ref,
                label=station.get("label", ""),
                river_name=station.get("riverName", ""),
                catchment_name=station.get("catchmentName", ""),
                town=station.get("town", ""),
                lat=station.get("lat", 0.0),
                long=station.get("long", 0.0),
                notation=station.get("notation", ""),
                status=station.get("status", ""),
                date_opened=station.get("dateOpened", "")
            )
            ea_producer.send_uk_gov_environment_ea_flood_monitoring_station(
                station_data, flush_producer=False)

        # Send readings
        readings = api.get_latest_readings()
        for item in readings:
            measure_uri = item.get("measure", "")
            station_ref = measure_map.get(measure_uri, "")
            reading_data = Reading(
                station_reference=station_ref,
                date_time=item.get("dateTime", ""),
                measure=measure_uri,
                value=float(item.get("value", 0))
            )
            ea_producer.send_uk_gov_environment_ea_flood_monitoring_reading(
                reading_data, flush_producer=False)

        producer.flush()

        # Consume messages from Kafka
        from confluent_kafka import Consumer
        consumer_config = {
            'bootstrap.servers': kafka_container.get_bootstrap_server(),
            'group.id': 'test-consumer-group-ea',
            'auto.offset.reset': 'earliest',
            'security.protocol': 'PLAINTEXT',
        }
        consumer = Consumer(consumer_config)
        consumer.subscribe([topic])

        messages = []
        deadline = time.time() + 30
        while len(messages) < 4 and time.time() < deadline:
            msg = consumer.poll(timeout=1.0)
            if msg is not None and not msg.error():
                messages.append(msg)

        consumer.close()

        # 2 stations + 2 readings = 4 messages
        assert len(messages) == 4, f"Expected 4 messages in Kafka, got {len(messages)}"

        # Verify at least one message has station data
        station_messages = []
        reading_messages = []
        for msg in messages:
            value = json.loads(msg.value().decode('utf-8'))
            if 'data' in value:
                data = value['data']
            else:
                data = value
            if 'station_reference' in data and 'label' in data:
                station_messages.append(data)
            elif 'measure' in data and 'value' in data:
                reading_messages.append(data)

        assert len(station_messages) == 2
        assert len(reading_messages) == 2

    @patch('uk_ea_flood_monitoring.uk_ea_flood_monitoring.EAFloodMonitoringAPI.list_stations')
    @patch('uk_ea_flood_monitoring.uk_ea_flood_monitoring.EAFloodMonitoringAPI.get_latest_readings')
    def test_stations_reference_data_delivered(self, mock_readings, mock_stations,
                                                kafka_container, kafka_config):
        """Test that station reference data is delivered to Kafka."""
        topic = 'test-ea-stations-ref'
        self._create_topic(kafka_container, topic)

        mock_stations.return_value = SAMPLE_STATIONS_RESPONSE["items"]
        mock_readings.return_value = []

        from uk_ea_flood_monitoring.uk_ea_flood_monitoring_producer.producer_client import UKGovEnvironmentEAFloodMonitoringEventProducer
        from uk_ea_flood_monitoring.uk_ea_flood_monitoring_producer.uk.gov.environment.ea.floodmonitoring.station import Station
        from confluent_kafka import Producer

        producer = Producer(kafka_config)
        ea_producer = UKGovEnvironmentEAFloodMonitoringEventProducer(producer, topic)

        from uk_ea_flood_monitoring.uk_ea_flood_monitoring import EAFloodMonitoringAPI
        api = EAFloodMonitoringAPI()
        stations = api.list_stations()

        for station in stations:
            station_data = Station(
                station_reference=station.get("stationReference", ""),
                label=station.get("label", ""),
                river_name=station.get("riverName", ""),
                catchment_name=station.get("catchmentName", ""),
                town=station.get("town", ""),
                lat=station.get("lat", 0.0),
                long=station.get("long", 0.0),
                notation=station.get("notation", ""),
                status=station.get("status", ""),
                date_opened=station.get("dateOpened", "")
            )
            ea_producer.send_uk_gov_environment_ea_flood_monitoring_station(
                station_data, flush_producer=False)
        producer.flush()

        from confluent_kafka import Consumer
        consumer_config = {
            'bootstrap.servers': kafka_container.get_bootstrap_server(),
            'group.id': 'test-consumer-group-ea-ref',
            'auto.offset.reset': 'earliest',
            'security.protocol': 'PLAINTEXT',
        }
        consumer = Consumer(consumer_config)
        consumer.subscribe([topic])

        messages = []
        deadline = time.time() + 30
        while len(messages) < 2 and time.time() < deadline:
            msg = consumer.poll(timeout=1.0)
            if msg is not None and not msg.error():
                messages.append(msg)

        consumer.close()

        assert len(messages) == 2

        for msg in messages:
            value = json.loads(msg.value().decode('utf-8'))
            data = value.get('data', value)
            assert 'station_reference' in data
            assert 'label' in data
            assert 'lat' in data
            assert 'long' in data


@pytest.mark.integration
class TestEAFloodMonitoringLiveContainerIntegration:
    """Live API-to-Kafka integration tests using real EA API and real Kafka."""

    @pytest.fixture(scope="class")
    def kafka_container(self):
        """Start a KafkaContainer for the test session."""
        from testcontainers.kafka import KafkaContainer
        container = KafkaContainer()
        container.start()
        yield container
        container.stop()

    @pytest.fixture
    def kafka_config(self, kafka_container):
        bootstrap_servers = kafka_container.get_bootstrap_server()
        return {
            'bootstrap.servers': bootstrap_servers,
            'security.protocol': 'PLAINTEXT',
        }

    def _create_topic(self, kafka_container, topic_name):
        from confluent_kafka.admin import AdminClient, NewTopic
        bootstrap_servers = kafka_container.get_bootstrap_server()
        admin = AdminClient({'bootstrap.servers': bootstrap_servers})
        new_topic = NewTopic(topic_name, num_partitions=1, replication_factor=1)
        futures = admin.create_topics([new_topic])
        for topic, future in futures.items():
            try:
                future.result()
            except Exception:
                pass

    def test_live_stations_to_kafka(self, kafka_container, kafka_config):
        """Test sending real stations from EA API to Kafka."""
        topic = 'test-ea-live-stations'
        self._create_topic(kafka_container, topic)

        from uk_ea_flood_monitoring.uk_ea_flood_monitoring import EAFloodMonitoringAPI
        from uk_ea_flood_monitoring.uk_ea_flood_monitoring_producer.producer_client import UKGovEnvironmentEAFloodMonitoringEventProducer
        from uk_ea_flood_monitoring.uk_ea_flood_monitoring_producer.uk.gov.environment.ea.floodmonitoring.station import Station
        from confluent_kafka import Producer

        api = EAFloodMonitoringAPI()
        producer = Producer(kafka_config)
        ea_producer = UKGovEnvironmentEAFloodMonitoringEventProducer(producer, topic)

        # Fetch real stations (limit to first 10 for test speed)
        import requests
        response = requests.get(
            "https://environment.data.gov.uk/flood-monitoring/id/stations",
            params={"_limit": 10, "parameter": "level"},
            timeout=30
        )
        response.raise_for_status()
        stations = response.json().get("items", [])
        assert len(stations) > 0

        for station in stations:
            station_ref = station.get("stationReference", station.get("notation", ""))
            station_data = Station(
                station_reference=station_ref,
                label=station.get("label", ""),
                river_name=station.get("riverName", ""),
                catchment_name=station.get("catchmentName", ""),
                town=station.get("town", ""),
                lat=station.get("lat", 0.0) if station.get("lat") is not None else 0.0,
                long=station.get("long", 0.0) if station.get("long") is not None else 0.0,
                notation=station.get("notation", ""),
                status=station.get("status", ""),
                date_opened=station.get("dateOpened", "")
            )
            ea_producer.send_uk_gov_environment_ea_flood_monitoring_station(
                station_data, flush_producer=False)
        producer.flush()

        # Consume and verify
        from confluent_kafka import Consumer
        consumer_config = {
            'bootstrap.servers': kafka_container.get_bootstrap_server(),
            'group.id': 'test-consumer-ea-live-stations',
            'auto.offset.reset': 'earliest',
            'security.protocol': 'PLAINTEXT',
        }
        consumer = Consumer(consumer_config)
        consumer.subscribe([topic])

        messages = []
        deadline = time.time() + 30
        while len(messages) < len(stations) and time.time() < deadline:
            msg = consumer.poll(timeout=1.0)
            if msg is not None and not msg.error():
                messages.append(msg)

        consumer.close()

        assert len(messages) == len(stations)

        for msg in messages:
            value = json.loads(msg.value().decode('utf-8'))
            data = value.get('data', value)
            assert 'station_reference' in data
            assert 'label' in data

    def test_live_readings_to_kafka(self, kafka_container, kafka_config):
        """Test sending real readings from EA API to Kafka."""
        topic = 'test-ea-live-readings'
        self._create_topic(kafka_container, topic)

        from uk_ea_flood_monitoring.uk_ea_flood_monitoring_producer.producer_client import UKGovEnvironmentEAFloodMonitoringEventProducer
        from uk_ea_flood_monitoring.uk_ea_flood_monitoring_producer.uk.gov.environment.ea.floodmonitoring.reading import Reading
        from confluent_kafka import Producer

        producer = Producer(kafka_config)
        ea_producer = UKGovEnvironmentEAFloodMonitoringEventProducer(producer, topic)

        # Fetch real latest readings (limited)
        import requests
        response = requests.get(
            "https://environment.data.gov.uk/flood-monitoring/data/readings",
            params={"latest": "", "_limit": 10},
            timeout=30
        )
        response.raise_for_status()
        readings = response.json().get("items", [])
        assert len(readings) > 0

        sent_count = 0
        for item in readings:
            value = item.get("value")
            if value is None or not isinstance(value, (int, float)):
                continue
            measure_uri = item.get("measure", "")
            station_ref = ""
            if "/" in measure_uri:
                parts = measure_uri.split("/")
                for i, part in enumerate(parts):
                    if part == "measures" and i + 1 < len(parts):
                        station_ref = parts[i + 1].split("-")[0]
                        break

            reading_data = Reading(
                station_reference=station_ref,
                date_time=item.get("dateTime", ""),
                measure=measure_uri,
                value=float(value)
            )
            ea_producer.send_uk_gov_environment_ea_flood_monitoring_reading(
                reading_data, flush_producer=False)
            sent_count += 1
        producer.flush()

        assert sent_count > 0

        # Consume and verify
        from confluent_kafka import Consumer
        consumer_config = {
            'bootstrap.servers': kafka_container.get_bootstrap_server(),
            'group.id': 'test-consumer-ea-live-readings',
            'auto.offset.reset': 'earliest',
            'security.protocol': 'PLAINTEXT',
        }
        consumer = Consumer(consumer_config)
        consumer.subscribe([topic])

        messages = []
        deadline = time.time() + 30
        while len(messages) < sent_count and time.time() < deadline:
            msg = consumer.poll(timeout=1.0)
            if msg is not None and not msg.error():
                messages.append(msg)

        consumer.close()

        assert len(messages) == sent_count

        for msg in messages:
            value = json.loads(msg.value().decode('utf-8'))
            data = value.get('data', value)
            assert 'station_reference' in data
            assert 'date_time' in data
            assert 'value' in data
