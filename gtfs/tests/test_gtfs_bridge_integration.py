"""
Integration tests for GTFS Bridge with mocked external services.
Tests interactions with GTFS-RT feeds and schedule APIs.
"""

import pytest
import requests
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime, timedelta
from gtfs_rt_bridge.gtfs_cli import (
    fetch_schedule_file,
    read_schedule_file_contents,
)


@pytest.mark.integration
class TestScheduleFileFetching:
    """Tests for GTFS schedule file fetching with mocked HTTP"""

    @pytest.fixture
    def mock_response(self):
        """Create a mock HTTP response"""
        response = Mock()
        response.status_code = 200
        response.content = b'mock zip file content'
        response.headers = {'ETag': '"new-etag-123"'}
        return response

    def test_fetch_schedule_file_success(self, mock_response, tmp_path):
        """Test successful schedule file fetch"""
        with patch('gtfs_rt_bridge.gtfs_cli.requests.get', return_value=mock_response):
            gtfs_url = 'https://example.com/gtfs.zip'
            
            etag, file_path = fetch_schedule_file(gtfs_url, None, [], None, str(tmp_path))
            
            assert etag == '"new-etag-123"'
            assert file_path.endswith('.json')
            assert str(tmp_path) in file_path

    def test_fetch_schedule_file_with_etag_not_modified(self, tmp_path):
        """Test that 304 Not Modified returns existing file"""
        # Create an existing file first
        import hashlib
        gtfs_url = 'https://example.com/gtfs.zip'
        url_hash = hashlib.sha256(gtfs_url.encode()).hexdigest()
        file_path = tmp_path / f"{url_hash}.json"
        file_path.write_bytes(b'existing content')
        # Touch file to make it recent (within 24 hours)
        file_path.touch()
        
        # Since file is recent, it should return None for etag (no fetch)
        with patch('gtfs_rt_bridge.gtfs_cli.requests.get') as mock_get:
            etag, returned_path = fetch_schedule_file(gtfs_url, None, [], '"old-etag"', str(tmp_path))
            
            # Should not make HTTP request due to recent cache
            mock_get.assert_not_called()
            assert etag is None
            assert returned_path == str(file_path)

    def test_fetch_schedule_file_uses_cache_if_recent(self, tmp_path):
        """Test that recent cached files are reused"""
        import hashlib
        gtfs_url = 'https://example.com/gtfs.zip'
        url_hash = hashlib.sha256(gtfs_url.encode()).hexdigest()
        file_path = tmp_path / f"{url_hash}.json"
        file_path.write_bytes(b'cached content')
        # Touch the file to set recent modification time
        file_path.touch()
        
        with patch('gtfs_rt_bridge.gtfs_cli.requests.get') as mock_get:
            etag, returned_path = fetch_schedule_file(gtfs_url, None, [], None, str(tmp_path))
            
            # Should not make HTTP request
            mock_get.assert_not_called()
            assert returned_path == str(file_path)

    def test_fetch_schedule_file_with_custom_headers(self, mock_response, tmp_path):
        """Test that custom headers are passed to request"""
        with patch('gtfs_rt_bridge.gtfs_cli.requests.get', return_value=mock_response) as mock_get:
            gtfs_url = 'https://example.com/gtfs.zip'
            custom_headers = [['Authorization', 'Bearer token123'], ['X-Custom', 'value']]
            
            fetch_schedule_file(gtfs_url, None, custom_headers, None, str(tmp_path))
            
            call_args = mock_get.call_args
            headers = call_args[1]['headers']
            assert 'Authorization' in headers
            assert headers['Authorization'] == 'Bearer token123'
            assert headers['X-Custom'] == 'value'
            assert headers['User-Agent'] == 'gtfs-rt-cli/0.1'

    def test_fetch_schedule_file_timeout_raises_error(self, tmp_path):
        """Test that request timeout is handled"""
        with patch('gtfs_rt_bridge.gtfs_cli.requests.get', side_effect=requests.exceptions.Timeout):
            gtfs_url = 'https://example.com/gtfs.zip'
            
            with pytest.raises(requests.exceptions.Timeout):
                fetch_schedule_file(gtfs_url, None, [], None, str(tmp_path))

    def test_fetch_schedule_file_http_error_raises(self, tmp_path):
        """Test that HTTP errors are raised"""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("404 Not Found")
        
        with patch('gtfs_rt_bridge.gtfs_cli.requests.get', return_value=mock_response):
            gtfs_url = 'https://example.com/gtfs.zip'
            
            with pytest.raises(requests.exceptions.HTTPError):
                fetch_schedule_file(gtfs_url, None, [], None, str(tmp_path))

    def test_fetch_schedule_file_creates_cache_directory(self, tmp_path):
        """Test that cache directory is created if it doesn't exist"""
        cache_dir = tmp_path / "new_cache_dir"
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = b'content'
        mock_response.headers = {'ETag': '"etag"'}
        
        with patch('gtfs_rt_bridge.gtfs_cli.requests.get', return_value=mock_response):
            gtfs_url = 'https://example.com/gtfs.zip'
            
            fetch_schedule_file(gtfs_url, None, [], None, str(cache_dir))
            
            assert cache_dir.exists()


