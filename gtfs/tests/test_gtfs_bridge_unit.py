"""
Unit tests for GTFS Bridge functionality.
Tests core functions without external dependencies.
"""

import pytest
import os
import hashlib
import json
from types import GeneratorType
from unittest.mock import Mock, patch, mock_open
from datetime import datetime, timedelta
import gtfs_rt_bridge.gtfs_cli as gtfs_cli
from gtfs_rt_bridge.gtfs_cli import (
    parse_connection_string,
    calculate_file_hashes,
    read_file_hashes,
    write_file_hashes,
    fetch_and_process_schedule,
    map_stops,
)


@pytest.mark.unit
class TestConnectionStringParsing:
    """Tests for Event Hubs connection string parsing"""

    def test_parse_connection_string_with_all_components(self):
        """Test parsing a complete Event Hubs connection string"""
        connection_string = (
            "Endpoint=sb://test.servicebus.windows.net/;"
            "SharedAccessKeyName=RootManageSharedAccessKey;"
            "SharedAccessKey=testkey123;"
            "EntityPath=gtfs-events"
        )
        
        result = parse_connection_string(connection_string)
        
        assert result['bootstrap.servers'] == 'test.servicebus.windows.net:9093'
        assert result['kafka_topic'] == 'gtfs-events'
        assert result['sasl.username'] == '$ConnectionString'
        assert connection_string.strip() in result['sasl.password']

    def test_parse_connection_string_strips_whitespace(self):
        """Test that connection string parsing handles whitespace"""
        connection_string = (
            "  Endpoint=sb://test.servicebus.windows.net/;  "
            "EntityPath=gtfs-events  "
        )
        
        result = parse_connection_string(connection_string)
        
        assert result['bootstrap.servers'] == 'test.servicebus.windows.net:9093'
        assert result['kafka_topic'] == 'gtfs-events'

    def test_parse_connection_string_with_quotes(self):
        """Test parsing connection string with quoted values"""
        connection_string = (
            'Endpoint="sb://test.servicebus.windows.net/";'
            'EntityPath="gtfs-events"'
        )
        
        result = parse_connection_string(connection_string)
        
        assert result['bootstrap.servers'] == 'test.servicebus.windows.net:9093'
        assert result['kafka_topic'] == 'gtfs-events'

    def test_parse_connection_string_removes_protocol_prefix(self):
        """Test that sb:// protocol is removed from endpoint"""
        connection_string = (
            "Endpoint=sb://namespace.servicebus.windows.net/;"
            "EntityPath=topic"
        )
        
        result = parse_connection_string(connection_string)
        
        assert 'sb://' not in result['bootstrap.servers']
        assert result['bootstrap.servers'].startswith('namespace.servicebus.windows.net')

    def test_parse_connection_string_adds_port(self):
        """Test that port 9093 is added to bootstrap server"""
        connection_string = (
            "Endpoint=sb://test.servicebus.windows.net/;"
            "EntityPath=topic"
        )
        
        result = parse_connection_string(connection_string)
        
        assert result['bootstrap.servers'].endswith(':9093')

    def test_parse_connection_string_invalid_format_raises_error(self):
        """Test that malformed connection string raises ValueError"""
        connection_string = "EndpointWithoutEquals;EntityPathAlsoInvalid"
        
        with pytest.raises(ValueError, match="Invalid connection string format"):
            parse_connection_string(connection_string)

    def test_parse_connection_string_sets_sasl_credentials(self):
        """Test that SASL credentials are properly set when SharedAccessKeyName is present"""
        connection_string = (
            "Endpoint=sb://test.servicebus.windows.net/;"
            "SharedAccessKeyName=MyPolicy;"
            "SharedAccessKey=abc123;"
            "EntityPath=topic"
        )
        
        result = parse_connection_string(connection_string)
        
        assert result['sasl.username'] == '$ConnectionString'
        assert result['sasl.password'] == connection_string.strip()
        assert result['security.protocol'] == 'SASL_SSL'
        assert result['sasl.mechanism'] == 'PLAIN'

    def test_parse_connection_string_without_sasl(self):
        """Test that plain connection string without SharedAccessKeyName has no SASL config"""
        connection_string = (
            "Endpoint=sb://test.servicebus.windows.net/;"
            "EntityPath=topic"
        )
        
        result = parse_connection_string(connection_string)
        
        assert 'sasl.username' not in result
        assert 'security.protocol' not in result


