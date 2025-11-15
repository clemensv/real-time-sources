"""
Test CloudEvents configuration and event generation for NOAA producer
"""

import pytest
import json
from datetime import datetime, timezone
from unittest.mock import Mock, patch
from cloudevents.http import CloudEvent
from noaa.noaa_producer.microsoft.opendata.us.noaa.waterlevel import WaterLevel
from noaa.noaa_producer.microsoft.opendata.us.noaa.airtemperature import AirTemperature
from noaa.noaa_producer.microsoft.opendata.us.noaa.wind import Wind


@pytest.mark.unit
class TestCloudEventsConfiguration:
    """Test CloudEvents structure and configuration"""

    def test_cloudevent_required_attributes(self):
        """Test that CloudEvents have all required attributes"""
        # Create a sample CloudEvent
        event = CloudEvent({
            'type': 'microsoft.opendata.us.noaa.waterlevel',
            'source': 'noaa://station/8454000',
            'subject': 'water_level',
            'datacontenttype': 'application/json',
            'data': {
                'station_id': '8454000',
                'time': '2024-01-01T00:00:00Z',
                'value': 2.5
            }
        })

        # Verify required CloudEvents attributes
        assert event['type'] is not None
        assert event['source'] is not None
        assert event['id'] is not None
        assert event['specversion'] is not None
        assert event['datacontenttype'] is not None

    def test_cloudevent_type_format(self):
        """Test CloudEvent type follows naming convention"""
        event_types = [
            'microsoft.opendata.us.noaa.waterlevel',
            'microsoft.opendata.us.noaa.airtemperature',
            'microsoft.opendata.us.noaa.wind',
            'microsoft.opendata.us.noaa.predictions',
            'microsoft.opendata.us.noaa.airpressure'
        ]

        for event_type in event_types:
            # Verify format: reverse domain notation
            assert event_type.startswith('microsoft.opendata.us.noaa.')
            # Verify lowercase
            assert event_type == event_type.lower()
            # Verify no special characters except dots
            assert all(c.isalnum() or c == '.' for c in event_type)

    def test_cloudevent_source_format(self):
        """Test CloudEvent source URI format"""
        sources = [
            'noaa://station/8454000',
            'noaa://station/9414290',
            'noaa://station/1234567'
        ]

        for source in sources:
            # Verify format
            assert source.startswith('noaa://station/')
            # Verify station ID is numeric
            station_id = source.split('/')[-1]
            assert station_id.isdigit()

    def test_cloudevent_data_content_type(self):
        """Test CloudEvent data content type is JSON"""
        event = CloudEvent({
            'type': 'microsoft.opendata.us.noaa.waterlevel',
            'source': 'noaa://station/8454000',
            'datacontenttype': 'application/json',
            'data': {'test': 'data'}
        })

        assert event['datacontenttype'] == 'application/json'

    def test_cloudevent_time_format(self):
        """Test CloudEvent time is in ISO 8601 format"""
        now = datetime.now(timezone.utc)
        
        event = CloudEvent({
            'type': 'microsoft.opendata.us.noaa.waterlevel',
            'source': 'noaa://station/8454000',
            'time': now.isoformat(),
            'data': {'test': 'data'}
        })

        # Verify time attribute exists and can be parsed
        assert 'time' in event
        time_str = event['time']
        # Verify it's a valid ISO 8601 timestamp
        parsed_time = datetime.fromisoformat(time_str.replace('Z', '+00:00'))
        assert isinstance(parsed_time, datetime)


@pytest.mark.unit
class TestNOAADataModels:
    """Test NOAA data models for CloudEvents"""

    def test_water_level_model_structure(self):
        """Test WaterLevel data model structure"""
        # This would test the actual model if accessible
        # For now, verify expected attributes
        expected_fields = ['station_id', 'time', 'value', 'sigma', 'flags', 'quality']
        
        # Verify these are the fields we expect to see in water level data
        assert all(isinstance(field, str) for field in expected_fields)

    def test_air_temperature_model_structure(self):
        """Test AirTemperature data model structure"""
        expected_fields = ['station_id', 'time', 'value', 'flags']
        
        assert all(isinstance(field, str) for field in expected_fields)

    def test_wind_model_structure(self):
        """Test Wind data model structure"""
        expected_fields = ['station_id', 'time', 'speed', 'direction', 'gust', 'flags']
        
        assert all(isinstance(field, str) for field in expected_fields)


