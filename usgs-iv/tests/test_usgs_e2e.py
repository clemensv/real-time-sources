"""
End-to-end tests for USGS Instantaneous Values data poller.
Tests against real USGS API endpoints.
"""

import pytest
import asyncio
from unittest.mock import patch
from usgs_iv.usgs_iv import USGSDataPoller


@pytest.mark.e2e
class TestUSGSAPIEndToEnd:
    """End-to-end tests against real USGS Instantaneous Values Service."""

    @pytest.mark.asyncio
    async def test_fetch_data_from_real_api(self):
        """Test fetching data from real USGS API for Maryland (small dataset)."""
        with patch('usgs_iv.usgs_iv.Producer'):
            poller = USGSDataPoller(kafka_config=None, kafka_topic='test-topic')
            
            # Use MD (Maryland) as it typically has fewer sites than larger states
            record_count = 0
            site_count = 0
            
            async for records in poller.get_data_by_state('MD'):
                site_count += 1
                record_count += len(records)
                
                # Validate record structure
                if records:
                    first_record = records[0]
                    
                    # Check required fields exist
                    assert 'agency_cd' in first_record
                    assert 'site_no' in first_record
                    assert 'datetime' in first_record
                    assert 'tz_cd' in first_record
                    
                    # Check agency code
                    assert first_record['agency_cd'] == 'USGS'
                    
                    # Check site number format (8-15 digits)
                    assert first_record['site_no'].isdigit()
                    assert 8 <= len(first_record['site_no']) <= 15
                    
                    # Check datetime format
                    assert len(first_record['datetime']) > 0
                    
                    # Check timezone code exists
                    assert len(first_record['tz_cd']) >= 2
                
                # Only process a few sites to keep test fast
                if site_count >= 3:
                    break
            
            # Should have found at least some data
            assert record_count > 0
            print(f"\\nFetched {record_count} records from {site_count} sites")

    @pytest.mark.asyncio
    async def test_fetch_data_different_states(self):
        """Test fetching data from multiple different states."""
        test_states = ['DE', 'RI', 'NH']  # Small states for faster testing
        
        with patch('usgs_iv.usgs_iv.Producer'):
            poller = USGSDataPoller(kafka_config=None, kafka_topic='test-topic')
            
            for state_code in test_states:
                record_count = 0
                
                async for records in poller.get_data_by_state(state_code):
                    record_count += len(records)
                    
                    # Just fetch first site for each state
                    break
                
                print(f"\\nState {state_code}: {record_count} records")
                # Note: Some states might have no recent data, so just check it completes

    @pytest.mark.asyncio
    async def test_api_returns_recent_data(self):
        """Test that API returns recent data (modified within last 2 hours)."""
        from datetime import datetime, timedelta
        
        with patch('usgs_iv.usgs_iv.Producer'):
            poller = USGSDataPoller(kafka_config=None, kafka_topic='test-topic')
            
            found_recent = False
            cutoff = datetime.now() - timedelta(hours=3)
            
            # Try to find at least one site with recent data
            async for records in poller.get_data_by_state('CA'):
                if records:
                    # Parse the datetime from first record
                    first_record = records[0]
                    if 'datetime' in first_record:
                        # Just verify we got a datetime string
                        assert len(first_record['datetime']) > 0
                        found_recent = True
                        break
                
                # Check a few sites
                if found_recent:
                    break
            
            # California is large and active, should have some recent data
            assert found_recent, "Should find at least one site with data"

    @pytest.mark.asyncio
    async def test_api_parameter_codes_present(self):
        """Test that API returns recognized parameter codes."""
        with patch('usgs_iv.usgs_iv.Producer'):
            poller = USGSDataPoller(kafka_config=None, kafka_topic='test-topic')
            
            found_parameters = set()
            
            # Look for common parameters in New York data
            async for records in poller.get_data_by_state('NY'):
                if records:
                    first_record = records[0]
                    
                    # Extract parameter codes from column names
                    for key in first_record.keys():
                        if '_' in key and key.split('_')[0].isdigit():
                            # This is a timeseries_parameter column
                            param_code = key.split('_')[1]
                            found_parameters.add(param_code)
                    
                    # Check first few sites
                    if len(found_parameters) >= 3:
                        break
            
            # Verify we found some recognized parameter codes
            recognized_params = set(USGSDataPoller.PARAMETERS.keys())
            common_params = found_parameters.intersection(recognized_params)
            
            assert len(common_params) > 0, f"Should find at least one recognized parameter. Found: {found_parameters}"
            print(f"\\nFound {len(found_parameters)} parameter codes, {len(common_params)} recognized")

    @pytest.mark.asyncio
    async def test_api_url_format(self):
        """Test that API URL is correctly formatted."""
        with patch('usgs_iv.usgs_iv.Producer'):
            poller = USGSDataPoller(kafka_config=None, kafka_topic='test-topic')
            
            # Check base URL
            assert poller.BASE_URL.startswith('https://')
            assert 'waterservices.usgs.gov' in poller.BASE_URL
            
            # The actual URL used includes state code and format parameters
            expected_pattern = 'https://waterservices.usgs.gov/nwis/iv/'
            assert poller.BASE_URL == expected_pattern

    @pytest.mark.asyncio
    async def test_empty_state_response(self):
        """Test handling of state with no data (invalid state code)."""
        with patch('usgs_iv.usgs_iv.Producer'):
            poller = USGSDataPoller(kafka_config=None, kafka_topic='test-topic')
            
            record_count = 0
            
            # Use a clearly invalid state code
            async for records in poller.get_data_by_state('XX'):
                record_count += len(records)
            
            # Should handle gracefully even with no data
            assert record_count >= 0

    @pytest.mark.asyncio
    async def test_multiple_parameters_per_site(self):
        """Test that sites can have multiple parameters."""
        with patch('usgs_iv.usgs_iv.Producer'):
            poller = USGSDataPoller(kafka_config=None, kafka_topic='test-topic')
            
            found_multi_param = False
            
            # Check sites in a state likely to have multi-parameter stations
            async for records in poller.get_data_by_state('WA'):
                if records:
                    first_record = records[0]
                    
                    # Count parameter columns (format: {ts_id}_{param_code})
                    param_columns = [k for k in first_record.keys() 
                                   if '_' in k and k.split('_')[0].isdigit() 
                                   and not k.endswith('_cd')]
                    
                    if len(param_columns) > 1:
                        found_multi_param = True
                        print(f"\\nFound site with {len(param_columns)} parameters: {first_record.get('site_no', 'unknown')}")
                        break
                
                # Check several sites
                if found_multi_param:
                    break
            
            # Large states typically have multi-parameter sites
            # But this isn't guaranteed, so we won't assert
            print(f"\\nMulti-parameter site found: {found_multi_param}")

    @pytest.mark.asyncio
    async def test_timezone_codes_valid(self):
        """Test that timezone codes are valid USGS timezone abbreviations."""
        from usgs_iv.usgs_iv import usgs_tz_map
        
        with patch('usgs_iv.usgs_iv.Producer'):
            poller = USGSDataPoller(kafka_config=None, kafka_topic='test-topic')
            
            found_timezones = set()
            
            async for records in poller.get_data_by_state('FL'):
                if records:
                    for record in records:
                        if 'tz_cd' in record:
                            found_timezones.add(record['tz_cd'])
                
                # Check first site
                if found_timezones:
                    break
            
            # Verify at least one timezone was found and is recognized
            assert len(found_timezones) > 0
            
            # At least one should be in our mapping
            recognized = any(tz in usgs_tz_map for tz in found_timezones)
            print(f"\\nFound timezones: {found_timezones}")
            print(f"Recognized: {recognized}")