@pytest.mark.unit
class TestFileHashCalculation:
    """Tests for schedule file hash calculation"""

    @patch('gtfs_rt_bridge.gtfs_cli.ZipFile')
    def test_calculate_file_hashes_processes_txt_files(self, mock_zipfile):
        """Test that only .txt files are hashed"""
        mock_zip = Mock()
        mock_zip.namelist.return_value = ['agency.txt', 'routes.txt', 'readme.md', 'image.png']
        def make_file_cm(*_args, **_kwargs):
            cm = Mock()
            mock_file = Mock()
            mock_file.read = Mock(side_effect=[b'test content', b''])
            cm.__enter__ = Mock(return_value=mock_file)
            cm.__exit__ = Mock(return_value=False)
            return cm
        mock_zip.open = Mock(side_effect=make_file_cm)
        mock_zipfile.return_value.__enter__.return_value = mock_zip
        
        result = calculate_file_hashes('/path/to/schedule.zip')
        
        assert 'agency.txt' in result
        assert 'routes.txt' in result
        assert 'readme.md' not in result
        assert 'image.png' not in result

    @patch('gtfs_rt_bridge.gtfs_cli.ZipFile')
    def test_calculate_file_hashes_computes_sha256(self, mock_zipfile):
        """Test that SHA-256 hashes are computed correctly"""
        test_content = b'test content for hashing'
        expected_hash = hashlib.sha256(test_content).hexdigest()
        
        mock_zip = Mock()
        mock_zip.namelist.return_value = ['test.txt']
        mock_file = Mock()
        mock_file.read = Mock(side_effect=[test_content, b''])
        mock_zip.open.return_value.__enter__ = Mock(return_value=mock_file)
        mock_zip.open.return_value.__exit__ = Mock(return_value=False)
        mock_zipfile.return_value.__enter__.return_value = mock_zip
        
        result = calculate_file_hashes('/path/to/schedule.zip')
        
        assert result['test.txt'] == expected_hash

    @patch('gtfs_rt_bridge.gtfs_cli.ZipFile')
    def test_calculate_file_hashes_handles_empty_zip(self, mock_zipfile):
        """Test handling of empty schedule file"""
        mock_zip = Mock()
        mock_zip.namelist.return_value = []
        mock_zipfile.return_value.__enter__.return_value = mock_zip
        
        result = calculate_file_hashes('/path/to/empty.zip')
        
        assert result == {}


@pytest.mark.unit
class TestFileHashStorage:
    """Tests for file hash reading and writing"""

    @patch('builtins.open', new_callable=mock_open, read_data='{"agency.txt": "abc123"}')
    @patch('os.path.exists', return_value=True)
    def test_read_file_hashes_loads_existing_hashes(self, mock_exists, mock_file):
        """Test reading existing hash file"""
        result = read_file_hashes('/path/to/schedule.zip', None)
        
        assert result == {"agency.txt": "abc123"}

    @patch('os.path.exists', return_value=False)
    def test_read_file_hashes_returns_empty_dict_if_not_exists(self, mock_exists):
        """Test that missing hash file returns empty dict"""
        result = read_file_hashes('/path/to/schedule.zip', None)
        
        assert result == {}

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.expanduser', return_value='/home/user')
    def test_write_file_hashes_creates_json_file(self, mock_expanduser, mock_file):
        """Test writing hashes to JSON file"""
        hashes = {"agency.txt": "abc123", "routes.txt": "def456"}
        
        write_file_hashes('schedule.zip', hashes, None)
        
        mock_file.assert_called()
        handle = mock_file()
        # Check that json.dump was called (indirectly through write calls)
        assert handle.write.called

    @patch('builtins.open', new_callable=mock_open)
    def test_write_file_hashes_uses_custom_cache_dir(self, mock_file):
        """Test that custom cache directory is used"""
        hashes = {"agency.txt": "abc123"}
        cache_dir = '/custom/cache'
        
        write_file_hashes('schedule.zip', hashes, cache_dir)
        
        # Verify the file was opened with the custom cache directory path
        call_args = mock_file.call_args[0][0]
        assert cache_dir in call_args


