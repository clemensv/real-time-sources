"""
Container integration tests for NOAA SWPC Space Weather poller.
Tests with a real Kafka container using testcontainers.

Run with: pytest tests/test_noaa_goes_container.py -v
"""

import pytest
import json
import time
import tempfile
import os
from unittest.mock import patch, Mock


SAMPLE_ALERTS_RESPONSE = [
    {
        "product_id": "ALTK04-20240101-001",
        "issue_datetime": "2024 Jan 01 0030 UTC",
        "message": "Space Weather Message Code: ALTK04\nSerial Number: 1234\nIssue Time: 2024 Jan 01 0030 UTC\n\nALERT: Geomagnetic K-index of 4\nThreshold Reached: 2024 Jan 01 0029 UTC"
    },
    {
        "product_id": "WATA50-20240101-002",
        "issue_datetime": "2024 Jan 01 0100 UTC",
        "message": "Space Weather Message Code: WATA50\nSerial Number: 5678\nIssue Time: 2024 Jan 01 0100 UTC\n\nWATCH: Geomagnetic Storm Category G1 Predicted"
    }
]

SAMPLE_K_INDEX_RESPONSE = [
    ["time_tag", "Kp", "a_running", "station_count"],
    ["2024-01-01 00:00:00.000", "2", "5", "8"],
    ["2024-01-01 03:00:00.000", "4", "15", "8"]
]

SAMPLE_SOLAR_WIND_SPEED_RESPONSE = {
    "TimeStamp": "2024-01-01T00:05:00Z",
    "WindSpeed": "425.3"
}

SAMPLE_SOLAR_WIND_MAG_FIELD_RESPONSE = {
    "TimeStamp": "2024-01-01T00:05:00Z",
    "Bt": "5.2",
    "Bz": "-1.3"
}


