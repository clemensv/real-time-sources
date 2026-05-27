"""
Container integration tests for NOAA NWS Weather Alerts poller.
Tests with a real Kafka container using testcontainers.

Run with: pytest tests/test_noaa_nws_container.py -v
"""

import pytest
import json
import time
import tempfile
import os
from unittest.mock import patch, Mock


SAMPLE_NWS_RESPONSE = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "properties": {
                "id": "urn:oid:2.49.0.1.840.0.test-container-1",
                "areaDesc": "Harris County, TX",
                "sent": "2024-06-15T14:00:00-05:00",
                "effective": "2024-06-15T14:00:00-05:00",
                "onset": "2024-06-15T14:00:00-05:00",
                "expires": "2024-06-15T20:00:00-05:00",
                "ends": "2024-06-15T20:00:00-05:00",
                "status": "Actual",
                "messageType": "Alert",
                "category": "Met",
                "severity": "Severe",
                "certainty": "Observed",
                "urgency": "Immediate",
                "event": "Severe Thunderstorm Warning",
                "sender": "w-nws.webmaster@noaa.gov",
                "senderName": "NWS Houston TX",
                "headline": "Severe Thunderstorm Warning issued for Harris County",
                "description": "The National Weather Service in Houston has issued a severe thunderstorm warning.",
                "instruction": "Take shelter immediately.",
                "response": "Shelter"
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": [[[-95.5, 29.7], [-95.3, 29.7], [-95.3, 29.9], [-95.5, 29.9], [-95.5, 29.7]]]
            }
        },
        {
            "type": "Feature",
            "properties": {
                "id": "urn:oid:2.49.0.1.840.0.test-container-2",
                "areaDesc": "Cook County, IL",
                "sent": "2024-06-15T15:00:00-05:00",
                "effective": "2024-06-15T15:00:00-05:00",
                "onset": "2024-06-15T18:00:00-05:00",
                "expires": "2024-06-16T06:00:00-05:00",
                "ends": "2024-06-16T06:00:00-05:00",
                "status": "Actual",
                "messageType": "Alert",
                "category": "Met",
                "severity": "Moderate",
                "certainty": "Likely",
                "urgency": "Expected",
                "event": "Winter Storm Watch",
                "sender": "w-nws.webmaster@noaa.gov",
                "senderName": "NWS Chicago IL",
                "headline": "Winter Storm Watch for Cook County",
                "description": "A winter storm watch has been issued for Cook County.",
                "instruction": "Monitor the latest forecasts.",
                "response": "Prepare"
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": [[[-87.9, 41.6], [-87.5, 41.6], [-87.5, 42.0], [-87.9, 42.0], [-87.9, 41.6]]]
            }
        }
    ]
}