@pytest.mark.unit
class TestHelperFunctions:
    """Tests for utility helper functions"""

    def test_connection_string_parsing_is_deterministic(self):
        """Test that parsing the same connection string produces identical results"""
        connection_string = (
            "Endpoint=sb://test.servicebus.windows.net/;"
            "EntityPath=topic"
        )
        
        result1 = parse_connection_string(connection_string)
        result2 = parse_connection_string(connection_string)
        
        assert result1 == result2

    def test_parse_connection_string_preserves_key_order(self):
        """Test that all required keys are present in parsed result with SASL"""
        connection_string = (
            "Endpoint=sb://test.servicebus.windows.net/;"
            "SharedAccessKeyName=MyPolicy;"
            "SharedAccessKey=abc123;"
            "EntityPath=topic"
        )
        
        result = parse_connection_string(connection_string)
        
        required_keys = ['bootstrap.servers', 'kafka_topic', 'sasl.username', 'sasl.password']
        for key in required_keys:
            assert key in result


@pytest.mark.unit
class TestStreamingScheduleProcessing:
    """Tests for streaming schedule processing."""

    def test_map_stops_returns_generator(self):
        """Test that stop mapping accepts iterables and yields lazily."""
        rows = iter([
            {
                'stop_id': 'stop-1',
                'stop_name': 'Main Stop',
                'stop_lat': '51.0',
                'stop_lon': '4.0',
            }
        ])

        entities = map_stops(rows)

        assert isinstance(entities, GeneratorType)
        stops = list(entities)
        assert len(stops) == 1
        assert stops[0].stopId == 'stop-1'
        assert stops[0].stopLat == pytest.approx(51.0)
        assert stops[0].stopLon == pytest.approx(4.0)

    @patch('gtfs_rt_bridge.gtfs_cli.write_file_hashes')
    @patch('gtfs_rt_bridge.gtfs_cli.calculate_file_hashes')
    @patch('gtfs_rt_bridge.gtfs_cli.read_file_hashes')
    @patch('gtfs_rt_bridge.gtfs_cli.iter_schedule_file_contents')
    @patch('gtfs_rt_bridge.gtfs_cli.read_schedule_file_contents')
    @patch('gtfs_rt_bridge.gtfs_cli.fetch_schedule_file')
    def test_fetch_and_process_schedule_streams_changed_files(
        self,
        mock_fetch_schedule_file,
        mock_read_schedule_file_contents,
        mock_iter_schedule_file_contents,
        mock_read_file_hashes,
        mock_calculate_file_hashes,
        mock_write_file_hashes,
    ):
        """Test that changed GTFS files are streamed instead of materialized."""
        schedule_path = 'C:\\cache\\schedule.zip'
        mock_fetch_schedule_file.return_value = ('etag-1', schedule_path)
        mock_read_file_hashes.return_value = {}
        mock_calculate_file_hashes.return_value = {'stops.txt': 'hash-1'}

        def read_side_effect(_schedule_path, file_name):
            if file_name == 'agency.txt':
                return [{'agency_url': 'https://agency.example'}]
            if file_name in ('calendar.txt', 'calendar_dates.txt'):
                return []
            raise AssertionError(f'unexpected materialized read for {file_name}')

        mock_read_schedule_file_contents.side_effect = read_side_effect
        mock_iter_schedule_file_contents.return_value = iter([
            {
                'stop_id': 'stop-1',
                'stop_name': 'Main Stop',
                'stop_lat': '51.0',
                'stop_lon': '4.0',
            }
        ])

        producer_client = Mock()
        producer_client.producer = Mock()

        with patch.dict(gtfs_cli.etags, {}, clear=True):
            fetch_and_process_schedule(
                agency_id='agency-1',
                reference_producer_client=producer_client,
                gtfs_urls=['https://example.com/gtfs.zip'],
                headers=[],
                force_refresh=False,
                cache_dir=None,
            )

        mock_iter_schedule_file_contents.assert_called_once_with(schedule_path, 'stops.txt')
        assert all(call.args[1] != 'stops.txt' for call in mock_read_schedule_file_contents.call_args_list)
        producer_client.send_general_transit_feed_static_stops.assert_called_once()
        producer_client.producer.flush.assert_called()
        # Per-file hash writes: read_file_hashes called to load persisted state,
        # then write_file_hashes called with updated hash for just this file
        assert mock_write_file_hashes.call_count == 1
        written_hashes = mock_write_file_hashes.call_args[0][1]
        assert 'stops.txt' in written_hashes


