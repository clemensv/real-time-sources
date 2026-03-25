"""
Container integration tests for NOAA NDBC Buoy Observations poller.
Tests with a real Kafka container using testcontainers.

Run with: pytest tests/test_noaa_ndbc_container.py -v
"""

import pytest
import json
import time
import tempfile
import os
from unittest.mock import patch, Mock


SAMPLE_OBS_TEXT = """\
#STN     LAT      LON  YYYY MM DD hh mm WDIR WSPD  GST  WVHT   DPD   APD MWD   PRES  PTDY  ATMP  WTMP  DEWP  VIS  TIDE
#        deg      deg   yr mo da hr mn  deg  m/s  m/s    m    sec   sec deg    hPa   hPa  degC  degC  degC   nmi    ft
41001  34.700  -72.700 2024 06 15 14 50 210  8.2 10.3   1.5   7.1   5.2 200 1015.2  -1.2  22.3  24.1  18.5   MM   MM
41002  32.300  -75.200 2024 06 15 14 50 180  5.1  6.8   0.8   8.0   4.5 190 1016.0   0.3  23.1  25.5  20.2   MM   MM
"""


@pytest.mark.integration
class TestNDBCContainerIntegration:
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
        return 'test-ndbc-observations'

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

    @patch('noaa_ndbc.noaa_ndbc.requests.get')
    def test_observations_delivered_to_kafka(self, mock_get, kafka_container, kafka_config, kafka_topic, temp_state_file):
        """Test that observations are fetched and delivered to Kafka"""
        # Create the topic
        self._create_topic(kafka_container, kafka_topic)

        # Mock the NDBC API response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.raise_for_status = Mock()
        mock_response.text = SAMPLE_OBS_TEXT
        mock_get.return_value = mock_response

        from noaa_ndbc.noaa_ndbc import NDBCBuoyPoller

        # Create the poller with real Kafka
        poller = NDBCBuoyPoller(
            kafka_config=kafka_config,
            kafka_topic=kafka_topic,
            last_polled_file=temp_state_file
        )

        # Run one poll cycle (not the infinite loop)
        state = poller.load_state()
        last_timestamps = state.get("last_timestamps", {})
        observations = poller.poll_observations()

        new_count = 0
        for obs in observations:
            if obs.station_id in last_timestamps and last_timestamps[obs.station_id] == obs.timestamp:
                continue

            poller.producer.send_microsoft_open_data_us_noaa_ndbc_buoy_observation(
                obs, obs.station_id, flush_producer=False)
            last_timestamps[obs.station_id] = obs.timestamp
            new_count += 1

        poller.producer.producer.flush()

        assert new_count == 2, f"Expected 2 new observations, got {new_count}"

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
            assert 'station_id' in value or 'data' in value or 'type' in value

    @patch('noaa_ndbc.noaa_ndbc.requests.get')
    def test_duplicate_observations_not_resent(self, mock_get, kafka_container, kafka_config, kafka_topic, temp_state_file):
        """Test that duplicate observations are not sent again"""
        self._create_topic(kafka_container, 'test-ndbc-dedup')

        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.raise_for_status = Mock()
        mock_response.text = SAMPLE_OBS_TEXT
        mock_get.return_value = mock_response

        # Pre-populate state with already-seen timestamps
        state_data = {"last_timestamps": {
            "41001": "2024-06-15T14:50:00+00:00",
            "41002": "2024-06-15T14:50:00+00:00"
        }}
        with open(temp_state_file, 'w', encoding='utf-8') as f:
            json.dump(state_data, f)

        from noaa_ndbc.noaa_ndbc import NDBCBuoyPoller

        poller = NDBCBuoyPoller(
            kafka_config=kafka_config,
            kafka_topic='test-ndbc-dedup',
            last_polled_file=temp_state_file
        )

        # Run one poll cycle
        state = poller.load_state()
        last_timestamps = state.get("last_timestamps", {})
        observations = poller.poll_observations()

        new_count = 0
        for obs in observations:
            if obs.station_id in last_timestamps and last_timestamps[obs.station_id] == obs.timestamp:
                continue
            new_count += 1

        assert new_count == 0, f"Expected 0 new observations (all should be duplicates), got {new_count}"

    @patch('noaa_ndbc.noaa_ndbc.requests.get')
    def test_buoy_stations_delivered_to_kafka(self, mock_get, kafka_container, kafka_config, kafka_topic, temp_state_file):
        """Test that buoy station reference data is fetched and delivered to Kafka"""
        topic = 'test-ndbc-stations'
        self._create_topic(kafka_container, topic)

        # Mock the NDBC station table response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.raise_for_status = Mock()
        mock_response.text = """#STATION_ID | OWNER | TTYPE | HULL | NAME | PAYLOAD | LOCATION | TIMEZONE | FORECAST | NOTE
41001 | NDBC | Weather Buoy | NOMAD | CAPE HATTERAS | ARES 9.2 | 34.700 N 72.700 W (34&#176;42'06" N 72&#176;41'54" W) | EST | WFO Morehead City, NC | 
41002 | NDBC | Weather Buoy | NOMAD | SOUTH HATTERAS | ARES 9.2 | 32.300 N 75.200 W (32&#176;18'00" N 75&#176;12'00" W) | EST | WFO Charleston, SC | 
44013 | NDBC | Weather Buoy | DISCUS | BOSTON HARBOR | ARES 9.2 | 42.346 N 70.651 W (42&#176;20'46" N 70&#176;39'04" W) | EST | WFO Boston, MA | 
"""
        mock_get.return_value = mock_response

        from noaa_ndbc.noaa_ndbc import NDBCBuoyPoller

        poller = NDBCBuoyPoller(
            kafka_config=kafka_config,
            kafka_topic=topic,
            last_polled_file=temp_state_file
        )

        # Fetch and send stations (as poll_and_send does at startup)
        stations = poller.fetch_stations()
        assert len(stations) == 3

        for station in stations:
            poller.producer.send_microsoft_open_data_us_noaa_ndbc_buoy_station(
                station, flush_producer=False)
        poller.producer.producer.flush()

        # Consume messages from Kafka and verify
        from confluent_kafka import Consumer
        consumer_config = {
            'bootstrap.servers': kafka_container.get_bootstrap_server(),
            'group.id': 'test-station-consumer',
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

        assert len(messages) == 3, f"Expected 3 station messages in Kafka, got {len(messages)}"

        # Verify message content (CloudEvents structured format nests data under 'data')
        station_ids = set()
        for msg in messages:
            value = json.loads(msg.value().decode('utf-8'))
            data = value.get('data', value)
            assert 'station_id' in data
            station_ids.add(data['station_id'])
        assert station_ids == {'41001', '41002', '44013'}