@pytest.mark.integration
class TestNWSContainerIntegration:
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
        return 'test-nws-alerts'

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

    @patch('noaa_nws.noaa_nws.requests.get')
    def test_alerts_delivered_to_kafka(self, mock_get, kafka_container, kafka_config, kafka_topic, temp_state_file):
        """Test that alerts are fetched and delivered to Kafka"""
        # Create the topic
        self._create_topic(kafka_container, kafka_topic)

        # Mock the NWS API response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.raise_for_status = Mock()
        mock_response.json.return_value = SAMPLE_NWS_RESPONSE
        mock_get.return_value = mock_response

        # Import here to avoid import errors if producer not yet generated
        from noaa_nws.noaa_nws import NWSAlertPoller

        # Create the poller with real Kafka
        poller = NWSAlertPoller(
            kafka_config=kafka_config,
            kafka_topic=kafka_topic,
            last_polled_file=temp_state_file
        )

        # Run one poll cycle (not the infinite loop)
        state = poller.load_seen_alerts()
        seen_ids = set(state.get("seen_ids", []))
        features = poller.poll_alerts()

        new_count = 0
        for feature in features:
            props = feature.get("properties", {})
            alert_id = props.get("id", "")
            if not alert_id or alert_id in seen_ids:
                continue

            from noaa_nws.noaa_nws_producer.microsoft.opendata.us.noaa.nws.weatheralert import WeatherAlert
            alert = WeatherAlert(
                alert_id=alert_id,
                area_desc=props.get("areaDesc", ""),
                sent=props.get("sent", ""),
                effective=props.get("effective", ""),
                expires=props.get("expires", ""),
                status=props.get("status", ""),
                message_type=props.get("messageType", ""),
                category=props.get("category", ""),
                severity=props.get("severity", ""),
                certainty=props.get("certainty", ""),
                urgency=props.get("urgency", ""),
                event=props.get("event", ""),
                sender_name=props.get("senderName", ""),
                headline=props.get("headline", ""),
                description=props.get("description", "")
            )

            poller.producer.send_microsoft_open_data_us_noaa_nws_weather_alert(
                alert, alert_id, flush_producer=False)
            seen_ids.add(alert_id)
            new_count += 1

        poller.producer.producer.flush()

        assert new_count == 2, f"Expected 2 new alerts, got {new_count}"

        # Consume messages from Kafka and verify
        from confluent_kafka import Consumer
        consumer_config = {
            'bootstrap.servers': kafka_container.get_bootstrap_server(),
            'group.id': 'test-consumer-group',
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

        # Verify message content
        for msg in messages:
            value = json.loads(msg.value().decode('utf-8'))
            assert 'alert_id' in value or 'data' in value or 'type' in value

    @patch('noaa_nws.noaa_nws.requests.get')
    def test_duplicate_alerts_not_resent(self, mock_get, kafka_container, kafka_config, kafka_topic, temp_state_file):
        """Test that duplicate alerts are not sent again"""
        self._create_topic(kafka_container, 'test-nws-dedup')

        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.raise_for_status = Mock()
        mock_response.json.return_value = SAMPLE_NWS_RESPONSE
        mock_get.return_value = mock_response

        # Pre-populate state with already-seen alert IDs
        state_data = {"seen_ids": [
            "urn:oid:2.49.0.1.840.0.test-container-1",
            "urn:oid:2.49.0.1.840.0.test-container-2"
        ]}
        with open(temp_state_file, 'w', encoding='utf-8') as f:
            json.dump(state_data, f)

        from noaa_nws.noaa_nws import NWSAlertPoller

        poller = NWSAlertPoller(
            kafka_config=kafka_config,
            kafka_topic='test-nws-dedup',
            last_polled_file=temp_state_file
        )

        # Run one poll cycle
        state = poller.load_seen_alerts()
        seen_ids = set(state.get("seen_ids", []))
        features = poller.poll_alerts()

        new_count = 0
        for feature in features:
            props = feature.get("properties", {})
            alert_id = props.get("id", "")
            if not alert_id or alert_id in seen_ids:
                continue
            new_count += 1

        assert new_count == 0, f"Expected 0 new alerts (all duplicates), got {new_count}"

    @patch('noaa_nws.noaa_nws.requests.get')
    def test_zones_delivered_to_kafka(self, mock_get, kafka_container, kafka_config, kafka_topic, temp_state_file):
        """Test that zone reference data is fetched and delivered to Kafka"""
        topic = 'test-nws-zones'
        self._create_topic(kafka_container, topic)

        # Mock the NWS zones API response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.raise_for_status = Mock()
        mock_response.json.return_value = {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "properties": {
                        "id": "TXZ211",
                        "name": "Harris",
                        "type": "forecast",
                        "state": "TX",
                        "forecastOffice": "https://api.weather.gov/offices/HGX",
                        "timeZone": "America/Chicago",
                        "radarStation": "KHGX"
                    }
                },
                {
                    "type": "Feature",
                    "properties": {
                        "id": "ILZ014",
                        "name": "Cook",
                        "type": "forecast",
                        "state": "IL",
                        "forecastOffice": "https://api.weather.gov/offices/LOT",
                        "timeZone": "America/Chicago",
                        "radarStation": "KLOT"
                    }
                },
                {
                    "type": "Feature",
                    "properties": {
                        "id": "CAZ006",
                        "name": "San Francisco",
                        "type": "forecast",
                        "state": "CA",
                        "forecastOffice": "https://api.weather.gov/offices/MTR",
                        "timeZone": "America/Los_Angeles",
                        "radarStation": "KMUX"
                    }
                }
            ]
        }
        mock_get.return_value = mock_response

        from noaa_nws.noaa_nws import NWSAlertPoller

        poller = NWSAlertPoller(
            kafka_config=kafka_config,
            kafka_topic=topic,
            last_polled_file=temp_state_file
        )

        # Fetch and send zones (as poll_and_send does at startup)
        zones = poller.fetch_zones()
        assert len(zones) == 3

        for zone in zones:
            poller.producer.send_microsoft_open_data_us_noaa_nws_zone(
                zone, flush_producer=False)
        poller.producer.producer.flush()

        # Consume messages from Kafka and verify
        from confluent_kafka import Consumer
        consumer_config = {
            'bootstrap.servers': kafka_container.get_bootstrap_server(),
            'group.id': 'test-zone-consumer',
            'auto.offset.reset': 'earliest',
            'security.protocol': 'PLAINTEXT',
        }
        consumer = Consumer(consumer_config)
        consumer.subscribe([topic])

        messages = []
        deadline = time.time() + 30
        while len(messages) < 3 and time.time() < deadline:
            msg = consumer.poll(timeout=1.0)
            if msg is not None and not msg.error():
                messages.append(msg)

        consumer.close()

        assert len(messages) == 3, f"Expected 3 zone messages in Kafka, got {len(messages)}"

        # Verify message content (CloudEvents structured format nests data under 'data')
        zone_ids = set()
        for msg in messages:
            value = json.loads(msg.value().decode('utf-8'))
            data = value.get('data', value)
            assert 'zone_id' in data
            zone_ids.add(data['zone_id'])
        assert zone_ids == {'TXZ211', 'ILZ014', 'CAZ006'}

    def test_live_zones_api_to_kafka(self, kafka_container, kafka_config, kafka_topic, temp_state_file):
        """Test real NWS zones API fetched and delivered to Kafka end-to-end"""
        topic = 'test-nws-live-zones'
        self._create_topic(kafka_container, topic)

        from noaa_nws.noaa_nws import NWSAlertPoller

        poller = NWSAlertPoller(
            kafka_config=kafka_config,
            kafka_topic=topic,
            last_polled_file=temp_state_file
        )

        # Call the real NWS zones API
        zones = poller.fetch_zones()
        assert len(zones) > 0, "Expected at least some zones from the live NWS API"

        # Send a sample (first 5) to Kafka
        sample = zones[:5]
        for zone in sample:
            poller.producer.send_microsoft_open_data_us_noaa_nws_zone(
                zone, flush_producer=False)
        poller.producer.producer.flush()

        # Consume from Kafka and verify
        from confluent_kafka import Consumer
        consumer_config = {
            'bootstrap.servers': kafka_container.get_bootstrap_server(),
            'group.id': 'test-live-zone-consumer',
            'auto.offset.reset': 'earliest',
            'security.protocol': 'PLAINTEXT',
        }
        consumer = Consumer(consumer_config)
        consumer.subscribe([topic])

        messages = []
        deadline = time.time() + 30
        while len(messages) < len(sample) and time.time() < deadline:
            msg = consumer.poll(timeout=1.0)
            if msg is not None and not msg.error():
                messages.append(msg)

        consumer.close()

        assert len(messages) == len(sample), f"Expected {len(sample)} zone messages, got {len(messages)}"

        # Verify each message is a valid CloudEvent with zone data
        for msg in messages:
            value = json.loads(msg.value().decode('utf-8'))
            data = value.get('data', value)
            assert 'zone_id' in data, f"Missing zone_id in message: {value}"
            assert len(data['zone_id']) >= 3, f"Zone id too short: {data['zone_id']}"
            assert 'name' in data, f"Missing name in message: {value}"

    def test_live_alerts_api_to_kafka(self, kafka_container, kafka_config, kafka_topic, temp_state_file):
        """Test real NWS alerts API fetched and delivered to Kafka end-to-end"""
        topic = 'test-nws-live-alerts'
        self._create_topic(kafka_container, topic)

        from noaa_nws.noaa_nws import NWSAlertPoller
        from noaa_nws.noaa_nws_producer.microsoft.opendata.us.noaa.nws.weatheralert import WeatherAlert

        poller = NWSAlertPoller(
            kafka_config=kafka_config,
            kafka_topic=topic,
            last_polled_file=temp_state_file
        )

        # Call the real NWS alerts API
        features = poller.poll_alerts()
        # There may or may not be active alerts right now, so just verify the flow works
        sent_count = 0
        for feature in features[:5]:
            props = feature.get("properties", {})
            alert_id = props.get("id", "")
            if not alert_id:
                continue
            alert = WeatherAlert(
                alert_id=alert_id,
                area_desc=props.get("areaDesc", ""),
                sent=props.get("sent", ""),
                effective=props.get("effective", ""),
                expires=props.get("expires", ""),
                status=props.get("status", ""),
                message_type=props.get("messageType", ""),
                category=props.get("category", ""),
                severity=props.get("severity", ""),
                certainty=props.get("certainty", ""),
                urgency=props.get("urgency", ""),
                event=props.get("event", ""),
                sender_name=props.get("senderName", ""),
                headline=props.get("headline", ""),
                description=props.get("description", "")
            )
            poller.producer.send_microsoft_open_data_us_noaa_nws_weather_alert(
                alert, flush_producer=False)
            sent_count += 1
        poller.producer.producer.flush()

        # Consume and verify what was sent
        if sent_count > 0:
            from confluent_kafka import Consumer
            consumer_config = {
                'bootstrap.servers': kafka_container.get_bootstrap_server(),
                'group.id': 'test-live-alert-consumer',
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

            assert len(messages) == sent_count, f"Expected {sent_count} alert messages, got {len(messages)}"
            for msg in messages:
                value = json.loads(msg.value().decode('utf-8'))
                data = value.get('data', value)
                assert 'alert_id' in data, f"Missing alert_id in message: {value}"