@pytest.mark.integration
class TestSWPCContainerIntegration:
    """Integration tests using a real Kafka container"""

    @pytest.fixture(scope="class")
    def kafka_container(self):
        """Start a KafkaContainer for the test session"""
        from testcontainers.kafka import KafkaContainer
        container = KafkaContainer()
        container.start()
        yield container
        container.stop()

    @pytest.fixture
    def temp_state_file(self):
        fd, path = tempfile.mkstemp(suffix='.json')
        os.close(fd)
        yield path
        if os.path.exists(path):
            os.unlink(path)

    @pytest.fixture
    def kafka_config(self, kafka_container):
        """Build Kafka config from the running container"""
        bootstrap_servers = kafka_container.get_bootstrap_server()
        return {
            'bootstrap.servers': bootstrap_servers,
            'security.protocol': 'PLAINTEXT',
        }

    @pytest.fixture
    def kafka_topic(self):
        return 'test-swpc-data'

    def _create_topic(self, kafka_container, topic_name):
        """Create a Kafka topic using the container's admin client"""
        from confluent_kafka.admin import AdminClient, NewTopic
        bootstrap_servers = kafka_container.get_bootstrap_server()
        admin = AdminClient({'bootstrap.servers': bootstrap_servers})
        new_topic = NewTopic(topic_name, num_partitions=1, replication_factor=1)
        futures = admin.create_topics([new_topic])
        for topic, future in futures.items():
            try:
                future.result()
            except Exception:
                pass  # topic may already exist

    def _mock_get_side_effect(self, url, **kwargs):
        """Return appropriate mock response based on URL"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.raise_for_status = Mock()

        if "alerts.json" in url:
            mock_response.json.return_value = SAMPLE_ALERTS_RESPONSE
        elif "noaa-planetary-k-index.json" in url:
            mock_response.json.return_value = SAMPLE_K_INDEX_RESPONSE
        elif "solar-wind-speed.json" in url:
            mock_response.json.return_value = SAMPLE_SOLAR_WIND_SPEED_RESPONSE
        elif "solar-wind-mag-field.json" in url:
            mock_response.json.return_value = SAMPLE_SOLAR_WIND_MAG_FIELD_RESPONSE
        else:
            mock_response.json.return_value = {}

        return mock_response

    @patch('noaa_goes.noaa_goes.requests.get')
    def test_alerts_delivered_to_kafka(self, mock_get, kafka_container, kafka_config, kafka_topic, temp_state_file):
        """Test that space weather alerts are fetched and delivered to Kafka"""
        self._create_topic(kafka_container, kafka_topic)

        mock_get.side_effect = self._mock_get_side_effect

        from noaa_goes.noaa_goes import SWPCPoller
        from noaa_goes.noaa_goes_producer.microsoft.opendata.us.noaa.swpc.spaceweatheralert import SpaceWeatherAlert

        poller = SWPCPoller(
            kafka_config=kafka_config,
            kafka_topic=kafka_topic,
            last_polled_file=temp_state_file
        )

        # Run one poll cycle manually for alerts
        alerts = poller.poll_alerts()
        assert len(alerts) == 2

        new_count = 0
        for alert_data in alerts:
            product_id = alert_data.get("product_id", "")
            alert = SpaceWeatherAlert(
                product_id=product_id,
                issue_datetime=alert_data.get("issue_datetime", ""),
                message=alert_data.get("message", "")
            )
            poller.producer.send_microsoft_open_data_us_noaa_swpc_space_weather_alert(
                alert, product_id, flush_producer=False)
            new_count += 1

        poller.producer.producer.flush()
        assert new_count == 2

        # Consume messages from Kafka
        from confluent_kafka import Consumer
        consumer_config = {
            'bootstrap.servers': kafka_container.get_bootstrap_server(),
            'group.id': 'test-consumer-alerts',
            'auto.offset.reset': 'earliest',
            'security.protocol': 'PLAINTEXT',
        }
        consumer = Consumer(consumer_config)
        consumer.subscribe([kafka_topic])

        messages = []
        deadline = time.time() + 30
        while len(messages) < 2 and time.time() < deadline:
            msg = consumer.poll(timeout=1.0)
            if msg is not None and not msg.error():
                messages.append(msg)

        consumer.close()

        assert len(messages) == 2, f"Expected 2 messages in Kafka, got {len(messages)}"

        for msg in messages:
            value = json.loads(msg.value().decode('utf-8'))
            assert 'product_id' in value or 'data' in value or 'type' in value

    @patch('noaa_goes.noaa_goes.requests.get')
    def test_k_index_delivered_to_kafka(self, mock_get, kafka_container, kafka_config, temp_state_file):
        """Test that K-index data is fetched and delivered to Kafka"""
        topic = 'test-swpc-kindex'
        self._create_topic(kafka_container, topic)

        mock_get.side_effect = self._mock_get_side_effect

        from noaa_goes.noaa_goes import SWPCPoller
        from noaa_goes.noaa_goes_producer.microsoft.opendata.us.noaa.swpc.planetarykindex import PlanetaryKIndex

        poller = SWPCPoller(
            kafka_config=kafka_config,
            kafka_topic=topic,
            last_polled_file=temp_state_file
        )

        rows = poller.poll_k_index()
        assert len(rows) == 2

        for row in rows:
            kindex = PlanetaryKIndex(
                time_tag=str(row[0]),
                kp=float(row[1]),
                a_running=float(row[2]),
                station_count=float(row[3])
            )
            poller.producer.send_microsoft_open_data_us_noaa_swpc_planetary_kindex(
                kindex, str(row[0]), flush_producer=False)

        poller.producer.producer.flush()

        from confluent_kafka import Consumer
        consumer_config = {
            'bootstrap.servers': kafka_container.get_bootstrap_server(),
            'group.id': 'test-consumer-kindex',
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
        assert len(messages) == 2, f"Expected 2 K-index messages, got {len(messages)}"

    @patch('noaa_goes.noaa_goes.requests.get')
    def test_solar_wind_delivered_to_kafka(self, mock_get, kafka_container, kafka_config, temp_state_file):
        """Test that solar wind data is fetched and delivered to Kafka"""
        topic = 'test-swpc-solarwind'
        self._create_topic(kafka_container, topic)

        mock_get.side_effect = self._mock_get_side_effect

        from noaa_goes.noaa_goes import SWPCPoller
        from noaa_goes.noaa_goes_producer.microsoft.opendata.us.noaa.swpc.solarwindsummary import SolarWindSummary

        poller = SWPCPoller(
            kafka_config=kafka_config,
            kafka_topic=topic,
            last_polled_file=temp_state_file
        )

        records = poller.poll_solar_wind()
        assert len(records) == 1

        record = records[0]
        summary = SolarWindSummary(
            timestamp=record["timestamp"],
            wind_speed=record["wind_speed"],
            bt=record["bt"],
            bz=record["bz"]
        )
        poller.producer.send_microsoft_open_data_us_noaa_swpc_solar_wind_summary(
            summary, record["timestamp"], flush_producer=True)

        from confluent_kafka import Consumer
        consumer_config = {
            'bootstrap.servers': kafka_container.get_bootstrap_server(),
            'group.id': 'test-consumer-solarwind',
            'auto.offset.reset': 'earliest',
            'security.protocol': 'PLAINTEXT',
        }
        consumer = Consumer(consumer_config)
        consumer.subscribe([topic])

        messages = []
        deadline = time.time() + 30
        while len(messages) < 1 and time.time() < deadline:
            msg = consumer.poll(timeout=1.0)
            if msg is not None and not msg.error():
                messages.append(msg)

        consumer.close()
        assert len(messages) == 1, f"Expected 1 solar wind message, got {len(messages)}"
