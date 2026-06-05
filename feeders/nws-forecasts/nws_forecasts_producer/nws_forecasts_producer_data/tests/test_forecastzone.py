"""
Test case for ForecastZone
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from nws_forecasts_producer_data.forecastzone import ForecastZone
from nws_forecasts_producer_data.zonetypeenum import ZoneTypeenum
import datetime


class Test_ForecastZone(unittest.TestCase):
    """
    Test case for ForecastZone
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_ForecastZone.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of ForecastZone for testing
        """
        instance = ForecastZone(
            zone_id='tmabqihhlklojqxpkxsb',
            zone_type=ZoneTypeenum.public,
            name='rpznonlcqbxlhryfqbkg',
            state='dkykxvsjezyuqsslxhmg',
            forecast_office_url='dlpvnrchzmzxcvbbngem',
            grid_identifier='mzklfermfmvgglypqjrf',
            awips_location_identifier='vuzwjcipvkkcdoipalvg',
            cwa_ids=['rsmtnqcoduijxqdsjqgv', 'kcnlcxcqhebpthnccbps', 'fbyuvmggozdbtzrnjicc', 'tznvewguqpfbiusrqmns', 'ethfjqohfhzgqipwnumd'],
            forecast_office_urls=['ijaatgmwqkuukhdutuem', 'zdmyyacexqogzyzttysa'],
            time_zones=['fnrhihdswdhlipfalmme', 'jblsetzglaqsxmfqwlyt', 'cnjszqbmvfcfvfqztoku'],
            observation_station_ids=['dybnrzwhceaertsdygnh', 'zfqydmpsqwgukfxghlyz', 'sxexiuxnbiuniigrmdts', 'nfewwdajrotaknyypybz'],
            radar_station='ikwchatktfiklfsrpvuc',
            effective_date=datetime.datetime.now(datetime.timezone.utc),
            expiration_date=datetime.datetime.now(datetime.timezone.utc)
        )
        return instance

    
    def test_zone_id_property(self):
        """
        Test zone_id property
        """
        test_value = 'tmabqihhlklojqxpkxsb'
        self.instance.zone_id = test_value
        self.assertEqual(self.instance.zone_id, test_value)
    
    def test_zone_type_property(self):
        """
        Test zone_type property
        """
        test_value = ZoneTypeenum.public
        self.instance.zone_type = test_value
        self.assertEqual(self.instance.zone_type, test_value)
    
    def test_name_property(self):
        """
        Test name property
        """
        test_value = 'rpznonlcqbxlhryfqbkg'
        self.instance.name = test_value
        self.assertEqual(self.instance.name, test_value)
    
    def test_state_property(self):
        """
        Test state property
        """
        test_value = 'dkykxvsjezyuqsslxhmg'
        self.instance.state = test_value
        self.assertEqual(self.instance.state, test_value)
    
    def test_forecast_office_url_property(self):
        """
        Test forecast_office_url property
        """
        test_value = 'dlpvnrchzmzxcvbbngem'
        self.instance.forecast_office_url = test_value
        self.assertEqual(self.instance.forecast_office_url, test_value)
    
    def test_grid_identifier_property(self):
        """
        Test grid_identifier property
        """
        test_value = 'mzklfermfmvgglypqjrf'
        self.instance.grid_identifier = test_value
        self.assertEqual(self.instance.grid_identifier, test_value)
    
    def test_awips_location_identifier_property(self):
        """
        Test awips_location_identifier property
        """
        test_value = 'vuzwjcipvkkcdoipalvg'
        self.instance.awips_location_identifier = test_value
        self.assertEqual(self.instance.awips_location_identifier, test_value)
    
    def test_cwa_ids_property(self):
        """
        Test cwa_ids property
        """
        test_value = ['rsmtnqcoduijxqdsjqgv', 'kcnlcxcqhebpthnccbps', 'fbyuvmggozdbtzrnjicc', 'tznvewguqpfbiusrqmns', 'ethfjqohfhzgqipwnumd']
        self.instance.cwa_ids = test_value
        self.assertEqual(self.instance.cwa_ids, test_value)
    
    def test_forecast_office_urls_property(self):
        """
        Test forecast_office_urls property
        """
        test_value = ['ijaatgmwqkuukhdutuem', 'zdmyyacexqogzyzttysa']
        self.instance.forecast_office_urls = test_value
        self.assertEqual(self.instance.forecast_office_urls, test_value)
    
    def test_time_zones_property(self):
        """
        Test time_zones property
        """
        test_value = ['fnrhihdswdhlipfalmme', 'jblsetzglaqsxmfqwlyt', 'cnjszqbmvfcfvfqztoku']
        self.instance.time_zones = test_value
        self.assertEqual(self.instance.time_zones, test_value)
    
    def test_observation_station_ids_property(self):
        """
        Test observation_station_ids property
        """
        test_value = ['dybnrzwhceaertsdygnh', 'zfqydmpsqwgukfxghlyz', 'sxexiuxnbiuniigrmdts', 'nfewwdajrotaknyypybz']
        self.instance.observation_station_ids = test_value
        self.assertEqual(self.instance.observation_station_ids, test_value)
    
    def test_radar_station_property(self):
        """
        Test radar_station property
        """
        test_value = 'ikwchatktfiklfsrpvuc'
        self.instance.radar_station = test_value
        self.assertEqual(self.instance.radar_station, test_value)
    
    def test_effective_date_property(self):
        """
        Test effective_date property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.effective_date = test_value
        self.assertEqual(self.instance.effective_date, test_value)
    
    def test_expiration_date_property(self):
        """
        Test expiration_date property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.expiration_date = test_value
        self.assertEqual(self.instance.expiration_date, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = ForecastZone.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = ForecastZone.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