@pytest.mark.integration
class TestScheduleFileReading:
    """Tests for reading GTFS schedule file contents"""

    @pytest.fixture
    def mock_zip_file(self, tmp_path):
        """Create a mock GTFS zip file with CSV data"""
        import zipfile
        import csv
        
        zip_path = tmp_path / "test_gtfs.zip"
        
        with zipfile.ZipFile(zip_path, 'w') as zf:
            # Create agency.txt
            agency_csv = "agency_id,agency_name,agency_url,agency_timezone\n"
            agency_csv += "1,Test Transit,https://example.com,America/New_York\n"
            zf.writestr('agency.txt', agency_csv)
            
            # Create routes.txt
            routes_csv = "route_id,agency_id,route_short_name,route_long_name,route_type\n"
            routes_csv += "A,1,1,Main Line,3\n"
            routes_csv += "B,1,2,Express,3\n"
            zf.writestr('routes.txt', routes_csv)
        
        return str(zip_path)

    def test_read_schedule_file_contents_parses_csv(self, mock_zip_file):
        """Test reading and parsing CSV file from schedule"""
        result = read_schedule_file_contents(mock_zip_file, 'agency.txt')
        
        assert len(result) == 1
        assert result[0]['agency_id'] == '1'
        assert result[0]['agency_name'] == 'Test Transit'
        assert result[0]['agency_timezone'] == 'America/New_York'

    def test_read_schedule_file_contents_multiple_rows(self, mock_zip_file):
        """Test reading multiple rows from CSV"""
        result = read_schedule_file_contents(mock_zip_file, 'routes.txt')
        
        assert len(result) == 2
        assert result[0]['route_short_name'] == '1'
        assert result[1]['route_short_name'] == '2'

    def test_read_schedule_file_contents_nonexistent_file(self, mock_zip_file):
        """Test reading non-existent file returns empty list"""
        result = read_schedule_file_contents(mock_zip_file, 'nonexistent.txt')
        
        assert result == []

    def test_read_schedule_file_contents_preserves_all_columns(self, mock_zip_file):
        """Test that all CSV columns are preserved"""
        result = read_schedule_file_contents(mock_zip_file, 'routes.txt')
        
        expected_columns = ['route_id', 'agency_id', 'route_short_name', 'route_long_name', 'route_type']
        assert all(col in result[0] for col in expected_columns)


@pytest.mark.integration
class TestGTFSRealtimeFeedParsing:
    """Tests for GTFS-RT feed parsing with mocked protocol buffer data"""

    @pytest.fixture
    def mock_gtfs_rt_response(self):
        """Create a mock GTFS-RT protocol buffer response"""
        from google.transit import gtfs_realtime_pb2
        
        feed = gtfs_realtime_pb2.FeedMessage()
        feed.header.gtfs_realtime_version = "2.0"
        feed.header.incrementality = gtfs_realtime_pb2.FeedHeader.FULL_DATASET
        feed.header.timestamp = int(datetime.now().timestamp())
        
        # Add a vehicle position
        entity = feed.entity.add()
        entity.id = "vehicle_1"
        entity.vehicle.vehicle.id = "1001"
        entity.vehicle.position.latitude = 40.7128
        entity.vehicle.position.longitude = -74.0060
        entity.vehicle.timestamp = int(datetime.now().timestamp())
        
        return feed.SerializeToString()

    def test_gtfs_rt_feed_parsing_vehicle_position(self, mock_gtfs_rt_response):
        """Test parsing vehicle position from GTFS-RT feed"""
        from google.transit import gtfs_realtime_pb2
        
        feed = gtfs_realtime_pb2.FeedMessage()
        feed.ParseFromString(mock_gtfs_rt_response)
        
        assert len(feed.entity) == 1
        assert feed.entity[0].vehicle.vehicle.id == "1001"
        assert feed.entity[0].vehicle.position.latitude == pytest.approx(40.7128)
        assert feed.entity[0].vehicle.position.longitude == pytest.approx(-74.0060)

    def test_gtfs_rt_feed_header_validation(self, mock_gtfs_rt_response):
        """Test GTFS-RT feed header is properly parsed"""
        from google.transit import gtfs_realtime_pb2
        
        feed = gtfs_realtime_pb2.FeedMessage()
        feed.ParseFromString(mock_gtfs_rt_response)
        
        assert feed.header.gtfs_realtime_version == "2.0"
        assert feed.header.incrementality == gtfs_realtime_pb2.FeedHeader.FULL_DATASET
        assert feed.header.timestamp > 0


@pytest.mark.integration
class TestProducerClientIntegration:
    """Tests for Kafka producer client integration"""

    def test_producer_client_can_be_imported(self):
        """Test that producer client modules can be imported"""
        from gtfs_rt_producer_kafka_producer.producer import (
            GeneralTransitFeedRealTimeEventProducer,
            GeneralTransitFeedStaticEventProducer
        )
        
        assert GeneralTransitFeedRealTimeEventProducer is not None
        assert GeneralTransitFeedStaticEventProducer is not None

    def test_producer_data_classes_can_be_imported(self):
        """Test that producer data classes can be imported"""
        from gtfs_rt_producer_data.generaltransitfeedrealtime.vehicle.vehicleposition import VehiclePosition
        from gtfs_rt_producer_data.generaltransitfeedrealtime.trip.tripupdate import TripUpdate
        from gtfs_rt_producer_data.generaltransitfeedrealtime.alert.alert import Alert
        
        assert VehiclePosition is not None
        assert TripUpdate is not None
        assert Alert is not None