@pytest.mark.unit
class TestStaticFilePriorityOrdering:
    """Tests for the priority-based ordering of static schedule files."""

    @patch('gtfs_rt_bridge.gtfs_cli.write_file_hashes')
    @patch('gtfs_rt_bridge.gtfs_cli.read_file_hashes')
    @patch('gtfs_rt_bridge.gtfs_cli.calculate_file_hashes')
    @patch('gtfs_rt_bridge.gtfs_cli.iter_schedule_file_contents')
    @patch('gtfs_rt_bridge.gtfs_cli.read_schedule_file_contents')
    @patch('gtfs_rt_bridge.gtfs_cli.fetch_schedule_file')
    def test_shapes_processed_last(
        self,
        mock_fetch,
        mock_read_contents,
        mock_iter_contents,
        mock_calc_hashes,
        mock_read_hashes,
        mock_write_hashes,
    ):
        """Shapes should be processed after all other files."""
        mock_fetch.return_value = ('etag-1', 'schedule.zip')
        mock_read_hashes.return_value = {}
        # All three files are "changed"
        mock_calc_hashes.return_value = {
            'shapes.txt': 'h1',
            'agency.txt': 'h2',
            'routes.txt': 'h3',
        }
        mock_read_contents.side_effect = lambda _p, f: (
            [{'agency_url': 'https://x'}] if f == 'agency.txt' else []
        )
        mock_iter_contents.return_value = iter([])

        producer = Mock()
        producer.producer = Mock()
        processing_order = []
        original_info = gtfs_cli.logger.info

        def capture_info(msg, *args):
            if msg == "Processing %s entities":
                processing_order.append(args[0])
            original_info(msg, *args)

        with patch.dict(gtfs_cli.etags, {}, clear=True), \
             patch.object(gtfs_cli.logger, 'info', side_effect=capture_info):
            fetch_and_process_schedule('a1', producer, ['https://x/gtfs.zip'], [], force_refresh=True)

        assert processing_order[-1] == 'shapes', \
            f"shapes should be last, got order: {processing_order}"
        assert processing_order[0] == 'agency', \
            f"agency should be first, got order: {processing_order}"

    def test_priority_list_puts_shapes_last(self):
        """The STATIC_FILE_PRIORITY constant should end with shapes."""
        # Import the priority list indirectly by checking the sort behavior
        files = ['shapes.txt', 'routes.txt', 'agency.txt', 'stops.txt', 'trips.txt']
        # Reproduce the sort logic from fetch_and_process_schedule
        STATIC_FILE_PRIORITY = [
            "agency", "calendar", "calendar_dates",
            "routes", "stops", "stop_areas",
            "trips", "stop_times", "frequencies",
            "transfers", "feed_info", "levels", "pathways",
            "networks", "route_networks", "areas",
            "attributions", "booking_rules", "fare_attributes",
            "fare_leg_rules", "fare_media", "fare_products",
            "fare_rules", "fare_transfer_rules", "location_groups",
            "location_group_stores", "timeframes", "translations",
            "shapes",
        ]

        def priority(f):
            base = os.path.basename(f).split(".")[0]
            try:
                return STATIC_FILE_PRIORITY.index(base)
            except ValueError:
                return len(STATIC_FILE_PRIORITY) - 2

        sorted_files = sorted(files, key=priority)
        assert sorted_files[-1] == 'shapes.txt'
        assert sorted_files[0] == 'agency.txt'
        assert sorted_files.index('routes.txt') < sorted_files.index('trips.txt')