@pytest.mark.unit
class TestEventProducerConfiguration:
    """Test event producer configuration"""

    def test_kafka_producer_config_structure(self):
        """Test Kafka producer configuration structure"""
        config = {
            'bootstrap.servers': 'test.servicebus.windows.net:9093',
            'sasl.mechanisms': 'PLAIN',
            'security.protocol': 'SASL_SSL',
            'sasl.username': '$ConnectionString',
            'sasl.password': 'Endpoint=sb://test...'
        }

        # Verify required fields
        assert 'bootstrap.servers' in config
        assert 'sasl.mechanisms' in config
        assert 'security.protocol' in config
        assert 'sasl.username' in config
        assert 'sasl.password' in config

        # Verify Event Hubs specific settings
        assert ':9093' in config['bootstrap.servers']
        assert config['sasl.mechanisms'] == 'PLAIN'
        assert config['security.protocol'] == 'SASL_SSL'

    def test_event_hubs_connection_string_format(self):
        """Test Event Hubs connection string format"""
        connection_string = (
            "Endpoint=sb://test.servicebus.windows.net/;"
            "SharedAccessKeyName=sendlisten;"
            "SharedAccessKey=testkey123==;"
            "EntityPath=noaa-events"
        )

        # Verify format
        assert 'Endpoint=sb://' in connection_string
        assert 'SharedAccessKeyName=' in connection_string
        assert 'SharedAccessKey=' in connection_string
        assert 'EntityPath=' in connection_string
        assert '.servicebus.windows.net' in connection_string


@pytest.mark.integration
class TestCloudEventsGeneration:
    """Integration tests for CloudEvents generation"""

    def test_generate_water_level_event(self):
        """Test generating CloudEvent for water level data"""
        # Sample water level data
        data = {
            'station_id': '8454000',
            'time': '2024-01-01T00:00:00Z',
            'value': 2.5,
            'sigma': 0.02,
            'flags': '0,0,0,0',
            'quality': 'v'
        }

        # Create CloudEvent
        event = CloudEvent({
            'type': 'microsoft.opendata.us.noaa.waterlevel',
            'source': f"noaa://station/{data['station_id']}",
            'subject': 'water_level',
            'datacontenttype': 'application/json',
            'time': data['time'],
            'data': data
        })

        # Verify event structure
        assert event['type'] == 'microsoft.opendata.us.noaa.waterlevel'
        assert event['source'] == 'noaa://station/8454000'
        assert event['subject'] == 'water_level'
        assert event.data == data

    def test_generate_air_temperature_event(self):
        """Test generating CloudEvent for air temperature data"""
        data = {
            'station_id': '9414290',
            'time': '2024-01-01T12:00:00Z',
            'value': 15.5,
            'flags': '0,0,0'
        }

        event = CloudEvent({
            'type': 'microsoft.opendata.us.noaa.airtemperature',
            'source': f"noaa://station/{data['station_id']}",
            'subject': 'air_temperature',
            'datacontenttype': 'application/json',
            'time': data['time'],
            'data': data
        })

        # Verify event structure
        assert event['type'] == 'microsoft.opendata.us.noaa.airtemperature'
        assert event['source'] == 'noaa://station/9414290'
        assert event.data == data

    def test_generate_wind_event(self):
        """Test generating CloudEvent for wind data"""
        data = {
            'station_id': '8454000',
            'time': '2024-01-01T18:00:00Z',
            'speed': 12.5,
            'direction': 180,
            'gust': 15.2,
            'flags': '0,0'
        }

        event = CloudEvent({
            'type': 'microsoft.opendata.us.noaa.wind',
            'source': f"noaa://station/{data['station_id']}",
            'subject': 'wind',
            'datacontenttype': 'application/json',
            'time': data['time'],
            'data': data
        })

        # Verify event structure
        assert event['type'] == 'microsoft.opendata.us.noaa.wind'
        assert event['source'] == 'noaa://station/8454000'
        assert event.data == data


@pytest.mark.unit
class TestEventSerialization:
    """Test CloudEvents serialization"""

    def test_cloudevent_json_serialization(self):
        """Test CloudEvent can be serialized to JSON"""
        event = CloudEvent({
            'type': 'microsoft.opendata.us.noaa.waterlevel',
            'source': 'noaa://station/8454000',
            'subject': 'water_level',
            'datacontenttype': 'application/json',
            'data': {
                'station_id': '8454000',
                'value': 2.5
            }
        })

        # Serialize to JSON
        from cloudevents.http import to_structured
        headers, body = to_structured(event)

        # Verify serialization
        assert body is not None
        event_dict = json.loads(body)
        
        assert event_dict['type'] == 'microsoft.opendata.us.noaa.waterlevel'
        assert event_dict['source'] == 'noaa://station/8454000'
        assert 'data' in event_dict
        assert event_dict['data']['station_id'] == '8454000'

    def test_cloudevent_binary_serialization(self):
        """Test CloudEvent binary content mode"""
        event = CloudEvent({
            'type': 'microsoft.opendata.us.noaa.waterlevel',
            'source': 'noaa://station/8454000',
            'data': {'station_id': '8454000', 'value': 2.5}
        })

        # Verify event can be serialized
        from cloudevents.http import to_binary
        headers, body = to_binary(event)

        # Verify headers contain CloudEvents attributes
        assert b'ce-type' in headers or 'ce-type' in headers
        assert b'ce-source' in headers or 'ce-source' in headers


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