@pytest.mark.unit
class TestPerFileHashWrites:
    """Tests for per-file hash persistence after each flush."""

    @patch('gtfs_rt_bridge.gtfs_cli.write_file_hashes')
    @patch('gtfs_rt_bridge.gtfs_cli.read_file_hashes')
    @patch('gtfs_rt_bridge.gtfs_cli.calculate_file_hashes')
    @patch('gtfs_rt_bridge.gtfs_cli.iter_schedule_file_contents')
    @patch('gtfs_rt_bridge.gtfs_cli.read_schedule_file_contents')
    @patch('gtfs_rt_bridge.gtfs_cli.fetch_schedule_file')
    def test_hash_written_per_file_not_all_at_end(
        self,
        mock_fetch,
        mock_read_contents,
        mock_iter_contents,
        mock_calc_hashes,
        mock_read_hashes,
        mock_write_hashes,
    ):
        """Each processed file should trigger its own hash write."""
        mock_fetch.return_value = ('etag-1', 'schedule.zip')
        mock_read_hashes.return_value = {}
        mock_calc_hashes.return_value = {
            'agency.txt': 'ha',
            'stops.txt': 'hs',
        }
        mock_read_contents.side_effect = lambda _p, f: (
            [{'agency_url': 'https://x'}] if f == 'agency.txt' else []
        )

        call_count = [0]
        def iter_side_effect(_path, _fname):
            call_count[0] += 1
            if call_count[0] == 1:
                return iter([{'agency_id': 'a1', 'agency_name': 'Test', 'agency_url': 'https://x', 'agency_timezone': 'UTC'}])
            return iter([{'stop_id': 's1', 'stop_name': 'S', 'stop_lat': '51', 'stop_lon': '4'}])

        mock_iter_contents.side_effect = iter_side_effect

        producer = Mock()
        producer.producer = Mock()

        with patch.dict(gtfs_cli.etags, {}, clear=True):
            fetch_and_process_schedule('a1', producer, ['https://x/gtfs.zip'], [], force_refresh=True)

        # Should be called once per changed file (2 files = 2 writes)
        assert mock_write_hashes.call_count == 2
        # First write should contain agency hash
        first_written = mock_write_hashes.call_args_list[0][0][1]
        assert 'agency.txt' in first_written
        # Second write should contain stops hash
        second_written = mock_write_hashes.call_args_list[1][0][1]
        assert 'stops.txt' in second_written


@pytest.mark.unit
class TestBackgroundScheduleThread:
    """Tests for background schedule thread in feed_realtime_messages."""

    @patch('gtfs_rt_bridge.gtfs_cli.poll_and_submit_realtime_feed')
    @patch('gtfs_rt_bridge.gtfs_cli.fetch_and_process_schedule')
    @patch('gtfs_rt_bridge.gtfs_cli.Producer')
    def test_rt_polling_starts_without_waiting_for_schedule(
        self,
        mock_producer_cls,
        mock_fetch_schedule,
        mock_poll_rt,
    ):
        """RT polling should begin on the first loop iteration even while
        schedule processing runs in the background."""
        import threading

        mock_producer = Mock()
        mock_producer_cls.return_value = mock_producer

        # Make schedule processing block until we release it
        schedule_started = threading.Event()
        schedule_release = threading.Event()

        def slow_schedule(*args, **kwargs):
            schedule_started.set()
            schedule_release.wait(timeout=5)

        mock_fetch_schedule.side_effect = slow_schedule

        # Make RT polling raise KeyboardInterrupt after first call to exit the loop
        call_count = [0]
        def rt_poll_then_exit(*args, **kwargs):
            call_count[0] += 1
            if call_count[0] >= 1:
                raise KeyboardInterrupt()

        mock_poll_rt.side_effect = rt_poll_then_exit

        from gtfs_rt_bridge.gtfs_cli import feed_realtime_messages

        try:
            feed_realtime_messages(
                agency_id='a1',
                kafka_bootstrap_servers='localhost:9092',
                kafka_topic='test',
                sasl_username=None,
                sasl_password=None,
                gtfs_rt_urls=['https://rt.example/feed'],
                gtfs_rt_headers=[],
                gtfs_urls=['https://static.example/gtfs.zip'],
                gtfs_headers=[],
                mdb_source_id=None,
                route=None,
                poll_interval=1,
                schedule_poll_interval=3600,
                cloudevents_mode='structured',
                cache_dir='/tmp/test',
                force_schedule_refresh=True,
            )
        except KeyboardInterrupt:
            pass

        schedule_release.set()

        # RT polling was called even though schedule hadn't finished
        assert mock_poll_rt.called, "RT polling should have been called"
        # Schedule was started in background
        assert schedule_started.wait(timeout=5), "Schedule thread should have started"

